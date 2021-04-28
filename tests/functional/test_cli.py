import os
import shutil
import subprocess
import sys

import saltfactories


def test_salt_factories_cli():
    if not shutil.which("salt-factories") and os.path.isfile("saltfactories/cli.py"):
        # Binary not installed, but local source available
        cmd = [sys.executable, "-m", "saltfactories.cli"]
    else:
        cmd = ["salt-factories"]
    ret = subprocess.run(
        cmd + ["--coverage"],
        stdout=subprocess.PIPE,
        universal_newlines=True,
        check=False,
    )
    assert ret.returncode == 0
    assert ret.stdout
    assert ret.stdout.strip() == str(saltfactories.CODE_ROOT_DIR / "utils" / "coverage")
