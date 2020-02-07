from math import log, sin, cos, tan, pi, e, nan
from copy import deepcopy
from extra_funcs import is_digit

NUMBER = [float, int]

class Expr(object):
    def __init__(self, term, exprTail):
        self.term = term
        self.exprTail = exprTail
        self.coef = 1
        self.expo = 1
        self.sign = None

    def __add__(self, left):
        return left

    def __mul__(self, left):
        return left

    def eval(self):
        if self.exprTail is None:
            return self.term.eval()
        else:
            return self.exprTail.calc(self.term.eval())

    def get_domain(self):
        return eq, in_eq

    def __repr__(self):
        return "Expr(%s, %s)" % (self.term, self.exprTail)

class ExprTail(object):
    def __init__(self, op, term, exprTail):
        self.op = op
        self.term = term
        self.exprTail = exprTail

    def calc(self, left):
        term = self.term.eval()

        if self.op is '-':
            term.coef *= -1

        if isinstance(left.contain, dict):
            if isinstance(term.contain, dict):
                dic_term_key_list = list(term.contain.keys())
                for n in range(len(term.contain)):
                    if dic_term_key_list[n] in left.contain:
                        if term.coef == -1:
                            term.contain[dic_term_key_list[n]].coef *= -1
                        a = deepcopy(left.contain[dic_term_key_list[n]]) + term.contain[dic_term_key_list[n]]
                        del left.contain[dic_term_key_list[n]]
                        if a.contain != 0:
                            left.contain[(a.sign, a.contain, a.expo)] = a
                    else:
                        if term.coef == -1:
                            term.contain[dic_term_key_list[n]].coef *= -1
                        left[dic_term_key_list[n]] = term.contain[dic_term_key_list[n]]
                
                if len(left.contain) == 0:
                    left.contain = 0
                elif len(left.contain) == 1:
                    dic_left_key_list = list(left.contain.keys())
                    left.contain = left.contain[dic_left_key_list[0]]

            else:
                if (term.sign, term.contain, term.expo) in left.contain:
                    a = deepcopy(left.contain[(term.sign, term.contain, term.expo)]) + term
                    del left.contain[(term.sign, term.contain, term.expo)]

                    if a.contain != 0:
                        left.contain[(a.sign, a.contain, a.expo)] = a
                    elif len(left.contain) == 1:
                        dic_left_key_list = list(left.contain.keys())
                        left.coef *= left.contain[dic_left_key_list[0]].coef
                        left.expo *= left.contain[dic_left_key_list[0]].expo
                        left.contain = left.contain[dic_left_key_list[0]].contain
                    
                else:
                    left.contain[(term.sign, term.contain, term.expo)] = term
        else:
            left += term

        if self.exprTail is None:
            return left
        else:
            return self.exprTail.calc(left)

    def __repr__(self):
        return "ExprTail(%s, %s, %s)" %(self.op, self.term, self.exprTail)

class Term(Expr):
    def __init__(self, sequence, termTail):
        self.sequence = sequence
        self.termTail = termTail
        self.coef = 1
        self.expo = 1
        self.sign = None

    def __add__(self, left):
        return left

    def __mul__(self, left):
        self.sequence *= left
        return left

    def eval(self):
        if self.termTail is None:
            left = self.sequence.eval()
        else:
            left = self.termTail.calc(self.sequence.eval())

        return left

    def __repr__(self):
        return "Term(%s, %s)" % (self.sequence, self.termTail)

class TermTail(object):
    def __init__(self, op, sequence, termTail):
        self.op = op
        self.sequence = sequence
        self.termTail = termTail

    def calc(self, left):
        sequence = self.sequence.eval()

        if self.op is '*':
            if isinstance(left.contain, dict):
                if isinstance(sequence.contain, dict):
                    dic_left_key_list = list(left.contain.keys())
                    dic_seq_key_list = list(sequence.contain.keys())
                    empty_dic = {}
                    for n in range(len(left.contain)):
                        for m in range(len(sequence.contain)):
                            a = deepcopy(left.contain[dic_left_key_list[n]]) * deepcopy(sequence.contain[dic_seq_key_list[m]])

                            if (a.sign, a.contain, a.expo) in empty_dic:
                                empty_dic[(qa.sign, a.contain, a.expo)] += a
                            else:
                                empty_dic[(a.sign, a.contain, a.expo)] = a

                    left.coef = 1
                    left.contain = empty_dic
                    left.expo = 1

                else:
                    dic_key_list = list(left.contain.keys())
                    for n in range(len(left.contain)):
                        left.contain[dic_key_list[n]] *= sequence
            else:
                left *= sequence

        elif self.op is '/':
            sequence.expo *= -1
            left *= sequence

        if self.termTail is None:
            return left
        else:
            return self.termTail.calc(left)

    def __repr__(self):
        return "TermTail(%s, %s, %s)" %(self.op, self.sequence, self.termTail)

