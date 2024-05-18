#!/usr/bin/python3
import queue
import ipdb
import sys
line = sys._getframe
Break = ipdb.set_trace
class Terminal:
    def __init__(self, c: str):
        self.charactor = c
        # print('Terminal', c)
    def __repr__(self):
        return self.charactor
    def __hash__(self):
        return hash(str(self))
    def __lt__(self, a):
        return str(self) < str(a)
    def __eq__(self, a):
        if type(a) != Terminal:
            return False
        return str(a) == str(self)
    def RawStr(self):
        return self.charactor
class Variable:
    def __init__(self, c: str):
        self.charactor = c
        # print('Variable', c)
    def RawStr(self):
        return self.charactor
    def __repr__(self):
        if len(self.charactor) == 1:
            return '\033[31m' + self.charactor + '\033[0m'
        else:
            return '\033[31m<' + self.charactor + '>\033[0m'
    def __hash__(self):
        return hash(str(self))
    def __lt__(self, a):
        return str(self) < str(a)
    def __eq__(self, a):
        if type(a) == Terminal:
            return False
        return str(a) == str(self)
class ProductionString:
    def __init__(self, string: list):
        self.string = tuple(string)
        self.terminal_count = 0
        self.variable_count = 0
        q = 'S'
        delta = {
                'S': {Variable: 'L', Terminal: 'R'},
                'R': {Variable: 'A', Terminal: 'R'},
                'A': {Variable: 'N', Terminal: 'N'},
                'N': {Variable: 'N', Terminal: 'N'},
                'L': {Variable: 'N', Terminal: 'L'},
                }
        for v in self.string:
            q = delta[q][type(v)]
            if type(v) == Terminal:
                self.terminal_count += 1
            else:
                self.variable_count += 1
        if q == 'A' or q == 'L':
            self.type = 'RG'
        else:
            self.type = 'CFG'
    def Info(self):
        return '{} with {} terminals and {} variables'.format(
                self.string, self.terminal_count, self.variable_count)
    def RawStr(self):
        ret = ''
        for i in self.string:
            ret += i.RawStr()
        return ret
    def __repr__(self):
        ret = ''
        for i in self.string:
            ret += str(i)
        return ret
    def __iter__(self):
        return iter(self.string)
    def __next__(self):
        return next(self.string)
    def __hash__(self):
        # print('ProductionString, hash:', hash(str(self)))
        return hash(str(self))
    def __getitem__(self, item):
        if type(item) == slice:
            return ProductionString(self.string[item])
        else:
            return self.string[item]
    def __add__(self, a):
        return ProductionString(self.string + a.string)
    def __len__(self):
        return len(self.string)
    def __eq__(self, a):
        # print('ProductionString, eq:', self, a, str(self) == str(a))
        # print('ProductionString, eq:', self, a, hash(self) == hash(a))
        return str(self) == str(a)
class Production:
    def __init__(self, left: list, right: list):
        self.left = ProductionString(left)
        self.right = ProductionString(right)
    def __repr__(self):
        ret = ''
        for left in self.left:
            ret += str(left)
        ret += '\033[32m->\033[0m'
        for right in self.right:
            ret += str(right)
        if len(self.right) == 0:
            ret += "\033[34m''\033[0m"
        return ret
    '''
    def __lt__(self, a):
        if self.right.variable_count == 0 and a.right.variable_count != 0:
            return True
        else:
            return False
            '''
    def RawStr(self):
        return self.left.RawStr() + '->' + self.right.RawStr()
    def __lt__(self, a):
        return str(self) < str(a)
    def __hash__(self):
        return hash(str(self))
    def __eq__(self, rhs):
        if type(rhs) != type(self):
            return False
        return self.left == rhs.left and self.right == rhs.right
class ProductionFilter:
    def __init__(self, productions):
        self.filter = {}
        for p in productions:
            if p.left not in self.filter:
                self.filter[p.left] = []
            self.filter[p.left].append(p)
        # print('ProductionFilter:', self.filter)
    def __repr__(self):
        ret = ''
        for p in self.filter:
            ret += str(p) + ': {'
            for k in self.filter[p]:
                ret += str(k) + ', '
            if len(self.filter[p]) >= 1:
                ret = ret[:-2]
            ret += '},\n'
        return ret
    def __getitem__(self, left):
        return self.filter[left]
