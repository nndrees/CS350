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

def _testerror(message):
  print("ERROR: test is written incorrectly: " + message + ".")
  print("REPORT THIS TO YOUR INSTRUCTOR!")

def _testfailprint(expected, got):
  try:
    print("Test Failed!")
    print("Expected: " + expected)
    print("Got: " + got)
  except:
    _testerror("Error while printing error message")

def runnotice(command):
  print("--- Running: '" + command + "'")

def runbasictest(command, expectedoutput):
  runnotice(command)
  try:
    child = pexpect.spawn(command)
    child.expect_exact(expectedoutput)
    if child.before:
      raise
    return True
  except:
    _testfailprint(expectedoutput, child.before.decode("utf-8"))
    return False

def runinteractivetest(command, prompts, expectedoutputs):
  runnotice(command)

  if len(prompts) != len(expectedoutputs):
    _testerror("mismatched number of prompts and outputs")
    return False

  try:
    child = pexpect.spawn(command)
    for i in range(len(prompts)):
      this_prompt = prompts[i]
      this_expected = expectedoutputs[i]
      if this_prompt:
        child.sendline(this_prompt)
      child.expect_exact(this_expected, timeout=5)
      if child.before and \
         child.before.decode("utf-8").strip() != this_prompt.strip():
        raise
    return True
  except:
    _testfailprint(this_expected, child.before.decode("utf-8"))
    return False

def runmultilinetest(command, prompts, expected):
  runnotice(command)

  try:
    child = pexpect.spawn(command)
    for i in range(len(prompts)):
      child.sendline(prompts[i])
    output = child.read().decode("utf-8")
    if output.strip().replace('\r', '') == expected.strip():
      return True
    else:
      _testfailprint("\n" + expected, "\n" + output)
      return False
  except pexpect.EOF:
    _testfailprint(expected, child.before.decode("utf-8"))
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
