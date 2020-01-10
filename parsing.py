from math import e, log, sin, cos, tan

NUMBER = [float, int]

class Variable():
# a * x^b * y^c
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

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
            left = left * sequence
        elif self.op is '/':
            left = left / sequence

        if self.termTail is None:
            return left
        else:
            return self.termTail.calc(left)

    def __repr__(self):
        return "TermTail(%s, %s, %s)" %(self.op, self.sequence, self.termTail)

class Sequence(Expr):
    def __init__(self, app, sign = None):
        self.app = app
        self.sign = sign

    def eval(self):
        left = self.app.eval()

        if self.sign == '-':
            return -left
        else:
            return left

    def __repr__(self):
        return "Sequence(%s, %s)" %(self.app, self.sign)

class SequenceTail(object):
    def __init__(self, sign, app, sequenceTail):
        self.sign = sign
        self.app = app
        self.sequenceTail = sequenceTail

    def calc(self, left):
        app = self.app.eval()

        if self.sign is '-':
            left = -app

        if self.sequenceTail is None:
            return left
        else:
            return self.sequenceTail.calc(left)

    def __repr__(self):
        return "SequenceTail(%s, %s, %s)" %(self.sign, self.app, self.sequenceTail)

class App(Expr):
    def __init__(self, deer, appTail):
        self.deer = deer
        self.appTail = appTail

    def eval(self):
        left = self.deer.eval()

        if self.appTail is None:
            return left
        else:
            return self.appTail.calc(left)

    def __repr__(self):
        return "App(%s, %s)" %(self.deer, self.appTail)

class AppTail(object):
    def __init__(self, op, deer, appTail):
        self.op = op
        self.deer = deer
        self.appTail = appTail

    def calc(self, left):
        deer = self.deer.eval()

        if self.op is '^':
            left = left ** deer

        if self.appTail is None:
            return left
        else:
            return self.appTail.calc(left)

    def __repr__(self):
        return "AppTail(%s, %s, %s)" %(self.op, self.deer, self.appTail)

class Deer(Expr):
    def __init__(self, factor, deerTail):
        self.factor = factor
        self.deerTail = deerTail

    def eval(self):
        left = self.factor.eval()

        if self.deerTail is None:
            return left
        else:
            return self.deerTail.calc(left)

    def __repr__(self):
        return "Deer(%s, %s)" %(self.factor, self.deerTail)

class DeerTail(Expr):
    def __init__(self, func, factor, deerTail):
        self.func = func
        self.factor = factor
        self.deerTail = deerTail

    def calc(self, left):
        self.funcs = {'log': log, 'sin': sin, 'cos': cos, 'tan': tan}
        funcs_list = ['log', 'sin', 'cos', 'tan']
        if self.func in funcs_list:
            func = self.funcs[self.func]
            left = func(left)
        
        if self.deerTail is None:
            return left
        else:
            return self.deerTail.calc(left)

    def __repr__(self):
        return "DeerTail(%s, %s, %s)" %(self.func, self.factor, self.deerTail)

class Factor(Expr):
    def __init__(self, expr):
        self.expr = expr

    def eval(self):
        ex = self.expr.eval() if isinstance(self.expr, Expr) else self.expr
        return ex

    def __repr__(self):
        return "Factor(%s)" % (self.expr)


class TokenList(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.n = 0

    def shift(self):
        self.n += 1
        return self.tokens[self.n - 1]

    def isType(self, tokenType):
        return self.tokens[self.n] is tokenType or (type(tokenType) is list and self.tokens[self.n].__class__ in tokenType) or tokenType == ('x' or 'y')

    def takeIt(self, tokenType = None):
        if tokenType is None or self.isType(tokenType):
            token = self.shift()
            return token
        else:
            raise Exception("Expected: %s, Actual: %s" % (tokenType, self.tokens[self.n]))
    
    def item(self):
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
    if tokens.isType('-'):
        tokens.takeIt()
        app = takeApp(tokens)
        return Sequence(app, '-')
    else:
        app = takeApp(tokens)
        return Sequence(app)

def takeApp(tokens):
    deer = takeDeer(tokens)
    appTail = takeAppTail(tokens)
    return App(deer, appTail)

def takeAppTail(tokens):
    if tokens.isType('^'):
        tokens.takeIt()
        deer = takeDeer(tokens)
        appTail = takeAppTail(tokens)
        return AppTail('^', deer, appTail)

def takeDeer(tokens):
    factor = takeFactor(tokens)
    deerTail = takeDeerTail(tokens)
    return Deer(factor, deerTail)

def takeDeerTail(tokens):
    funcs_list = ['log', 'sin', 'cos', 'tan']
    if tokens.item in funcs_list:
        func = tokens.takeIt()
        factor = takeFactor(tokens)
        deerTail = takeDeerTail(tokens)
        return DeerTail(func, factor, deerTail)

def takeFactor(tokens):
    if tokens.isType('('):
        tokens.takeIt('(')
        expr = takeExpr(tokens)
        tokens.takeIt(')')
        return Factor(expr)
    else:
        num = tokens.takeIt(NUMBER)
        return Factor(num)


def Parser(tokens):
    return takeExpr(TokenList(tokens))
