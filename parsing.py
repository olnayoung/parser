# E  := T E'
# E' := ( '+' | '-' ) T E' | e
# T  := S T'
# T' := ( '*' | '/' ) S T' | e
# S  := F S'
# S' := '^' F S'
# F  := '(' E ')' | '-' F | int | log F | sin F | ...

from math import log, sin, cos, tan
from extra_funcs import is_digit
from extra_funcs import multiply
from extra_funcs import div

NUMBER = [float, int]

class Expr(object):
    def __init__(self, term, exprTail):
        self.term = term
        self.exprTail = exprTail

    def eval(self):
        if self.exprTail is None:
            return self.term.eval()
        else:
            return self.exprTail.calc(self.term.eval())

    def __repr__(self):
        return "Expr(%s, %s)" % (self.term, self.exprTail)

class ExprTail(object):
    def __init__(self, op, term, exprTail):
        self.op = op
        self.term = term
        self.exprTail = exprTail

    def calc(self, left):
        eval_t = self.term.eval()
        
        if self.op is '+':
            left = left + eval_t
        elif self.op is '-':
            left = left - eval_t

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

    def eval(self):
        left = self.sequence.eval()

        if self.termTail is None:
            return left
        else:
            return self.termTail.calc(left)

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
            left *= sequence
        elif self.op is '/':
            left /= sequence

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
            left = left ** factor
        
        if self.sequenceTail is None:
            return left
        else:
            self.sequenceTail.calc(left)

    def __repr__(self):
        return "SequenceTail(%s, %s, %s)" %(self.op, self.factor, self.sequenceTail)

class Factor(Expr):
    def __init__(self, expr, sign = None):
        self.expr = expr
        self.sign = sign
        self.funcs = {'log': log, 'sin': sin, 'cos': cos, 'tan': tan}
        self.funcs_list = ['log', 'sin', 'cos', 'tan']

    def eval(self):
        temp = self.expr.eval() if isinstance(self.expr, Expr) else self.expr
        if self.sign is '-':
            temp *= -1
            return temp
        elif self.sign in self.funcs_list:
            func = self.funcs[self.sign]
            return func(temp)
        
        return temp

    def __repr__(self):
        return "Factor(%s, %s)" % (self.sign, self.expr)


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

        if tokenType is None or self.isType(tokenType) or tokenType in funcs_list or self.tokens[self.n] in ['x', 'y', 'e', 'pi']:
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
    funcs_list = ['log', 'sin', 'cos', 'tan']

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
        factor = takeFactor(tokens)
        return Factor(factor, func)

    else:
        num = tokens.takeIt(NUMBER)
        return Factor(num)


def Parser(tokens):
    return takeExpr(TokenList(tokens))