# import os
import sys
import subprocess
from . import notify
# import notify
import time
import signal
import threading
import os
import json
import argparse
from . import auth
# import auth
import pathlib
import re

SCRIPT_LOCATION = pathlib.Path(os.path.realpath(os.path.dirname(__file__)))
CONFIG_LOCATION = SCRIPT_LOCATION / 'config.json'


class timeout:
    def __init__(self, link, cmd, starttime, lastline, seconds=1):
        self.seconds = seconds
        self.cmd = cmd
        self.lastline = lastline
        self.starttime = starttime
        self.link = link

    def handle_timeout(self, signum, frame):
        notify.slack_notify(
            self.link,
            "timeout",
            cmd=self.cmd,
            starttime=self.starttime,
            lastline=self.lastline,
            hangth=self.seconds
        )

    def __enter__(self):
        if os.name == 'nt':
            # Windows
            alarm = threading.Timer(self.seconds, self.handle_timeout)
            alarm.start()
        else:
            # UNIX
            signal.signal(signal.SIGALRM, self.handle_timeout)
            signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        if os.name == 'nt':
            # Windows
            alarm.cancel()
        else:
            # UNIX
            signal.alarm(0)


def getchar(p):
    c = p.stdout.read(1).decode(sys.stdout.encoding)
    if c == "":
        return -1
    else:
        return c


def getcharerr(p):
    c = p.stderr.read(1).decode(sys.stdout.encoding)
    if c == "":
        return -1
    else:
        return c


def main():
    # parse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--hangthreshold',
        '-ht',
        help='Override config on hang threshold for sending hanging alert [seconds]',
        type=int,
        default=-1
    )
    parser.add_argument(
        '--regex',
        help='Send alert when output matches regex',
        type=str,
        default="$."
    ),
    parser.add_argument(
        '--change',
        help='Change alert channel.',
        action='store_true',
        default=False
    ),
    parser.add_argument(
        '--reset',
        help='Revert to factory settings',
        action='store_true',
        default=False
    )
    parser.add_argument(
        "command",
        help='Command to be executed.',
        nargs=argparse.REMAINDER
    )
    args = parser.parse_args()

    # if reset is True
    if args.reset:
        os.remove(CONFIG_LOCATION)
        auth.main()

    # load configuration
    if os.path.exists(CONFIG_LOCATION):
        with open(CONFIG_LOCATION, 'r') as f:
            config = json.load(f)

        if len(config["link"]) == 0:
            auth.main()
    else:
        auth.main()
        with open(CONFIG_LOCATION, 'r') as f:
            config = json.load(f)

    # if hangthreshold is defined
    try:
        if args.hangthreshold != -1:
            config["hangthreshold"] = args.hangthreshold
            with open(CONFIG_LOCATION, 'w') as f:
                json.dump(config, f, ensure_ascii=False, indent=4,
                          sort_keys=True, separators=(',', ': '))
    except KeyError:
        raise ValueError("Could not read config.json file. Consider using --reset to reset.")

    # load link
    try:
        link = config["link"]["url"]
        HANGTHRESHOLD = config["hangthreshold"]

    except KeyError:
        raise ValueError("Could not read config.json file. Consider using --reset to reset.")

    # regex
    # pattern = re.compile(args.regex)

    # if change is True
    if args.change:
        auth.main()

    if len(args.command) == 0:
        parser.print_help(sys.stderr)
        sys.exit(0)

    # start ------------------------
    starttime = time.time()
    line = ""
    lastline = ""
    stderr_record = ""
    line_reported = False

    p = subprocess.Popen(args.command, bufsize=0, stdin=sys.stdin,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # for each output char
    while p.poll() is None:
        nomore = False
        while not nomore:
            # while p.stdout.:
            with timeout(
                link=link,
                cmd=args.command,
                starttime=starttime,
                lastline=line,
                seconds=HANGTHRESHOLD
            ):
                c = getchar(p)
            if c == '\n':
                lastline = line
                line = ""
                line_reported = False
            if c != -1:
                line += c
                sys.stdout.write(c)
                sys.stdout.flush()
            else:
                nomore = True
                continue
            if re.search(args.regex, line) and not line_reported:
                notify.slack_notify(
                    link,
                    "regex_notify",
                    cmd=args.command,
                    lastline=line,
                    starttime=starttime,
                    regex=args.regex
                )
                line_reported = True

        nomore = False
        while not nomore:
            c = getcharerr(p)
            if c == -1:
                nomore = True
                continue
            else:
                nomore = False
            if c != -1:
                sys.stderr.write(c)
                stderr_record += c
                sys.stderr.flush()

    # process ended
    endtime = time.time()
    if p.returncode == 0:
        notify.slack_notify(
            link,
            "successful",
            cmd=args.command,
            lastline=lastline,
            starttime=starttime,
            endtime=endtime,
            returncode=p.returncode
        )
    else:
        notify.slack_notify(
            link,
            "ended with error",
            cmd=args.command,
            lastline=lastline,
            errmsg=stderr_record,
            starttime=starttime,
            endtime=endtime,
            returncode=p.returncode
        )


if __name__ == "__main__":
    main()