class Sequence(Expr):
    def __init__(self, factor, sequenceTail):
        self.factor = factor
        self.sequenceTail = sequenceTail
        self.coef = 1
        self.expo = 1
        self.sign = None

    def __add__(self, left):
        return left

    def __mul__(self, left):
        return left

    def eval(self):
        left = self.factor.eval()

        if self.sequenceTail is None:
            return left
        else:
            return self.sequenceTail.calc(left)

    def __repr__(self):
        return "Sequence(%s, %s)" % (self.factor, self.sequenceTail)

class SequenceTail(object):
    def __init__(self, op, factor, sequenceTail):
        self.op = op
        self.factor = factor
        self.sequenceTail = sequenceTail

    def calc(self, left):
        factor = self.factor.eval()

        if self.op == '^':
            if is_digit(left.contain) and is_digit(factor.contain):
                left.contain = left.contain ** factor.contain
            else:
                left.expo = factor * left.expo
            # left.expo *= factor
            # left = left ** factor

        if self.sequenceTail is None:
            return left
        else:
            return self.sequenceTail.calc(left)

    def __repr__(self):
        return "SequenceTail(%s, %s, %s)" %(self.op, self.factor, self.sequenceTail)

class Factor(Expr):
    funcs = {'sin': sin, 'cos': cos, 'tan': tan, 'e': e, 'pi': pi}
    funcs_list = ['sin', 'cos', 'tan']

    def __init__(self, expr, sign = None, base = None, k = None):
        self.expr = expr
        self.sign = sign            # -, sin, cos, tan, log
        self.base = base
        # self.k = k
        self.coef = 1
        self.contain = 0
        self.expo = 1

    def __add__(self, left):
        if is_digit(self.contain) and is_digit(left.contain):
            if left.coef == 1:
                self.contain += left.contain
            else:
                self.contain -= left.contain

        elif self.contain == left.contain:
            if self.expo == left.expo:
                self.coef += left.coef

                if self.coef == 0:
                    self.coef = 1
                    self.contain = 0
                    self.expo = 1

            else:
                dic = {(self.sign, self.contain, self.expo) : self, (left.sign, left.contain, left.expo) : left}
                self.coef = 1
                self.contain = deepcopy(dic)
                self.expo = 1

        else:
            dic = {(self.sign, self.contain, self.expo) : self, (left.sign, left.contain, left.expo) : left}
            self.coef = 1
            self.contain = deepcopy(dic)
            self.expo = 1

        return self

    def __mul__(self, left):
        if is_digit(left):
            self.contain *= left
        elif is_digit(self.contain) and is_digit(left.contain):
            
            expo = left.expo if is_digit(left.expo) else left.expo.contain
            if expo == 1:
                self.contain *= left.contain
            else:
                self.contain /= left.contain

        elif is_digit(self.contain):
            if self.expo == 1:
                left.coef *= (self.coef * self.contain)
            else:
                left.coef /= (self.coef * self.contain)
            return left

        elif is_digit(left.contain):
            if left.expo == 1:
                self.coef *= (left.coef * left.contain)
            else:
                self.coef /= (left.coef * left.contain)
        else:
            if self.contain == left.contain:
                self.coef *= left.coef
                self.expo += left.expo

                if self.expo == 0:
                    if self.coef > 0:
                        self.contain = self.coef
                        self.coef = 1
                    else:
                        self.contain = self.coef * -1
                        self.coef = -1
                    self.expo = 1
        return self

    def eval(self):
        if isinstance(self.expr, Expr):
            a = self.expr.eval()
            self.contain = a
        else:
            self.contain = self.expr

        if self.sign is '-':
            self.coef *= -1
            return self

        elif self.sign in self.funcs_list:
            func = self.funcs[self.sign]

            if is_digit(self.contain):
                self.contain = func(self.contain)
                self.sign = None

        # elif self.sign == 'log':
        
        # elif self.sign == 'sig':
        
        return self

    def __repr__(self):
        return "Factor(%s, %s, %s, %s)" % (self.sign, self.coef, self.contain, self.expo)


