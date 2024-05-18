#!/usr/bin/python3
import ipdb
import re
import sys
labels = {'main':[]}
exit_val = 0
def ProgExit(val):
    exit_val = val
functions = {}
jumps = {'main':{}}
# 'function_name': codes
label_id = 'main'
cmd_pos = 0
def Nothing():
    pass
# mode are F, T, B, means false, true, break
debug = 'T'
Break = ipdb.set_trace if debug == 'B' else Nothing
reg = r'((?:"(?:(?:\\.)|[^"])*")|\d+|(?::{0,1}\w+:{0,1}))'
for line in open(sys.argv[1]).read().split('\n'):
    cmd = re.findall(reg, line)
    #print(cmd)
    if len(cmd) == 0:
        continue
    if cmd[0][-1] == ':':
        # label
        label_id = cmd[0][:-1]
        labels[label_id] = []
        cmd_pos = 0
    elif cmd[0][0] == ':':
        # jump tag
        if label_id not in jumps:
            jumps[label_id] = {}
        jumps[label_id][cmd[0][1:]] = cmd_pos
    elif cmd[0] == 'func':
        func_name = cmd[1][:-1]
        functions[func_name] = None
        label_id = func_name
        labels[label_id] = []
        cmd_pos = 0
    elif 'back' in cmd[0]:
        labels[label_id].append(cmd)
        label_id = 'main'
        cmd_pos = 0
    else:
        labels[label_id].append(cmd)
        cmd_pos += 1
if debug == 'T':
    print('functions:', functions)
    print('labels   :', labels)
    print('jumps    :', jumps)
tmp_stack = [None, None]
prog_stack = [{}]
label_stack = [['main', 0]]
ret = None
class Spliter:
    def __init__(self):
        pass
    def __repr__(self):
        return '|'
while True:
    cmd = labels[label_stack[-1][0]][label_stack[-1][1]]
    if debug == 'T':
        print('label_stack :', label_stack)
        print('prog_stack  :', prog_stack)
        print('tmp_stack   :', tmp_stack)
        print(cmd)
        print()
    label_stack[-1][1] += 1
    T0 = tmp_stack[-1]
    T1 = tmp_stack[-2]
    if cmd[0] == 'exit':
        Break()
        break
    elif cmd[0] == 'va_split':
        Break()
        tmp_stack.append(Spliter())
    elif cmd[0] == 'pop':
        Break()
        if len(cmd) == 2:
            prog_stack[-1][cmd[1]] = T0
        tmp_stack.pop()
    elif cmd[0] == 'alc':
        Break()
        prog_stack[-1][cmd[1]] = None
    elif cmd[0] == 'ret':
        Break()
        ret = T0
        while type(tmp_stack[-1]) != Spliter:
            tmp_stack.pop()
        while type(label_stack[-1]) != Spliter:
            label_stack.pop()
        while type(prog_stack[-1]) != Spliter:
            prog_stack.pop()
        tmp_stack[-1] = ret
        label_stack.pop()
        prog_stack.pop()
        # TODO: give ret back to stack.
    elif cmd[0] == 'func_back':
        Break()
        while type(tmp_stack[-1]) != Spliter:
            tmp_stack.pop()
        while type(label_stack[-1]) != Spliter:
            label_stack.pop()
        while type(prog_stack[-1]) != Spliter:
            prog_stack.pop()
        tmp_stack[-1] = None
        label_stack.pop()
        prog_stack.pop()
    elif cmd[0] == 'if':
        Break()
        if bool(T0):
            label_id = cmd[1]
            label_stack.append([label_id, 0])
    elif cmd[0] == 'ifn':
        Break()
        if not bool(T0):
            label_id = cmd[1]
            label_stack.append([label_id, 0])
    elif cmd[0] == 'while':
        Break()
        if bool(T0):
            label_id = cmd[1]
            label_stack.append([label_id, 0])
    elif cmd[0] == 'while_if':
        Break()
        if bool(T0):
            label_id = label_stack[-1][0]
            jump_to = jumps[label_id][cmd[1]]
            label_stack[-1][1] = jump_to
            tmp_stack.pop()
            # TODO: JUMP
    elif cmd[0] == 'push':
        Break()
        if cmd[1].isdigit():
            tmp_stack.append(int(cmd[1]))
        elif cmd[1][0] == '"':
            tmp_stack.append(eval(cmd[1]))
        else:
            tmp_stack.append(prog_stack[-1][cmd[1]])
    elif cmd[0] == 'back':
        Break()
        label_stack.pop()
    elif cmd[0] == 'and':
        Break()
        tmp_stack.pop()
        T1 = bool(T1 and T0)
        tmp_stack[-1] = int(T1)
    elif cmd[0] == 'or':
        Break()
        tmp_stack.pop()
        T1 = bool(T1 or T0)
        tmp_stack[-1] = int(T1)
    elif cmd[0] == 'lt':
        Break()
        tmp_stack.pop()
        tmp_stack[-1] = int(T1 < T0)
    elif cmd[0] == 'gt':
        Break()
        tmp_stack.pop()
        tmp_stack[-1] = int(T1 > T0)
    elif cmd[0] == 'ge':
        Break()
        tmp_stack.pop()
        tmp_stack[-1] = int(T1 >= T0)
    elif cmd[0] == 'le':
        Break()
        tmp_stack.pop()
        tmp_stack[-1] = int(T1 <= T0)
    elif cmd[0] == 'eq':
        Break()
        tmp_stack.pop()
        tmp_stack[-1] = int(T1 == T0)
    elif cmd[0] == 'ne':
        Break()
        tmp_stack.pop()
        tmp_stack[-1] = int(T1 != T0)
    elif cmd[0] == 'add':
        Break()
        tmp_stack.pop()
        T1 = T1 + T0
        tmp_stack[-1] = T1
    elif cmd[0] == 'min':
        Break()
        tmp_stack.pop()
        T1 = T1 - T0
        tmp_stack[-1] = T1
    elif cmd[0] == 'mul':
        Break()
        tmp_stack.pop()
        T1 = T1 * T0
        tmp_stack[-1] = T1
    elif cmd[0] == 'div':
        Break()
        tmp_stack.pop()
        T1 = T1 // T0
        tmp_stack[-1] = T1
    elif cmd[0] == 'mod':
        Break()
        tmp_stack.pop()
        T1 = T1 % T0
        tmp_stack[-1] = T1
    elif cmd[0] == 'neg':
        Break()
        tmp_stack[-1] = -tmp_stack[-1]
    elif cmd[0] == 'call':
        Break()
        if cmd[1] == 'print':
            ret = print(T0, end = '\n' if debug == 'T' else '')
            while type(tmp_stack[-1]) != Spliter:
                tmp_stack.pop()
            tmp_stack[-1] = ret
        elif cmd[1] == 'exit':
            exit_val = T0
            break
        else:
            label_stack.append(Spliter())
            label_stack.append([cmd[1], 0])
            prog_stack.append(Spliter())
            prog_stack.append({})
    elif cmd[0] == 'jmp':
        Break()
        # TODO jump instruction
    else:
        print('Unknow instruction:', cmd)
        exit(0)
print('program exit:', exit_val)
print('label_stack :', label_stack)
print('prog_stack  :', prog_stack)
print('tmp_stack   :', tmp_stack)
