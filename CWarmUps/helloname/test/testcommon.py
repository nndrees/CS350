import pexpect
import os
import tempfile
import shutil
from contextlib import contextmanager

totalTests = 0
passedTests = 0

@contextmanager
def _testdir():
  # significant code and motivation:
  # https://stackoverflow.com/questions/21257782/how-to-remove-file-when-program-exits
  path = tempfile.mkdtemp(suffix=".testdir", dir=os.getcwd())
  try:
    yield path
  finally:
    pass
    try:
      shutil.rmtree(path)
    except IOError:
      # do nothing...user has to delete it manually!
      pass

def runnotice(command):
  print("--- Running: '" + command + "'")

def runbasictest(command, expectedoutput):
  runnotice(command)
  try:
    child = pexpect.spawn(command)
    child.expect(expectedoutput)
    if child.before:
      raise
    return True
  except:
    print("Test Failed!")
    print("Expected: " + expectedoutput)
    print("Got: " + child.before.decode("utf-8"))
    return False

def runcompiletest(compilecommand):
  runnotice(compilecommand)
  child = pexpect.spawn(compilecommand)
  output = child.read()
  if not output:
    return True
  else:
    print("Compilation error!")
    print(output.decode("utf-8"))
    return False

def _runonetest(toRun):
  global totalTests
  global passedTests

  totalTests += 1
  if toRun():
    passedTests += 1
    return True
  return False

def _printpassedratio():
  print("\n\nTests passed: %d / %d" % (passedTests, totalTests))

def runtests(compiletest, othertests):
  with _testdir() as test_dir:
    os.chdir(test_dir)

    if not _runonetest(compiletest):
      _printpassedratio()
      exit(1)

    for test in othertests:
      _runonetest(test)
    _printpassedratio()
