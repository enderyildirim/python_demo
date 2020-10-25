import os
from subprocess import CalledProcessError
from subprocess import STDOUT
from subprocess import check_output


def print_error(err: CalledProcessError):
    print(err)
    print(err.output.decode("utf-8"))


def run_command(command: list):
    try:
        return check_output(command, stderr=STDOUT)
    except CalledProcessError as err:
        print_error(err)
        return None


class Repo:
    def __init__(self, path: str):
        if not os.path.isdir(path):
            raise ValueError(f"Path must be a repository directory : {path}")
        self.path = path

    def create_tag(self, *, tag_name, commit=None):
        command = ["git", "-C", self.path, "tag", "-a", tag_name, "-m", "v{}".format(tag_name)]
        if commit:
            command.append(commit)
        return run_command(command) is not None

    def tags(self) -> list:
        command = ["git", "-C", self.path, "tag", "-l"]
        output = run_command(command)
        if output:
            return [tag for tag in output.decode("utf-8").splitlines() if len(tag.strip()) > 0]
        return []

    def fetch(self, *, tags=True, _all=True):
        command = ["git", "-C", self.path, "fetch"]
        if _all:
            command.append("--all")
        if tags:
            command.append("--tag")
        return run_command(command)

    def checkout(self, *, branch=None, commit=None):
        command = ["git", "-C", self.path, "checkout"]
        if branch:
            command.append(branch)
        if commit:
            command.append(commit)
        return run_command(command)

    def push(self, *, branch, tags=True):
        command = ["git", "-C", self.path, "push", "origin", branch]
        if tags:
            command.append("--tag")
        return run_command(command)

    def pull(self, *, branch):
        command = ["git", "-C", self.path, "pull", "origin", branch]
        return run_command(command)

    def __str__(self) -> str:
        return "Repo({})".format(self.path)
