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
line = sys._getframe
class Stack:
    def __init__(self):
        self.stack = []
    def Top(self):
        return self.stack[-1]
    def __len__(self):
        return len(self.stack)
    def __repr__(self):
        return str(self.stack)
    def Push(self, s):
        if hasattr(s, '__iter__'):
            for i in range(len(s) - 1, -1, -1):
                k = s[i]
                self.stack.append(k)
        else:
            self.stack.append(s)
    def Pop(self, count = 1):
        if count < 0:
            ret = []
            for i in range(len(self.stack) - 1, -1, -1):
                ret.append(self.stack[i])
            self.stack = []
        else:
            ret = self.stack[-1]
            self.stack = self.stack[:-1]
        return ret
class CommandStack(Stack):
    def __init__(self):
        Stack.__init__(self)
    def Pop(self):
        top = self.stack[-1]
        ret = []
        while top[0] == self.stack[-1][0]:
            ret.append(self.stack.pop())
        return ret
class LLCompiler:
    def __init__(self, ll, source):
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
        self.parser = ll
        self.labels = {'IF': 0, 'IFN': 0, 'WHILE': 0}
        self.jump_tag = -1
        #print(type_words)
    def __repr__(self):
        return ' '.join([str(i[1]) for i in self.type_words[self.current:]])
    def IterInit(self):
        self.current = 0
    def PreOne(self):
        if self.current == -1:
            raise 'There is no pre one terminal'
        ret = self.type_words[self.current - 1]
        return (grammar.Terminal(ret[0]), ret[1])
    def LatterOne(self):
        if self.current + 1 >= len(self.type_words):
            raise 'There is no latter one terminal'
        ret = self.type_words[self.current + 1]
        return (grammar.Terminal(ret[0]), ret[1])
    def Lookahead(self):
        if self.current == len(self.type_words):
            return (grammar.Terminal('$'), '$')
        ret = self.type_words[self.current]
        return (grammar.Terminal(ret[0]), ret[1])
    def Next(self):
        if self.current == len(self.type_words):
            return (grammar.Terminal('$'), '$')
        ret = self.type_words[self.current]
        self.current += 1
        return (grammar.Terminal(ret[0]), ret[1])
    def JumpTagCreat(self):
        self.jump_tag += 1
        ret = 'jmp%d' % self.jump_tag
        return ret
    def JumpTag(self):
        ret = 'jmp%d' % self.jump_tag
        return ret
    def LabelCreat(self, label_type):
        label_type = label_type.upper()
        for s in ['IF', 'IFN', 'WHILE']:
            if s == label_type:
                self.last_label = s + str(self.labels[s])
                #print('New label:', self.last_label)
                self.labels[s] += 1
                return self.last_label
    def LastLabel(self):
        return self.last_label
    def CompilerModify(self):
        commands = self.commands
        modify = []
        start = Stack()
        i = 0
        while i < len(commands):
            cmd = commands[i]
            if cmd[-1] == ':':
                start.Push(i)
                i += 1
            elif cmd == 'back':
                top = start.Pop()
                modify += commands[top:i + 1]
                commands = commands[0:top] + commands[i + 1:]
                i = top
            else:
                i += 1
        self.commands = modify + commands
    def Parse(self):
        self.IterInit()
        stack = Stack()
        stack.Push(self.parser.g.start)
        commands = []
        inst = Stack()
        inst.Push('\n')
        top = Stack()
        top.Push(0)
        last = 1
        #Break()
        while True:
            lkh = self.Lookahead()
            print('\nparse:', [i[1] for i in self.type_words[self.current:]])
            print('Lookahead:', lkh)
            if stack.Top() == lkh[0]:
                self.Next()
                stack.Pop()
                print('stack info:', stack)
            elif type(stack.Top()) == grammar.Variable:
                v = stack.Pop()
                if len(self.parser.table[v][lkh[0]]) == 0:
                    print(self)
                    raise 'Compile failed'
                p = tuple(self.parser.table[v][lkh[0]])[0]
                if p in self.parser.g.opr:
                    for opr in self.parser.g.opr[p]:
                        opr = opr.split()
                        offset = int(opr[1])
                        opr = opr[2:]
                        t = ' '.join(opr)
                        if '-%t' in t:
                            # jump tag
                            t = t.replace('-%t', '%s')
                            t = t % self.JumpTagCreat()
                        if ':%t' in t:
                            t = t.replace('%t', '%s')
                            t = t % self.JumpTag()
                        for i, k in [('%w', 'while'), ('%i', 'if'), ('%n', 'ifn')]:
                            if i in t:
                                t = t.replace(i, '%s')
                                t = t % self.LabelCreat(k)
                                #print(t)
                        if '%l' in t:
                            t = t.replace('%l', '%s')
                            t = t % self.LastLabel()
                            #print(line().f_lineno, 'PreOne:', lkh, t)
                        if '%p' in t:
                            t = t.replace('%p', '%s')
                            lkh = self.PreOne()
                            #print(line().f_lineno, 'PreOne:', lkh, t)
                        if '%a' in t:
                            t = t.replace('%a', '%s')
                            lkh = self.LatterOne()
                            #print(line().f_lineno, ':', lkh, t)
                        if '%s' in t:
                            t = t % lkh[1]
                        inst.Push([t])
                        length = len(stack) + offset + 1
                        top.Push(length)
                stack.Push(p.right)
                print('use production:', p)
            else:
                print(self)
                raise 'Compile failed'
            #print('commands:', commands)
            #print('symbol  :', stack)
            #print('inst    :', inst)
            #print('top     :', top)
            #print('self    :', self)
            while top.Top() > len(stack):
                commands.append(inst.Pop())
                top.Pop()
            if len(stack) == 0:
                print('Accept')
                break
        self.commands = commands
        self.CompilerModify()
    def Commands(self):
        return self.commands
    def Save(self, target):
        f = open(target, 'wt')
        f.write('\n'.join(self.commands))
        f.close()
if __name__ == '__main__':
    g = grammar.Grammar(sys.argv[1])
    ll = llparsergen.LLParser(g)
    llc = LLCompiler(ll, sys.argv[2])
    llc.Parse()
    print('#', llc.Commands())
    if len(sys.argv) == 4:
        llc.Save(sys.argv[3])
