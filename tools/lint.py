#!/usr/bin/env python3
import os
import sys
from util import third_party_path, root_path, run

cpplint = os.path.join(third_party_path, "python_packages", "cpplint.py")
os.chdir(root_path)
run([
    sys.executable, cpplint,
    "--filter=-build/include_subdir,-legal/copyright,-build/header_guard",
    "--recursive", "src", "test"
])
