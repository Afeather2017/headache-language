#!/usr/bin/python3
import ipdb
import sys
import grammar
import re
def ColorDelete(s):
    return re.sub('\033\[\d+m', '', s)
line = sys._getframe
Break = ipdb.set_trace
def ProductionSplit(production, split_at):
    if split_at >= len(production.right):
        return (production.left, production.right[:split_at], None, None)
    return (production.left, production.right[:split_at], production.right[split_at],
            production.right[split_at + 1:])
class Kernel:
    def __init__(self, production_ids):
        self.production_ids = list(production_ids)
        self.production_ids.sort()
        self.production_ids = tuple(self.production_ids)
        self.hash = hash(self.production_ids)
    def __hash__(self):
        return self.hash
    def __eq__(self, a):
        return self.production_ids == a.production_ids
    def __repr__(self):
        return str(self.production_ids)
    def __iter__(self):
        return iter(self.production_ids)
    def __next__(self):
        return next(self.production_ids)
    def Ids(self):
        return self.production_ids
class LALRParser:
    def _Closure(self, kernel_id):
        # return {(production_id, shift): lookahead, ...}
        J = set()
        for psid in self.kernels[kernel_id]:
            # self.lookahead[kid][psid]
            pid, shift = self.product_shift[psid]
            for lookahead in self.lookahead[kernel_id][psid]:
                J |= {(pid, shift, lookahead)}
        t = list(J)
        last = 0
        length = len(t)
        while True:
            for production_id, shift, lookahead in t[last:length]:
                A, alpha, v, beta = ProductionSplit(self.productions[production_id], shift)
                if v == None:
                    continue
                if type(v) == grammar.Terminal:
                    continue
                if type(v) == grammar.Variable:
                    v = grammar.ProductionString([v])
                first = self.toolkit.First(beta + grammar.ProductionString([lookahead]))
                group = self.g.Group(v)
                for p in group:
                    for lookahead in first:
                        if (self.index[p], 0, lookahead) not in J:
                            J |= {(self.index[p], 0, lookahead)}
                            t.append((self.index[p], 0, lookahead))
            if length == len(t):
                break
            last = length
            length = len(t)
        print(line().f_lineno, 'closure:', J)
        J = {}
        for pid, shift, lookahead in t:
            if (pid, shift) not in J:
                J[(pid, shift)] = set()
            J[(pid, shift)] |= {lookahead}
        return J
    def _Goto(self, kernel_id, X):
        # kernels is {(production_id, shift)} and production_id at shift is variable
        # {(production_id, shift), ...}
        J = set()
        for psid in self.kernels[kernel_id]:
            production_id, shift = self.product_shift[psid]
            p = self.productions[production_id]
            A, alpha, v, beta = ProductionSplit(p, shift)
            if v == X:
                J |= {(production_id, shift)}
        return self._Closure(kernel_id)
    def ClassifyClosure(self, closure, kernel_id):
        # FIXME: null-production will cause to some wrong result.
        classify = {}
        for production_id, shift in closure:
            A, alpha, X, beta = ProductionSplit(
                    self.productions[production_id], shift)
            if X == None:
                continue
            if X not in classify:
                classify[X] = {}
            # Break()
            lookahead = closure[(production_id, shift)]
            shift = min(shift + 1, len(self.shift_id[production_id]) - 1)
            classify[X] |= {self.shift_id[production_id][shift]: lookahead}
        print(line().f_lineno, 'ClassifyClosure:', classify)
        return classify
    def KernelCreat(self):
        buffer = {Kernel((0,)): 0}
        self.kernels = [Kernel((0,))]
        self.map = {}
        '''
        lookahead:
        kernels_id    0  1
        production_id {} {}
        ...
        '''
        self.lookahead = [{0: {self.end}, }]
        last = 0
        length = 1
        print(line().f_lineno, 'self.lookahead', self.lookahead)
        print(line().f_lineno, 'self.shift_id', self.shift_id)
        print(line().f_lineno, 'self.product_shift', self.product_shift)
        while True:
            print(line().f_lineno, 'self.kernels[{}:{}]:'.format(last, length), self.kernels[last:length])
            for i in range(last, length):
                self.map[i] = {}
                kernel = self.kernels[i]
                closure = self._Closure(i)
                # classify: {Variable: { (production_id, shift), ...}, ...}
                classify = self.ClassifyClosure(closure, i)
                print(line().f_lineno, 'classify:', classify)
                for v in classify:
                    # classify[k] is Item kernel
                    # represent like {(production_id, shift), ...}
                    kernel = Kernel(classify[v])
                    if kernel not in buffer:
                        kernel_id = len(self.kernels)
                        self.map[i] |= {kernel_id: v}
                        buffer |= {kernel: kernel_id}
                        self.kernels.append(kernel)
                        # Break()
                        self.LookaheadInsert(kernel_id, classify[v])
                        self._Goto(kernel_id, v)
                    else:
                        kernel_id = buffer[kernel]
                        self.map[i] |= {kernel_id: v}
                        self.LookaheadInsert(kernel_id, classify[v])
            print(line().f_lineno, 'After loop: kernels = ', self.kernels)
            print(line().f_lineno, 'self.lookahead = ', self.lookahead)
            #input()
            if length == len(self.kernels):
                break
            last = length
            length = len(self.kernels)
        print('Kernels:', self.kernels)
        print('Map:', self.map)
    def LookaheadInsert(self, kernel_id, lookahead):
        '''
        self.lookahead:
        kernels_id          0  1
        production_shift_id {} {}
        ...
        '''
        # lookahead: {production_shift_id: terminals
        if len(self.lookahead) <= kernel_id:
            self.lookahead.append({})
        for production_shift_id in self.kernels[kernel_id]:
            if production_shift_id not in self.lookahead[kernel_id]:
                self.lookahead[kernel_id][production_shift_id] = set()
            self.lookahead[kernel_id][production_shift_id] |= lookahead[production_shift_id]
    def TableCreat(self):
        '''
        for each item I:
            for each production matches 'A->[anystring].' with lookahead set s:
                creat reduce (I, s, 'A->[anystring]')
        but only the kernels has the matched production
        '''
        '''
        action:                 terminals
        state(kernel_id) (reduce, production_id)
                       or
        state(kernel_id) (shift,          state)
        '''
        action = {kid: {} for kid in range(len(self.kernels))}
        '''
        goto: variables
        state   state
        '''
        goto = {kid: {} for kid in range(len(self.kernels))}
        endpid = self.shift_id[0][2]
        for kid in range(len(self.kernels)):
            kernel = self.kernels[kid]
            for psid in kernel:
                if endpid == psid:
                    print(line().f_lineno, 'kernel_id:',  kid)
                    action[kid][self.end] = ('a', None)
                    continue
                pid, shift = self.product_shift[psid]
                #print(line().f_lineno, 'pid, shift, len:',  pid, shift, self.shift_id[pid])
                if shift + 1 != len(self.shift_id[pid]):
                    # not ending at tail of production's right.
                    continue
                if kid not in action:
                    action[kid] = {}
                for terminal in self.lookahead[kid][psid]:
                    if terminal in action[kid]:
                        raise 'This grammar is not LALR(1)'
                    action[kid][terminal] = ('r', pid)
        for kid in range(len(self.kernels)):
            for k in self.map[kid]:
                # kid connect to k with self.map[kid][k], which is a terminal or variable.
                v = self.map[kid][k]
                if type(v) == grammar.Terminal:
                    action[kid][v] = ('s', k)
                else:
                    goto[kid][v] = k
        print(line().f_lineno, 'action:', action)
        print(line().f_lineno, 'goto:', goto)
        self.action = action
        self.goto = goto
    def PidToProduction(self, pid):
        return self.production[pid]
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
        t = 'Productions is:\n' + str(self.productions) + '\n'
        t = ColorDelete(t)
        f.write(t)
        f.write('```\n')
        t = '| | ' + ' | '.join([str(v) for v in head]) + ' |\n'
        t = ColorDelete(t)
        f.write(t)
        t = '| - | ' + (' | '.join(['-'] * len(head)) + ' |\n')
        t = ColorDelete(t)
        f.write(t)
        for kid in range(len(self.kernels)):
            f.write('| %s | ' % kid)
            #Break()
            for v in head:
                t = ''
                if type(v) == grammar.Terminal:
                    if v in action[kid]:
                        t = str(action[kid][v])
                else: # variables
                    if v in goto[kid]:
                        t = 'g' + str(goto[kid][v])
                        t = ColorDelete(t)
                f.write(t + ' | ')
            f.write('\n')
        f.close()
    def __init__(self, g: grammar.Grammar):
        self.start = grammar.Variable('_')
        self.end = grammar.Terminal('$')
        left = grammar.ProductionString([self.start])
        right = grammar.ProductionString([g.start, self.end])
        #right = grammar.ProductionString([g.start])
        # Add the first variable
        self.productions = list(g.productions)
        self.productions.sort()
        self.productions = (grammar.Production(left, right), ) + tuple(
                self.productions)
        self.index = {}
        for i in range(len(self.productions)):
            self.index[self.productions[i]] = i
        self.g = g
        '''
            self.id    shift0    shift1
        production id0 kernel id
        production id1 
        production id2
        '''
        self.shift_id = []
        # for each id, product_shift[id] is the production and shift
        self.product_shift = {}
        self.tmpend = grammar.ProductionString([grammar.Terminal('#')])
        t = 0
        for i in range(len(self.productions)):
            self.shift_id.append([])
            for j in range(len(self.productions[i].right) + 1):
                self.shift_id[i].append(t)
                self.product_shift[t] = (i, j)
                t += 1
        # To represent a graph.
        print('LALR(1) self.productions:', self.productions)
        print('LALR(1) self.index', self.index)
        print('LALR(1) self.shift_id', self.shift_id)
        print('LALR(1) self.product_shift', self.product_shift)
        self.toolkit = grammar.Toolkit(g)
        self.KernelCreat()
        self.TableCreat()
        self.MarkDown(self.g.filename + '.md')
        # self.productions = [productions..]
        # self.toolkit
        # self.start = Variable
        # TODO: Generate shift, goto and reduce form.
        # For the case of reduce/reduce conflict, raise error.
if __name__ == '__main__':
    g = grammar.Grammar(sys.argv[1])
    LALRParser(g)
