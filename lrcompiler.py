#!/usr/bin/python3
import grammar
import llparsergen
import lalrparsergen
import lr1parsergen
import ipdb
import time
import sys
import re
Break = ipdb.set_trace
class LRCompiler(object):
    def __init__(self, lr, source):
        # c i { } t d f e l + - * / % > < g s n q o a ; = m ( ) , r
        reg = r'((?:\w+)|[/%-+()*;{<>,}]|(?:"(?:(?:\\.)|[^"])*")|(?:<=)|(?:>=)|(?:!=)|(?:=+)|-)'
        # For each keyword, we map a terminals.
        keyword_id = {
                'Func':'c',
                'Var':'v',
                'if': 'f',
                'else': 'e',
                'while':'l',
                '>=':'g',
                '<=':'s', 
                '!=': 'n',
                '==':'q',
                'or':'o',
                'and':'a',
                'return':'r',
            }
        # m: constant number or constant string
        terminals = {'/', '}', '+', '(', ')', '-', '*', ';', '{', '<', '>', ',', '=', '%'}
        id_keyword = {}
        for k in keyword_id:
            id_keyword[keyword_id[k]] = k
        type_words = []
        #split = re.findall(reg, 'Func Say(){print("wdnmd");print("wndmd");}')
        split = re.findall(reg, open(source).read())
        #print(split)
        for s in split:
            if s in keyword_id:
                type_words.append((keyword_id[s], s))
                continue
            elif s[0] == '"':
                type_words.append(('m', s))
                continue
            elif s in terminals:
                type_words.append((s, s))
                continue
            try:
                n = int(s)
                type_words.append(('m', n))
            except ValueError:
                type_words.append(('i', s))
        self.type_words = type_words
        self.id_keyword = id_keyword
        self.keyword_id = keyword_id
        self.parser = lr
        self.labels = {'IF': 0, 'IFN': 0, 'WHILE': 0}
        self.jump_tag = -1
        self.commands = []
        #print(type_words)

    def Commands(self):
        return self.commands

    def Save(self, target):
        f = open(target, 'wt')
        f.write('\n'.join(self.commands))
        f.close()

    def GenerateIcodeBy(self, reduced, p):
        if p not in self.parser.g.opr:
            return
        for opr in self.parser.g.opr[p]:
            opr = opr.split()
            offset = int(opr[1])
            opr = opr[2:]
            t = ' '.join(opr)
            if '%' in t:
                for i in range(len(p.right)):
                    t = t.replace('%' + str(i), str(reduced[i][2]))
            self.commands.append(t)

    def Reduce(self, stack, p):
        # reduce by production p
        reduced = []
        for i in range(len(p.right) - 1, -1, -1):
            if stack[-1][1] == p.right[i]:
                reduced.append(stack.pop())
            else:
                raise Exception("Parse error while reduce")
        self.GenerateIcodeBy(reduced, p)
        q = stack[-1][0]
        q = self.parser.goto[q][p.left[0]][1]
        # print('Reduce: push', (q, p.left[0]))
        stack.append((q, p.left[0]))

    def PrintInfo(self, index, stack, action):
        stack_strings = []
        for v in stack:
            if v[1] != None:
                stack_strings.append('{:<3}'.format(str(v[1]) + str(v[0])))
            else:
                stack_strings.append(f'{v[0]:<3}')
        cat_stack = ' '.join(stack_strings)
        cat_stack = lr1parsergen.ColorDelete(cat_stack)
        temp = [lr1parsergen.ColorDelete(str(v[1])) for v in self.type_words[index:]]
        string = ''.join(temp)
        self.PrintLine(cat_stack, string, action)

    def PrintLine(self, v1, v2, v3):
        print(f'{v1:20}   {v2:20}  {v3}')

    def Parse(self):
        stack = [(0, None)]
        print(stack)
        i = 0
        self.PrintLine('stack', 'remains', 'action')
        while True:
            tp, wd = '$', None
            if i < len(self.type_words):
                tp, wd = self.type_words[i]
            q = stack[-1][0]
            tp = grammar.Terminal(tp)
            if tp not in self.parser.action[q]:
                raise Exception("Cannot accept while read " + str(tp))
            action = self.parser.action[q][tp]
            self.PrintInfo(i, stack, action)
            if action[0] == 's':
                # shift
                # print('Parse: push', (action[1], tp, wd))
                stack.append((action[1], tp, wd))
                i += 1
            elif action[0] == 'r':
                # reduce
                self.Reduce(stack, action[1])
            elif action[0] == 'a':
                print('Accepted')
                break
            else:
                raise Exception("invalid action.")

if __name__ == '__main__':
    g = grammar.Grammar(sys.argv[1])
    parser = lr1parsergen.LRParser(g)
    lrc = LRCompiler(parser, sys.argv[2])
    lrc.Parse()
    print('#', lrc.Commands())
    if len(sys.argv) == 4:
        lrc.Save(sys.argv[3])
