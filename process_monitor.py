# -*- coding: utf-8 -*-

import sys
import os
from subprocess import check_output
import subprocess
import psutil
import time

# Usage
usage = '''
    Version: %s
    Author:  %s
    Usage:   %s <processName>
    Example: %s processor
    Output: monitor process memory and file handle number
''' % ('0.1.0', 'keithMaybe10', os.path.basename(sys.argv[0]), os.path.basename(sys.argv[0]))


def monitorProcess(processName):
    try:
        processorPID = int(check_output(["pidof", processName]).split()[0])
    except subprocess.CalledProcessError as e:
        print(e.output)
        try:
            sys.exit(0)
        except:
            print('Please check process name')
    print('monitor process: %s, PID: %s' % ('processor', processorPID))
    p = psutil.Process(processorPID)
    currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(p.create_time()))
    fileHandleNumber = subprocess.Popen('ls -l /proc/' + str(processorPID) + '/fd/ | wc -l', shell=True,
                                        stdout=subprocess.PIPE)
    out, err = fileHandleNumber.communicate()
    handleNumber = out.splitlines()[0]
    print('process start with %s file handle, create time: ' % (handleNumber, currentTime))

    # get memory info of system
    processMemory = psutil.virtual_memory()
    totalMemory = processMemory.total / (1024 * 1024 * 1024)
    freeMemory = processMemory.free / (1024 * 1024 * 1024)
    usedPercent = processMemory.used
    print('total memory: %s GB; free memory: %s GB; memory use percent: %s, current process used percent: %s' % (
        totalMemory, freeMemory, processMemory.used, p.memory_percent()))

    while (True):
        if (psutil.pid_exists(processorPID)):
            out, err = subprocess.Popen('ls -l /proc/' + str(processorPID) + '/fd/ | wc -l', shell=True,
                                        stdout=subprocess.PIPE).communicate()
            tmp = out.splitlines()[0]
            handleNumber = max(handleNumber, tmp)
            processMemory = psutil.virtual_memory()
            totalMemory = processMemory.total
            freeMemory = processMemory.free
            usedPercent = processMemory.used
        else:
            try:
                sys.exit(0)
            except:
                print(
                    'total memory: %s GB; free memory: %s GB; memory use percent: %s, current process used percent: %s' % (
                        totalMemory, freeMemory, processMemory.used, p.memory_percent()))
                print('process max file handle: %s' % handleNumber)
                print('finished time: %s' % time.strftime('%Y-%m-%d %H:%M%S', time.localtime(time.time())))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        try:
            sys.exit(0)
        except:
            print(usage)
    monitorProcess(sys.argv[1])
