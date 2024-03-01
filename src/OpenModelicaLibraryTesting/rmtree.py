import shutil
import subprocess

def rmtree(f):
  try:
    shutil.rmtree(f)
  except UnicodeDecodeError:
    # Yes, we can get UnicodeDecodeError because shutil.rmtree is poorly implemented
    subprocess.check_call(["rm", "-rf", f], stderr=subprocess.STDOUT)
