# -*- coding: utf-8 -*-
# author: z1r0

import os
import sys
import subprocess
import re
import argparse

li = lambda x : print('\x1b[01;38;5;214m' + str(x) + '\x1b[0m')
ll = lambda x : print('\x1b[01;38;5;1m' + str(x) + '\x1b[0m')
lg = lambda x : print('\033[32m' + str(x) + '\033[0m')

crashs_id = []

parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-p', help='application', required=True)
parser.add_argument('-c', help='crashes folder', required=True)
parser.add_argument('-m', help='command')
parser.add_argument('-o', help='save result')
parser.add_argument('-v','--version', action='version', version='%(prog)s 1.0')
args = parser.parse_args()

program_path = args.p
crashs_path = args.c
command = args.m
write_file = args.o

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
        if command:
            for i in crashs_id:
                result = subprocess.run([program_path, command, crashs_path + i], capture_output=True, text=True)
                output = result.stderr.strip()
                asan_result.append(output)
        else:
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
        st = re.compile(r'SUMMARY: AddressSanitizer: stack-overflow.*')

        oom_match = oom.search(i)
        segv_match = segv.search(i)
        uaf_match = uaf.search(i)
        stack_overflow_match = stack_overflow.search(i)
        heap_overflow_match = heap_overflow.search(i)
        global_overflow_match = global_overflow.search(i)
        abort_match = abort.search(i)
        st_match = st.search(i)

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
        if st_match:
            summary.append(st_match.group(0))
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
    for key, value in result_dict.items():
        crashes_type = 'crashes_type: ' + value
        crashes_type_result = crashes_type + '\n' + '-' * len(crashes_type)

        crashes_id = 'crashes_id: ' + key
        crashes_id_result = '-' * len(crashes_type) + '\n' + crashes_id + '\n'

        ll(crashes_id_result)
        li(crashes_type_result)

if __name__ == '__main__':
    get_crashs_id()
    lg('[+] Get crashes done!')
    get_result()
    lg('[+] Get asan_result done!')
    filter_data_type(asan_result)
    lg('[+] filter done!')
    to_integrate()
    show()
