#!/usr/bin/python3
import ipdb
import sys
import time
import grammar
import re
line = sys._getframe
Break = ipdb.set_trace
def ColorDelete(s):
    return re.sub('\033\[\d+m', '', s)
def ColoredFillBlank(s, length):
    length += sum([len(i) for i in re.findall('\033\[\d+m', s)])
    return ('%-' + str(length) + 's ') % (s,)
class LLParser:
    def __init__(self, g: grammar.Grammar):
        table = {p.left: {t:set() for t in g.terminals} for p in g.productions}
        toolkit = grammar.Toolkit(g)
        self.g = g
        '''
        for v in g.variables:
            print(type(v), v, hash(v))
            '''
        for p in g.productions:
            for first in toolkit.First(p.right):
                table[p.left][first] |= {p}
            if toolkit.Nullable(p.right) == False:
                continue
            for follow in toolkit.Follow(p.left):
                table[p.left][follow] |= {p}
        print(table)
        self.table = table
        for v in self.table:
            for t in self.table[v]:
                if len(self.table[v][t]) >= 2:
                    print('Warn: This grammar is not LL(1) grammar')
                    print('self.table[{}][{}] = {}'.format(v, t, self.table[v][t]))
                    time.sleep(1)
    def __repr__(self):
        length = {c:0 for c in g.terminals}
        maxvlength = 0
        for v in self.table:
            maxvlength = max(maxvlength, len(re.sub('\033\[\d+m', '', str(v))))
            for c in self.table[v]:
                for p in self.table[v][c]:
                    length[c] = max(length[c], len(re.sub('\033\[\d+m', '', str(p))))
            #print(maxvlength, length)
        length = length
        maxvlength = maxvlength
        ret = ''
        for v in self.table:
            # Head
            ret += ' ' * maxvlength + ' '
            for c in self.table[v]:
                ret += ColoredFillBlank(str(c), length[c])
            ret += '\n'
            break
        for v in self.table:
            # body
            # color charactor occupied some of space.
            ret += ColoredFillBlank(str(v), maxvlength)
            for c in self.table[v]:
                for p in self.table[v][c]:
                    ret += ColoredFillBlank(str(p), length[c])
                if len(self.table[v][c]) == 0:
                    ret += ' ' * length[c] + ' '
            ret += '\n'
        return ret
    def MarkDown(self, filename):
        terminals = list(self.g.terminals)
        variables = list(self.g.variables)
        terminals.sort()
        variables.sort()
        f = open(filename, 'w')
        #Break()
        f.write('```\n')
        t = 'Grammar is:\n' + str(self.g) + '\n'
        t = ColorDelete(t)
        f.write(t)
        f.write('```\n')
        t = '| | ' + ' | '.join([str(v) for v in terminals]) + ' |\n'
        t = ColorDelete(t)
        f.write(t)
        t = '| - | ' + (' | '.join(['-'] * len(terminals)) + ' |\n')
        t = ColorDelete(t)
        f.write(t)
        for v in variables:
            f.write('| %s | ' % (v.RawStr()))
            #Break()
            for t in terminals:
                if self.table[v][t] == set():
                    t = ''
                else:
                    t = ColorDelete(str(','.join([i.RawStr() for i in self.table[v][t]])))
                    t = '`' + t + '`'
                f.write(t + ' | ')
            f.write('\n')
        f.close()
if __name__ == '__main__':
    g = grammar.Grammar(sys.argv[1])
    llp = LLParser(g)
    llp.MarkDown(g.filename + '.md')
