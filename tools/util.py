import os
import re
import sys
import subprocess

root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
third_party_path = os.path.join(root_path, "third_party")


def make_env(merge_env=None, env=None):
    if env is None:
        env = os.environ
    env = env.copy()
    if merge_env is None:
        merge_env = {}
    for key in merge_env.keys():
        env[key] = merge_env[key]
    return env


def shell_quote_win(arg):
    if re.search(r'[\x00-\x20"^%~!@&?*<>|()=]', arg):
        # Double all " quote characters.
        arg = arg.replace('"', '""')
        # Wrap the entire string in " quotes.
        arg = '"' + arg + '"'
        # Double any N backslashes that are immediately followed by a " quote.
        arg = re.sub(r'(\\+)(?=")', r'\1\1', arg)
    return arg


def shell_quote(arg):
    if os.name == "nt":
        return shell_quote_win(arg)
    else:
        # Python has posix shell quoting built in, albeit in a weird place.
        from pipes import quote
        return quote(arg)


def find_exts(directories, extensions, skip=None):
    if skip is None:
        skip = []
    assert isinstance(directories, list)
    assert isinstance(extensions, list)
    skip = [os.path.normpath(i) for i in skip]
    matches = []
    for directory in directories:
        for root, dirnames, filenames in os.walk(directory):
            if root in skip:
                dirnames[:] = []  # Don't recurse further into this directory.
                continue
            for filename in filenames:
                for ext in extensions:
                    if filename.endswith(ext):
                        matches.append(os.path.join(root, filename))
                        break
    return matches


def run(args, quiet=False, cwd=None, env=None, merge_env=None, shell=None):
    args[0] = os.path.normpath(args[0])
    env = make_env(env=env, merge_env=merge_env)
    if shell is None:
        # Use the default value for 'shell' parameter.
        #   - Posix: do not use shell.
        #   - Windows: use shell; this makes .bat/.cmd files work.
        shell = os.name == "nt"
    if not quiet:
        print(" ".join([shell_quote(arg) for arg in args]))
    rc = subprocess.call(args, cwd=cwd, env=env, shell=shell)
    if rc != 0:
        sys.exit(rc)