class Grammar:
    def __init__(self, s: str):
        #Break()
        self.filename = s
        f = open(s, 'r')
        # First line: terminals
        terminals = set()
        for t in f.readline().split():
            if len(t) != 1:
                raise 'Terminal is not single charactor'
            terminals |= {Terminal(t)}
        # Second line: variables
        variables = set()
        for v in f.readline().split():
            variables |= {Variable(v)}
        # Third line: Start symbol
        # print('Construct terminals and variables', terminals, variables)
        start = Variable(f.readline().replace('\n', ''))
        # After that: productions
        # Format: left -> variable 'terminals'
        # And the first line is the start symbol
        productions = set()
        grammar_type = 3
        last = None
        opr = {}
        for p in f.read().split('\n'):
            if len(p) == 0:
                continue
            if p[0] == '#':
                # Operate
                if last != None:
                    if last not in opr:
                        opr[last] = []
                    opr[last].append(p)
                continue
            if p[0] == '##':
                # comment, skip
                continue
            state = 'l'
            left = []
            right = []
            for v in p.split():
                if state == 'l':
                    if v[0] == "'":
                        # Terminals
                        for t in v[1:-1]:
                            left.append(Terminal(t))
                    elif v == '->':
                        state = 'r'
                    else:
                        left.append(Variable(v))
                else: # state == 'r'
                    if v[0] == "'":
                        # Terminals
                        for t in v[1:-1]:
                            right.append(Terminal(t))
                    else:
                        right.append(Variable(v))
            # RG  3
            # CFG 2
            # CSG 1
            # PSG 0
            if len(left) != 1 and grammar_type >= 2:
                grammar_type = 1
            p = Production(left, right)
            last = p
            if p.right.type == 'CFG' and grammar_type == 3:
                grammar_type = 2
            productions |= {p}
        self.terminals = terminals
        self.productions = productions
        self.variables = variables
        self.start = start
        self.grammar_type = ['PSG', 'CSG', 'CFG', 'RG'][grammar_type]
        self.group = None
        self.opr = opr
        if __name__ == '__main__':
            print(line().f_lineno, 'operate for grammar:', opr)
    def __repr__(self):
        return '{}:(V {} = {},\nT {} = {},\nP {} = {},\nS = {})\n'.format(self.grammar_type,
                len(self.variables), self.variables, len(self.terminals), self.terminals,
                len(self.productions), self.productions, self.start)
    def _Product(self, s, variable_count, productions, times):
        # print(s, 'with', variable_count, 'variables and could derive', times)
        if variable_count == 0:
            self.result |= {str(s)}
            return
        if times == 0:
            return
        for i in range(len(s)):
            if type(s[i]) == Terminal:
                continue
            # For some of production that is 'aA->terminals and variables'
            # we will delete some string in s. For example:
            # s = 'aA' and production is 'aA->Aa'
            # then s converse to Aa
            # So edge checking is necessary.
            for p in productions[s[i]]:
                self._Product(s[:i] + p.right + s[i + 1:],
                        variable_count + p.right.variable_count - 1,
                        productions, times - 1)
            # TODO:Using TireTree to support PSG and CSG.
    def _GroupCreat(self):
        if self.grammar_type != 'CFG' and self.grammar_type != 'RG':
            raise 'Unsupported grammar!'
        self.group = ProductionFilter(self.productions)
    def Group(self, production):
        if self.group == None:
            self._GroupCreat()
        if type(production) == ProductionString:
            return self.group[production]
        return self.group[production.left]
    def Product(self, times = 5):
        if __name__ == '__main__':
            print('Production set:', self.productions)
        '''
        for p in self.productions:
            print(p.left.Info(), p.right.Info())
            '''
        if self.grammar_type != 'CFG' and self.grammar_type != 'RG':
            raise 'Unsupported grammar!'
        productions = ProductionFilter(self.productions)
        self.result = set()
        if __name__ == '__main__':
            print('Grouped Production:', productions)
        for p in productions[self.start]:
            self._Product(p.right, p.right.variable_count, productions, times - 1)
        ret = self.result
        return ret
