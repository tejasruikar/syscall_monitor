import os
import sys

def monitor_syscalls(application):
    pid = os.fork()
    if pid == 0:
        # Child process
        os.execl('/usr/bin/strace', 'strace', '-f', '-e', 'trace=all', '-o', '/tmp/strace.out', application)
    else:
        # Parent process
        try:
            os.waitpid(pid, 0)
        except KeyboardInterrupt:
            print('Exiting...')
            sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: {} <application>'.format(sys.argv[0]))
        sys.exit(1)
    monitor_syscalls(sys.argv[1])