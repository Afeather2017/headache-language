#!/usr/bin/python3
import ipdb
import sys
import grammar
import re
import time
def ColorDelete(s):
    return re.sub('\033\[\d+m', '', s)
line = sys._getframe
Break = ipdb.set_trace
class Production(grammar.Production):
    def __init__(self, left, right, lookahead, current = 0):
        grammar.Production.__init__(self, left, right)
        self.current = current
        self.lookahead = lookahead
    def __repr__(self):
        ret = ''
        for left in self.left:
            ret += str(left)
        ret += '\033[32m->\033[0m'
        for i in range(0, self.current):
            ret += str(self.right[i])
        ret += '\033[45m.\033[0m'
        for i in range(self.current, len(self.right)):
            ret += str(self.right[i])
        if len(self.right) == 0:
            ret += "\033[34m''\033[0m"
        ret += ': ' + str(self.lookahead)
        return ret
    def Production(self):
        ret = ''
        for left in self.left:
            ret += str(left)
        ret += '\033[32m->\033[0m'
        for i in range(0, self.current):
            ret += str(self.right[i])
        ret += '\033[45m.\033[0m'
        for i in range(self.current, len(self.right)):
            ret += str(self.right[i])
        if len(self.right) == 0:
            ret += "\033[34m''\033[0m"
        return ret
    def Dump(self):
        return Production(self.left, self.right, self.lookahead, self.current + 1)
    def Next(self):
        if len(self.right) == self.current:
            return None
        return Production(self.left, self.right, self.current + 1)
    def Split(self):
        # print('Split:', self, len(self.left), len(self.right), self.current)
        if self.current == len(self.right):
            return (self.left, self.right[:self.current], None, None, self.lookahead)
        return (self.left, self.right[:self.current], self.right[self.current],
                self.right[self.current + 1:], self.lookahead)
    def End(self):
        return self.current == len(self.right)
    def __hash__(self):
        # print('Production:Hash:', str(self))
        return hash(str(self))
    def __eq__(self, a):
        return str(self) == str(a)
class Item:
    def __init__(self, I, hash_with_char = True):
        self.item = I
        self.hash_with_char = hash_with_char
    def __hash__(self):
        return hash(str(self))
    def __eq__(self, a):
        return str(self) == str(a)
    def __iter__(self):
        return self.item.__iter__()
    def __next__(self):
        return self.item.__next__()
    def __repr__(self):
        t = [str(i) for i in self.item]
        t = ', '.join(t)
        return '{' + t + '}'
    def Print(self):
        t = {}
        for i in self.item:
            k = i.Production()
            if k not in t:
                t[k] = []
            t[k].append(str(i.lookahead))
        for i in t:
            t[i].sort()
            t[i] = ''.join(t[i])
        w = []
        for k, v in t.items():
            w.append(str(k) + ': ' + v)
        w.sort()
        print('Item: {' + ', '.join(w) + '}\n')
    def __len__(self):
        return len(self.item)
