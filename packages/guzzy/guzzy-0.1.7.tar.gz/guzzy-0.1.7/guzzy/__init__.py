from pysheller import PySheller
from os import chdir
from os.path import dirname, realpath, join


def main():
    dir_path = dirname(realpath(__file__))

    PySheller(
        name="guzzy",
        description="Interactive CLI git client inside fzf.",
        commands_dir=join(dir_path, "commands"),
    )
