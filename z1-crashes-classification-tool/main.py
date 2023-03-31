# -*- coding: utf-8 -*-
# author: z1r0

import os
import sys
import subprocess
import re

li = lambda x : print('\x1b[01;38;5;214m' + str(x) + '\x1b[0m')
ll = lambda x : print('\x1b[01;38;5;1m' + str(x) + '\x1b[0m')

crashs_id = []

if len(sys.argv) < 2:
    ll('please input program_path')
    sys.exit(1)
program_path = sys.argv[1]

if len(sys.argv) < 3:
    ll('please input crashs_path')
    sys.exit(1)
crashs_path = sys.argv[2]

if len(sys.argv) < 4:
    ll('please input write_file')
    sys.exit(1)
write_file = sys.argv[3]

asan_result = []
summary = []
summary_sort = []

final = {
}

result_dict = {}

def get_crashs_id():
    global crashs_path
    try:
        if crashs_path[-1:] == '/':
            pass
        else:
            crashs_path += '/';
        result = subprocess.run(['ls', crashs_path], capture_output=True, text=True)
        output_lines = result.stdout.strip().split('\n')

        for line in output_lines:
            if "id" in line:
                first_line = line
                crashs_id.append(first_line)

    except subprocess.CalledProcessError as err:
        li(err)

def get_result():
    try:
        for i in crashs_id:
            result = subprocess.run([program_path, crashs_path + i], capture_output=True, text=True)
            output = result.stderr.strip()
            asan_result.append(output)
    except subprocess.CalledProcessError as err:
        li(error)

def filter_data_type(data):
    for i in data:
        oom = re.compile(r'SUMMARY: AddressSanitizer: out-of-memory.*')
        segv = re.compile(r'SUMMARY: AddressSanitizer: SEGV.*')
        uaf = re.compile(r'SUMMARY: AddressSanitizer: heap-use-after-free.*')
        stack_overflow = re.compile(r'SUMMARY: AddressSanitizer: stack-buffer-overflow.*')
        heap_overflow = re.compile(r'SUMMARY: AddressSanitizer: heap-buffer-overflow.*')
        global_overflow = re.compile(r'SUMMARY: AddressSanitizer: global-buffer-overflow.*')
        abort = re.compile(r'AddressSanitizer: nested bug in the same thread, aborting.*')

        oom_match = oom.search(i)
        segv_match = segv.search(i)
        uaf_match = uaf.search(i)
        stack_overflow_match = stack_overflow.search(i)
        heap_overflow_match = heap_overflow.search(i)
        global_overflow_match = global_overflow.search(i)
        abort_match = abort.search(i)

        if oom_match:
            summary.append(oom_match.group(0))
            continue
        if segv_match:
            summary.append(segv_match.group(0))
            continue
        if uaf_match:
            summary.append(uaf_match.group(0))
            continue
        if stack_overflow_match:
            summary.append(stack_overflow_match.group(0))
            continue
        if heap_overflow_match:
            summary.append(heap_overflow_match.group(0))
            continue
        if global_overflow_match:
            summary.append(global_overflow_match.group(0))
            continue
        if abort_match:
            summary.append(abort_match.group(0))
            continue
        summary.append(i)

def to_integrate():
    for i in range(len(crashs_id)):
        final.update({crashs_id[i] : summary[i]})
    seen_values = set()
    for key, value in final.items():
        if value not in seen_values:
            result_dict[key] = value
            seen_values.add(value)

def show():
    with open(write_file, 'w') as f:
        for key, value in result_dict.items():
            crashes_type = 'crashes_type: ' + value
            crashes_type_result = crashes_type + '\n' + '-' * len(crashes_type)

            crashes_id = 'crashes_id: ' + key
            crashes_id_result = '-' * len(crashes_type) + '\n' + crashes_id + '\n'

            ll(crashes_id_result)
            li(crashes_type_result)
            f.write(crashes_id_result)
            f.write(crashes_type_result)
    f.close()

if __name__ == '__main__':
    get_crashs_id()
    get_result()
    filter_data_type(asan_result)
    to_integrate()
    show()