class LRParser:
    def Goto(self, I, X):
        J = set()
        # print(sys._getframe().f_lineno, 'LRParser.Goto:', I)
        for k in I:
            if len(k.right) == 0:
                continue
            (A, alpha, v, beta, lookahead) = k.Split()
            # print(line().f_lineno, 'X:', X)
            if v == X:
                k = k.Dump()
                J |= {k}
        # print(sys._getframe().f_lineno, 'LRParser.Goto:', I)
        return self.Closure(J)
    def Closure(self, I):
        t = set()
        # print('Closure for:', I)
        while True:
            t = set()
            for k in I:
                A, alpha, X, beta, lookahead = k.Split()
                if X == None:
                    continue
                if type(X) == grammar.Terminal:
                    continue
                X = grammar.ProductionString([X])
                for p in self.g.Group(X):
                    first = self.toolkit.First(beta +
                            grammar.ProductionString([lookahead]))
                    for w in first:
                        #print('Closure1', I)
                        k = Production(X, p.right, w)
                        if k not in I:
                            t |= {k}
                        #print('Closure2')
            if t == set():
                break
            I |= t
        # print('is:', end = ' ')
        # Item(I).Print()
        return I
    def TableCreat(self):
        '''
        for each item I:
            for each production matches 'A->[anystring].' with lookahead set s:
                creat reduce (I, s, 'A->[anystring]')
        but only the kernels has the matched production
        '''
        '''
        action:               terminals
        state(kernel_id) (reduce, production)
                       or
        state(kernel_id) (shift,       state)
        '''
        action = {kid: {} for kid in range(len(self.T))}
        '''
        goto: variables
        state   state
        '''
        goto = {kid: {} for kid in range(len(self.T))}
        for item_id in range(len(self.T)):
            # item: {production with shift, ...}
            item = self.T[item_id]
            for psl in item:
                # psl: production with shift and lookahead
                if psl == self.accept:
                    action[item_id][self.end] = ('a', None)
                    continue
                if psl.End() == False:
                    continue
                if psl.lookahead in action[item_id].items():
                    raise Exception('This grammar is not LR(1) cuz' +
                                    f'{psl.lookahead} not in {action[item_id]}')
                    #type_info = [f'lookahead type: {type(psl.lookahead)}',
                    #             'action[item_id]:']
                    #for k, v in action[item_id]:
                    #    type_info.append(f'{k} {type(k)}: {v} {type(v)}')
                    #raise Exception('This grammar is not LR(1) cuz' +
                    #                f'{psl.lookahead} not in {action[item_id]}'
                    #                + 'type_info:\n' + '\n'.join(type_info))
                p = grammar.Production(psl.left, psl.right)
                action[item_id][psl.lookahead] = ('r', p)
        for item_id in range(len(self.T)):
            # item: {production with shift, ...}
            for i in self.map[item_id]:
                v = self.map[item_id][i]
                if type(v) == grammar.Terminal:
                    action[item_id][v] = ('s', i)
                else:
                    goto[item_id][v] = ('g', i)
        print(line().f_lineno, 'action:', action)
        print(line().f_lineno, 'goto:', goto)
        self.action = action
        self.goto = goto
    def MarkDown(self, output):
        action = self.action
        goto = self.goto
        f = open(output, 'wt')
        terminals = list(self.g.terminals)
        variables = list(self.g.variables)
        terminals.sort()
        variables.sort()
        head = terminals + [self.end] + variables
        #Break()
        f.write('```\n')
        t = 'Grammar is:\n' + str(self.g) + '\n'
        t = ColorDelete(t)
        f.write(t)
        f.write('```\n')
        t = '| | ' + ' | '.join([str(v) for v in head]) + ' |\n'
        t = ColorDelete(t)
        f.write(t)
        t = '| - | ' + (' | '.join(['-'] * len(head)) + ' |\n')
        t = ColorDelete(t)
        f.write(t)
        for item_id in range(len(self.T)):
            f.write('| %s | ' % item_id)
            #Break()
            for v in head:
                t = ''
                if type(v) == grammar.Terminal:
                    if v in action[item_id]:
                        t = str(action[item_id][v])
                else: # variables
                    if v in goto[item_id]:
                        t = str(goto[item_id][v])
                t = ColorDelete(t)
                t = t[1:-1].replace(',', '').replace("'", '')
                f.write(t + ' | ')
            f.write('\n')
        f.close()
    def __init__(self, g: grammar.Grammar):
        # Creat frist variable.
        self.start = grammar.Variable('_')
        self.end = grammar.Terminal('$')
        left = grammar.ProductionString([self.start])
        right = grammar.ProductionString([g.start, self.end])
        # Add the first variable
        g.productions |= {grammar.Production(left, right)}
        self.g = g
        self.accept = Production(left, right, self.end, len(right))
        self.toolkit = grammar.Toolkit(g)
        # creat the dots.
        p = Production(left, right, self.end)
        print(p)
        p = self.Closure({p})
        p = Item(p)
        current = 1
        T = [p]
        # print('LRParser.init: p =', p, hash(p))
        self.index = {T[0]: 0}
        # To represent a graph.
        # map = { point: {to b: with a, }, }, }
        self.map = {0: {}}
        while True:
            J = None
            print('gen fa', time.time())
            for i in range(len(T)):
                #Break()
                if i not in self.map:
                    self.map[i] = {}
                for k in T[i]:
                    # print('T[' + str(i) + ']:', k)
                    A, alpha, X, beta, lookahead = k.Split()
                    if X == None:
                        continue
                    t = Item(self.Goto(T[i], X))
                    if t not in self.index:
                        J = t
                        self.index[J] = current
                        '''
                        print(line().f_lineno, 'LRParser.init: T =', T)
                        print(line().f_lineno, 'LRParser.init.index:', self.index)
                        print(line().f_lineno, 'LRParser.init.T[' + str(i) + ']:',
                                type(T[i]), T[i], hash(T[i]))
                        '''
                        index = self.index[T[i]]
                        self.map[index] |= {current: X}
                        T.append(J)
                        current += 1
                    else:
                        index = self.index[T[i]]
                        if index not in self.map:
                            self.map[index] = {}
                        # the fix: self.map[index] |= {index: X}
                        #          this always create a self edge.
                        self.map[index] |= {self.index[t]: X}
                    # print(line().f_lineno, 'T:', T)
            # print(line().f_lineno, J)
            # print(line().f_lineno, 'LRParser.init: T =', T)
            if J == None:
                break
        print('gen fa done at', time.time())
        self.T = T
        print('T:')
        for i, v in enumerate(self.T):
            print(i, len(v), v)
        print('index:')
        for k, v in self.index.items():
            print(f'{v}: {k}')
        print('map:')
        for k, v in self.map.items():
            print(k, v)
        # TODO: Generate shift, goto and reduce form.
        # For the case of shift/recuce conflict, raise error.
        self.TableCreat()
        self.MarkDown(g.filename + '.md')
        self.Draw(g.filename + '.dot')

    def Draw(self, filename):
        if filename == None:
            f = sys.stdout
        else:
            f = open(filename, 'wt')
        print('digraph G {', file=f)
        def PrintNodes(T):
            for i, n in enumerate(T):
                s = []
                for p in n:
                    s.append(ColorDelete(str(p)))
                s = '\\n'.join(s)
                print(f'  {i} [shape=box,label="I{i}\\n{s}"];', file=f)
        def PrintEdges(m):
            for u, k in m.items():
                for v, e in k.items():
                    e = ColorDelete(str(e))
                    print(f'  {u} -> {v} [label="{e}"];', file=f)
        PrintNodes(self.T)
        PrintEdges(self.map)
        print('}', file=f)
        f.close()

if __name__ == '__main__':
    g = grammar.Grammar(sys.argv[1])
    LRParser(g)
