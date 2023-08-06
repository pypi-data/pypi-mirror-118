from os import listdir, path
from argparse import ArgumentParser
from subprocess import call


def main():
    dir_path = path.join(path.dirname(path.realpath(__file__)), "commands")
    commands = [x.replace(".sh", "") for x in listdir(dir_path)]

    parser = ArgumentParser(
        prog="guzzy",
        description="Interactive CLI git client inside fzf.",
        allow_abbrev=False,
    )
    parser.add_argument("command", choices=commands)
    args = parser.parse_args()

    call(path.join(dir_path, f"{args.command}.sh"), shell=True)
