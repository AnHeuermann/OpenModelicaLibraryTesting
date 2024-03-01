
import os
import subprocess

def testHelloWorld(omc_cmd, cmd):
  isWin = os.name == 'nt'
  exeExt = ".exe" if isWin else ""

  with open("HelloWorld.mos") as fin:
    helloWorldContents = fin.read()
  try:
    os.unlink("HelloWorld"+exeExt)
  except OSError:
    pass
  open("HelloWorld.cmd.mos","w").write(cmd + "\n" + helloWorldContents)
  try:
    out=subprocess.check_output(omc_cmd + ["HelloWorld.cmd.mos"], stderr=subprocess.STDOUT)
    if os.path.exists("HelloWorld"+exeExt) and not "Error:" in out.decode():
      return True
  except subprocess.CalledProcessError as e:
    pass
  return False
