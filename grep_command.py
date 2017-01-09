#!/usr/bin/env python
import subprocess
def grep_command(command,grepopts):
    #http://stackoverflow.com/questions/6780035/python-how-to-run-ps-cax-grep-something-in-python
    p1 = subprocess.Popen(command.split(' '),stdout=subprocess.PIPE)
    p2 = subprocess.Popen('grep {}'.format(grepopts).split(' '),stdin=p1.stdout,stdout=subprocess.PIPE)
    p1.stdout.close()# Allow p1 to receive a SIGPIPE if p2 exits.
    return p2.communicate()[0].decode('utf-8')
    #Using shell=True can be dangerous.

if __name__ == '__main__':
    print grep_command('ls -la','p')
