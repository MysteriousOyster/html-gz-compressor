import subprocess

# The location of your system Python. Can be different for anyone.
# TODO: fill in.
SYSTEM_PYTHON = r""
COMPRESSOR_PATH = r"compressor.py"

if SYSTEM_PYTHON == "":
    raise ValueError("SYSTEM_PYTHON path must not be empty!")

subprocess.check_call([
    SYSTEM_PYTHON,
    COMPRESSOR_PATH
])
