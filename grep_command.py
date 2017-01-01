#!/usr/bin/env python3
import subprocess
def grep_command(command,grepopts):
    #http://stackoverflow.com/questions/6780035/python-how-to-run-ps-cax-grep-something-in-python
    p1 = subprocess.Popen(command.split(' '),stdout=subprocess.PIPE)
    p2 = subprocess.Popen(command.split('grep {}'.format(grepopts)),stdin=p1.stdout,stdout=subprocess.PIPE)
    p1.stdout.close()# Allow p1 to receive a SIGPIPE if p2 exits.
    return p2.communicate()[0].decode('utf-8')
    #Using shell=True can be dangerous.