class TokenList(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.n = 0

    def shift(self):
        self.n += 1
        return self.tokens[self.n - 1]

    def isType(self, tokenType):
        return self.tokens[self.n] is tokenType or (type(tokenType) is list and self.tokens[self.n].__class__ in tokenType)

    def takeIt(self, tokenType = None):
        funcs_list = ['log', 'sin', 'cos', 'tan']

        if tokenType is None or self.isType(tokenType) or tokenType in funcs_list or self.tokens[self.n] in ['e', 'pi', ','] or self.tokens[self.n] in var_list:
            token = self.shift()
            return token
        else:
            raise Exception("Expected: %s, Actual: %s" % (tokenType, self.tokens[self.n]))

    def getItem(self):
        return self.tokens[self.n]



def takeExpr(tokens):
    term = takeTerm(tokens)
    exprTail = takeExprTail(tokens)
    return Expr(term, exprTail)

def takeExprTail(tokens):
    if tokens.isType('+') or tokens.isType('-'):
        op = tokens.takeIt()
        term = takeTerm(tokens)
        exprTail = takeExprTail(tokens)
        return ExprTail(op, term, exprTail)

def takeTerm(tokens):
    sequence = takeSequence(tokens)
    termTail = takeTermTail(tokens)
    return Term(sequence, termTail)

def takeTermTail(tokens):
    if tokens.isType('*') or tokens.isType('/'):
        op = tokens.takeIt()
        sequence = takeSequence(tokens)
        termTail = takeTermTail(tokens)
        return TermTail(op, sequence, termTail)

def takeSequence(tokens):
    factor = takeFactor(tokens)
    sequenceTail = takeSequenceTail(tokens)
    return Sequence(factor, sequenceTail)

def takeSequenceTail(tokens):
    if tokens.isType('^'):
        op = tokens.takeIt()
        factor = takeFactor(tokens)
        sequenceTail = takeSequenceTail(tokens)
        return SequenceTail(op, factor, sequenceTail)

def takeFactor(tokens):
    funcs_list = ['sin', 'cos', 'tan']

    if tokens.isType('('):
        tokens.takeIt('(')
        expr = takeExpr(tokens)
        tokens.takeIt(')')
        return Factor(expr)
        
    elif tokens.isType('-'):
        tokens.takeIt('-')
        factor = takeFactor(tokens)
        return Factor(factor, '-')
    
    elif tokens.getItem() in funcs_list:
        func = tokens.getItem()
        tokens.takeIt(func)
        tokens.takeIt('(')
        expr = takeExpr(tokens)
        tokens.takeIt(')')
        return Factor(expr, func)
    
    # elif tokens.getItem() == 'sig':
    #     func = tokens.getItem()
    #     tokens.takeIt(func)
    #     tokens.takeIt('(')
    #     k = tokens.getItem()
    #     var_list.append(k)
    #     tokens.shift()
    #     tokens.takeIt(',')
    #     expr = takeExpr(tokens)
    #     var_list.pop()
    #     tokens.takeIt(',')
    #     start = tokens.takeIt(NUMBER)
    #     tokens.takeIt(',')
    #     end = tokens.takeIt(NUMBER)
    #     tokens.takeIt(')')
    #     return Factor(expr, 'sig', [start, end], k)

    elif tokens.getItem() == 'log':
        func = tokens.getItem()
        tokens.takeIt(func)
        tokens.takeIt('(')
        expr1 = takeExpr(tokens)
        expr2 = None
        
        if tokens.getItem() == ',':
            tokens.takeIt(',')
            expr2 = takeExpr(tokens)
        tokens.takeIt(')')
        return Factor(expr1, func, expr2)  # log(expr1, expr2) = log_expr2 (expr1)

    else:
        num = tokens.takeIt(NUMBER)
        return Factor(num)


def Parser(tokens, v_l):
    global var_list, eq, in_eq
    var_list = v_l
    eq = []
    in_eq = []
    
    return takeExpr(TokenList(tokens))