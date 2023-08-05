import os
import re
import sys
import time
import typing
from subprocess import PIPE, Popen

DEBUG = 1
ON_POSIX = "posix" in sys.builtin_module_names


# This is getting ridiculously advance. We basically have to run tests on pdb,
# while capturing the input/output to get/parse the results and send commands.
# The most important thing is to know line coverages for the unit test system.

# In order to achieve this monstrosity, we have to use subprocess to call pdb.
# subprocess.Popen() executes a child program in a new process, which makes it
# possible to run pdb parallelly while the input/output can be handled easily.


class UnexpectedSituation(Exception):
    pass


def file_in_dir(f, d):
    for file in os.listdir(d):
        if os.path.isdir(file):
            if file_in_dir(f, file):
                return True
            continue
        # file
        if os.path.abspath(os.path.join(d, file)) == os.path.abspath(f):
            return True
    return False


class Interacter:
    end = False
    outstr = ""
    coverage = {}
    src: str

    def __init__(self, src_dir):
        self.src = src_dir

    def flush(self):
        self.p.stdout.flush()
        self.p.stderr.flush()
        self.p.stdin.flush()

    def getch(self):
        if self.p.poll() is None:  # I hope the proc is still running
            self.p.stdout.flush()
            ch = self.p.stdout.read(1)
            self.outstr += ch
            if DEBUG:
                print(end=ch)
            return ch

    def wait_prompt(self):
        while True:
            self.getch()
            if self.outstr.split("\n")[-1] == "(Pdb) ":
                return

    def cont(self):
        """Continue."""
        while True:
            self.n()
            if "  # huputs: breakpoint()\n" in self.outstr or self.end:
                self.outstr = ""
                return

    def clr(self):
        self.outstr = ""
        self.flush()

    def run(self, s: str):
        self.outstr = ""
        self.p.stdin.write(s + "\n")
        self.p.stdin.flush()
        if DEBUG:
            print(s)
        self.wait_prompt()
        if (
            "The program finished and will be restarted" in self.outstr
            or self.end == True
        ):
            self.end = True
            self.p.terminate()
            return
        if "  # huputs: breakpoint()\n" in self.outstr:
            return
        if "  # huputs: err\n" in self.outstr:
            print("Error")
            self.outstr = ""
            self.p.stdin.write("err.__traceback__\n")
            self.p.stdin.flush()
            self.wait_prompt()
            print(self.outstr[:-6])
            self.end = True
            self.p.terminate()
            return
        self.record_coverage()

    def get_to_ex(self):
        """Jump to the executor."""
        self.run("n")
        self.run("n")
        self.run("s")
        # the -4'th line should be "(Pdb) --Call--"
        if self.outstr.startswith("--Call--"):
            return
        print(self.outstr)
        raise UnexpectedSituation()

    def record_coverage(self):
        try:
            m = re.search(
                r"> (.+)\(([0-9]+)\)([a-zA-Z_]\w*|<\w+>)\(\)",
                [
                    l
                    for l in self.outstr.splitlines()
                    if l.startswith("> ") and not l.endswith(">()")
                ][0],
            )
        except IndexError:
            return
        if not m:
            print(self.outstr)
            raise UnexpectedSituation
        path = m.group(1)
        if file_in_dir(path, self.src):
            try:
                self.coverage[path].add(int(m.group(2)))
            except KeyError:
                self.coverage[path] = set([int(m.group(2))])

    def in_src(self):
        # lines = self.outstr.splitlines()
        m = re.search(
            r"> (.+)\(([0-9]+)\)([a-zA-Z_]\w*|<\w+>)\(\)", self.outstr
        )
        if not m:
            print("!! FATAL !!  expected path:")
            print(self.outstr)
            raise UnexpectedSituation
        path = m.group(1)
        if path.startswith("<"):
            return False
        return file_in_dir(path, self.src) and path.startswith(
            os.path.abspath(self.src)
        )

    def n(self):
        if self.end:
            return
        self.flush()
        if "--Return--" in self.outstr.splitlines():
            self.run("n")
            return
        self.run("s")
        lines = self.outstr.splitlines()

        # check if a fn is called
        while "--Call--" in lines or not self.in_src():
            # get back out
            self.run("r")
            if self.end or "  # huputs: breakpoint()\n" in self.outstr:
                return
            if "--Return--" in self.outstr.splitlines():
                self.run("n")
            lines = self.outstr.splitlines()

    def q(self):
        self.p.stdin.write("q\n")
        self.flush()

    def test_out_with_coverage(self, path):
        self.py = sys.executable
        cmd = [self.py, "-u", "-m", "pdb", path]
        self.p = Popen(
            cmd,
            stdout=PIPE,
            stdin=PIPE,
            stderr=PIPE,
            close_fds=ON_POSIX,
            universal_newlines=True,
        )
        self.wait_prompt()
        # skip to huputs.py(500)test_out()
        self.cont()
        if self.end:
            self.q()
            return
        self.clr()
        self.get_to_ex()
        self.record_coverage()
        while True:
            self.n()
            if self.end:
                self.q()
                self.p.wait()
                return
            # detect errors
            l = self.outstr.splitlines()[0]
            if ":" in l:
                self.q()
                return l

    def test_out(self, path, cwd):
        self.p = Popen(
            [sys.executable, path],
            stderr=PIPE,
            close_fds=ON_POSIX,
            universal_newlines=True,
            cwd=cwd
        )
        self.p.wait()
        print(end=self.p.stderr.read())


if __name__ == "__main__":
    try:
        interact = Interacter(".")
        interact.test_out("simple_testing.py")
    except BrokenPipeError:
        print("Pipe is broken, exit.")
