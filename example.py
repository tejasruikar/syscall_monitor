import subprocess
import os
import shlex
import json
import streamlit as st
import pandas as pd
from io import StringIO
asdf = None
SCRIPT = "tracepoint:raw_syscalls:sys_enter { @[comm] = count(); } interval:s:5 { print(@); clear(@); }"
SCRIPT_FILEOPENS = "bpftrace -e 'tracepoint:syscalls:sys_enter_open { printf("%s %s\n", comm, str(args->filename)) }'"

def process_request()

def exec(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

def execute_and_listen_for_updates():
    dropdown = set()
    key1 = 0
    st.title("Real-time syscalls counter")
    option = st.empty()
    table_placeholder = st.empty()
    total_placeholder = st.empty()

    


    try:
        command = shlex.split("bpftrace -f json -e '{}'".format(SCRIPT))
        for entry in exec(command):
            entry = json.loads(entry)
            print(entry)
            if entry["type"] == "map":
                data_dict = entry["data"]["@"]
                proc_names, counts = [], []
                total = 0
                for k, v in data_dict.items():
                    proc_names.append(k)
                    dropdown.add(k)
                    counts.append(v) 
                    total += v

                df = pd.DataFrame(
                    {"counts": counts},
                    index=proc_names
                )
                key1 = key1 + 1
                asdf = option.selectbox("Apps", (dropdown), key=key1, on_change=dropdown_changed())
                table_placeholder.table(df)
                total_placeholder.text("total system calls: " + str(total))

    except Exception as e:
        print('internal error:', e)
        os._exit(0)

def dropdown_changed():
    if asdf:
        print("yes")

if __name__ == "__main__":
    asdf = None
    execute_and_listen_for_updates()