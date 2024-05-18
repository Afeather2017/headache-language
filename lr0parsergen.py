#!/usr/bin/python3
import ipdb
import sys
import grammar
import re
line = sys._getframe
Break = ipdb.set_trace
class LR0Parser:
    def Closure(self, kernel):
        # return {(production_id, shift), ...}
        J = {i for i in kernel}
        t = list(J)
        last = 0
        length = len(t)
        while True:
            print(line().f_lineno, 'Closure:', J)
            for production_id, shift in t[last:length]:
                A, alpha, v, beta = ProductionSplit(
                        self.productions[production_id], shift)
                print(line().f_lineno, 'Closure:', J, type(v), v)
                if v == None:
                    continue
                if type(v) == grammar.Terminal:
                    continue
                if type(v) == grammar.Variable:
                    v = grammar.ProductionString([v])
                group = self.g.Group(v)
                for p in group:
                    if (self.index[p], 0) not in J:
                        J |= {(self.index[p], 0)}
                        t.append((self.index[p], 0))
            if length == len(t):
                break
            last = length
            length = len(t)
        return J
    def Goto(self, kernel, X):
        # kernels is {(production_id, shift)} and production_id at shift is variable
        # {(production_id, shift), ...}
        print(line().f_lineno, 'Goto for kernel', kernel, X)
        J = set()
        for sid in kernel:
            production_id, shift = self.product_shift[sid]
            p = self.productions[production_id]
            A, alpha, v, beta = ProductionSplit(p, shift)
            print(line().f_lineno, 'Split', shift, A, alpha, v, beta)
            if v == X:
                J |= {(production_id, shift)}
        print(line().f_lineno, 'Goto for closure', J)
        return self.Closure(J)
    def ClassifyClosure(self, closure):
        classify = {}
        for production_id, shift in closure:
            A, alpha, X, beta = ProductionSplit(
                    self.productions[production_id], shift)
            if X == None:
                continue
            if X not in classify:
                classify[X] = set()
            shift = min(shift + 1, len(self.shift_id[production_id]) - 1)
            classify[X] |= {self.shift_id[production_id][shift]}
        return classify
    def KernelCreat(self):
        # kernel = [{(production id, shift), ...}, ...]
        buffer = {Kernel((0,)): 0}
        self.kernels = [Kernel((0,))]
        self.table = {}
        self.lookahead[0][0] = {self.end}
        last = 0
        length = 1
        while True:
            for i in range(last, length):
                self.table[i] = {}
                print(line().f_lineno, 'kernels', self.kernels)
                kernel = self.kernels[i]
                print(line().f_lineno, 'closure for kernel:', kernel)
                kernel_productions = [self.product_shift[i] for i in kernel]
                print(line().f_lineno, 'kernel_productions:', kernel_productions)
                closure = self.Closure(kernel_productions)
                print(line().f_lineno, 'closure:', closure)
                # {Variable: { (production_id, shift), ...}, ...}
                classify = self.ClassifyClosure(closure)
                print(line().f_lineno, 'classify:', classify)
                for v in classify:
                    # classify[k] is Item kernel
                    # represent like {(production_id, shift), ...}
                    kernel = Kernel(classify[v])
                    print(line().f_lineno, 'kernel from classify', kernel)
                    if kernel not in buffer:
                        self.table[i] |= {len(self.kernels): v}
                        buffer |= {kernel: len(self.kernels)}
                        self.kernels.append(kernel)
                        self.Goto(kernel, v)
                    else:
                        u = buffer[kernel]
                        self.table[i] |= {u: v}
            print(line().f_lineno, 'After loop: kernels = ', self.kernels)
            input()
            if length == len(self.kernels):
                break
            last = length
            length = len(self.kernels)
        print('Kernels:', self.kernels)
        print('Table:', self.table)
    def __init__(self, g: grammar.Grammar):
        self.start = grammar.Variable('_')
        self.end = grammar.Terminal('$')
        left = grammar.ProductionString([self.start])
        right = grammar.ProductionString([g.start, self.end])
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
        t = 0
        for i in range(len(self.productions)):
            self.shift_id.append([])
            for j in range(len(self.productions[i].right) + 1):
                self.shift_id[i].append(t)
                self.product_shift[t] = (i, j)
                t += 1
        # To represent a graph.
        # table = { point: {to b: with a, }, }, }
        print('self.productions:', self.productions)
        print('self.index', self.index)
        print('self.shift_id', self.shift_id)
        print('self.product_shift', self.product_shift)
        self.KernelCreat()
        # self.productions = [productions..]
        # self.toolkit
        # self.start = Variable
        # TODO: Generate shift, goto and reduce form.
        # For the case of reduce/reduce conflict, raise error.
if __name__ == '__main__':
    g = grammar.Grammar(sys.argv[1])
    LALRParser(g)
