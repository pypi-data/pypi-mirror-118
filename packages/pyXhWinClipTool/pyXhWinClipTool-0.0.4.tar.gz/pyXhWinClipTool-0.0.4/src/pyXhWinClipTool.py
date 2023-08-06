import subprocess
import argparse
import sys


def from_clip() -> str:
    return subprocess.run("powershell get-clipboard", universal_newlines=True, capture_output=True).stdout


def to_clip(text: str, replace: bool = False):
    if replace:
        subprocess.run("clip", universal_newlines=True, input=text.replace("\n", "\\n").replace("\t", "\\t"))
    else:
        subprocess.run("clip", universal_newlines=True, input=text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="clip board tools for windows only(default --copy)")
    parser.add_argument("-p", "--paste", dest='copy_cmd', help="retrieve data from clipboard", action='store_false')
    parser.add_argument("-c", "--copy", dest='copy_cmd', help="copy input to clipboard", action='store_true')
    parser.set_defaults(copy_cmd=True)
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        exit(0)

    if args.copy_cmd :
        data = ""
        for line in sys.stdin:
            data = data+line
        to_clip(data)
    else:
        data = from_clip()
        print(data)