class Toolkit:
    def __init__(self, g: Grammar):
        self.first = {}
        self.follow = {}
        self.nullable = {}
        self.grammar = g
        print(g)
        self._Nullable(g)
        print('Nullable:', self.nullable)
        self._First(g)
        print('First:')
        for v, t in self.first.items():
            print('{}: {}'.format(v, t))
        self._Follow(g)
        print('Follow:')
        for v, t in self.follow.items():
            print('{}: {}'.format(v, t))
    def _First(self, g):
        q = {}
        for p in g.productions:
            self.first[p.left] = set()
            q[p.left] = set()
        for p in g.productions:
            if len(p.right) > 0 and type(p.right[0]) == Terminal:
                self.first[p.left] |= {p.right[0]}
        for p in g.productions:
            if len(p.right) == 0:
                continue
            for r in p.right:
                if type(r) == Terminal:
                    self.first[p.left] |= {r}
                    break
                if self.nullable[r] == False:
                    q[p.left] |= {r}
                    break
                q[p.left] |= {r}
        changed = True
        while changed == True:
            changed = False
            for u in q:
                for c in q[u]:
                    if self.first[u] | self.first[c] != self.first[u]:
                        changed = True
                        self.first[u] |= self.first[c]
    def First(self, s):
        if len(s) == 0:
            return set()
        if type(s) == Terminal:
            return {s}
        if type(s) == Variable:
            return {self.first[s]}
        if type(s[0]) == Terminal:
            return {s[0]}
        else:
            ret = set()
            for i in s:
                if type(i) == Terminal:
                    # TODO: ret |= {i}
                    break
                elif self.nullable[i] == False:
                    ret |= self.first[i]
                    break
                else:
                    ret |= self.first[i]
            return ret
    def Follow(self, s):
        if len(s) == 0:
            raise 'null-string unsupported'
        if type(s[0]) == Terminal:
            raise 'Terminal has no follow'
        if len(s) >= 2:
            raise "Follow just for one variable"
        return self.follow[s]
    def _Follow(self, g):
        for p in g.productions:
            self.follow[p.left] = set()
        changed = True
        while changed == True:
            changed = False
            for p in g.productions:
                if len(p.right) == 0:
                    continue
                #print('creat follow for:', p)
                i = 0
                while i < len(p.right) - 1:
                    if type(p.right[i]) == Terminal:
                        i += 1
                        continue
                    '''
                    if self.First(p.right[i + 1:]) == set():
                        break
                    '''
                    t = self.First(p.right[i + 1:])
                    if self.Nullable(p.right[i + 1:]) == True:
                        t |= self.follow[p.left]
                    '''
                    if list(str(t)).count('+') >= 2:
                        print('DEBUG:', t)
                        for j in t:
                            print(type(j))
                    print('i:', p, self.follow, p.right[i], p.right[i + 1:], t)
                    '''
                    a = len(self.follow[p.right[i]])
                    self.follow[p.right[i]] |= t
                    b = len(self.follow[p.right[i]])
                    if a != b:
                        changed = True
                    i += 1
                if type(p.right[i]) == Terminal:
                    continue
                # print('a:', p, self.follow, p.right[i], p.left, self.follow[p.left])
                a = len(self.follow[p.right[i]])
                self.follow[p.right[i]] |= self.follow[p.left]
                b = len(self.follow[p.right[i]])
                if a != b:
                    changed = True
    def Nullable(self, s):
        for i in s:
            if type(i) == Terminal:
                return False
            if self.nullable[i] == False:
                return False
        return True
    def _Nullable(self, g):
        # TODO: Using bfs with reversed graph.
        q = set()
        for p in g.productions:
            self.nullable[p.left] = False
        for p in g.productions:
            if len(str(p.right)) == 0:
                # Null production
                self.nullable[p.left] = True
                q |= {p.left}
        productions = list(g.productions)
        while len(q) != 0:
            p = q.pop()
            for j in range(len(productions)):
                t = []
                for c in productions[j].right:
                    if c == p:
                        continue
                    t.append(c)
                if len(t) == 0 and self.nullable[productions[j].left] == False:
                    q |= {productions[j].left}
                    self.nullable[productions[j].left] = True
                productions[j] = Production(productions[j].left, t)
import sys
if __name__ == '__main__':
    g = Grammar(sys.argv[1])
    print(g)
    print(g.Product(int(sys.argv[2])))
