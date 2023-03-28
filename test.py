from subprocess import Popen, PIPE
import pandas as pd

def run_bpftrace(command):
    # Run bpftrace script and collect output
    process = Popen(['bpftrace', '-e', command], stdout=PIPE)
    output = process.communicate()[0].decode('utf-8')

    # Parse output into a DataFrame
    data = []
    for line in output.split('\n'):
        if not line:
            continue
        syscall, count = line.split()
        data.append({'syscall': syscall, 'count': int(count)})
    return pd.DataFrame(data)
app_name = "bpftrace"
# Run multiple bpftrace commands
df1 = run_bpftrace('tracepoint:syscalls:sys_enter_* { @[probe] = count(); }')
df2 = run_bpftrace('tracepoint:syscalls:sys_enter_open { @[comm] = count(); }')
df3 = run_bpftrace('tracepoint:syscalls:sys_enter_execve { printf("%s %d\n", comm, pid); }')
df4 = run_bpftrace('tracepoint:syscalls:sys_enter_read { @[kstack] = count(); }')
df5 = run_bpftrace('tracepoint:syscalls:sys_enter_write { @[ustack] = count(); }')

df = run_bpftrace(f'tracepoint:syscalls:sys_enter_* /comm == "{app_name}"/ {{ @[probe] = count(); }}')

# Perform advanced data analysis on the DataFrame using pandas
df['syscall'] = df['syscall'].str.replace('tracepoint:syscalls:sys_enter_', '')
df['percentage'] = df['count'] / df['count'].sum() * 100
df = df.sort_values('count', ascending=False)
