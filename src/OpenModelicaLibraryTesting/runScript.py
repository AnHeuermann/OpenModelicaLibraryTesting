"""
This file is part of OpenModelica.

Copyright (c) 1998-2024, Open Source Modelica Consortium (OSMC),
c/o Linköpings universitet, Department of Computer and Information Science,
SE-58183 Linköping, Sweden.

All rights reserved.

THIS PROGRAM IS PROVIDED UNDER THE TERMS OF GPL VERSION 3 LICENSE OR
THIS OSMC PUBLIC LICENSE (OSMC-PL) VERSION 1.2.
ANY USE, REPRODUCTION OR DISTRIBUTION OF THIS PROGRAM CONSTITUTES
RECIPIENT'S ACCEPTANCE OF THE OSMC PUBLIC LICENSE OR THE GPL VERSION 3,
ACCORDING TO RECIPIENTS CHOICE.

The OpenModelica software and the Open Source Modelica
Consortium (OSMC) Public License (OSMC-PL) are obtained
from OSMC, either from the above address,
from the URLs: http://www.ida.liu.se/projects/OpenModelica or
http://www.openmodelica.org, and in the OpenModelica distribution.
GNU version 3 is obtained from: http://www.gnu.org/copyleft/gpl.html.

This program is distributed WITHOUT ANY WARRANTY; without
even the implied warranty of  MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE, EXCEPT AS EXPRESSLY SET FORTH
IN THE BY RECIPIENT SELECTED SUBSIDIARY LICENSE CONDITIONS OF OSMC-PL.

See the full OSMC Public License conditions for more details.
"""

from monotonic import monotonic
import os
import simplejson as json
import sys

from runCommand import runCommand

def runScript(config, timeout, memoryLimit, msysEnvironment:str, librariespath:str, ompython_omhome:str, docker:bool, clean: bool, verbose: bool):
  isWin = os.name == 'nt'

  j = os.path.normpath("files/%s.stat.json" % config)
  try:
    os.remove(j)
  except:
    pass
  start=monotonic()
  # runCommand("%s %s %s.mos" % (omc_exe, single_thread, c), prefix=c, timeout=timeout)
  if verbose:
    print(f"Starting test: {config}")
    sys.stdout.flush()

  if isWin:
    cmd = (f"python testmodel.py --win "
          f"--msysEnvironment={msysEnvironment} "
          f"--libraries={librariespath} "
          f"{'--docker {docker} --dockerExtraArgs \'{dockerExtraArgs}\'' if docker else ''} "
          f"--ompython_omhome={ompython_omhome} "
          f"{config}.conf.json > files/{config}.cmdout 2>&1")
  else:
    cmd = (f"ulimit -v {memoryLimit}; "
          f"./testmodel.py "
          f"--libraries={librariespath} "
          f"{'--docker {docker} --dockerExtraArgs \'{dockerExtraArgs}\'' if docker else ''} "
          f"--ompython_omhome={ompython_omhome} "
          f"{config}.conf.json > files/{config}.cmdout 2>&1")

  if runCommand(cmd, prefix=config, timeout=timeout) != 0:
    print(f"files/{config}.err")
    with open(os.path.normpath("files/%s.err" % config), "a+") as errfile:
      errfile.write("Failed to read output from testmodel.py, exit status != 0:\n")
      try:
        with open(os.path.normpath("files/%s.cmdout" % config)) as cmdout:
          errfile.write(cmdout.read())
      except IOError:
        pass
      except OSError:
        pass

  if clean:
    try:
      os.unlink(os.path.normpath("files/%s.cmdout" % config))
    except OSError:
      pass

  execTime=monotonic()-start
  assert(execTime >= 0.0)
  try:
    data=json.load(open(j))
  except:
    data = {"phase":0}
  data["exectime"] = execTime
  json.dump(data, open(j,"w"))
  if verbose:
    print("Finished test: %s - %d[s]" % (config, execTime))
    sys.stdout.flush()
