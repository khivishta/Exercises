

"auxilliary functions for isTauto"

def addxt(env,x,b) :
    "add entry to dictionary"
    env = env.copy() #need to copy the dictionary
    env[x]=b
    return env
        
def truthtable(vars) :
    "create all truthtable for a given list of variables"
    "we need to use lists here not sets otherwise we cannot use"
    "indices or slicing"
    if vars == [] :
        return [dict([])]
    else :
        x = vars[0]
        tts = truthtable(vars[1:])
        "tts =  truthtables for all but the first variable (x)"
        "add x=true and x=false and combine the results"
        return list(map(lambda env:addxt(env,x,True),tts))+\
               list(map(lambda env:addxt(env,x,False),tts))

class Expr :

    def str_aux(self,fix) :
        "print expression in a given contxt"
        "fix = level of the context, higher = binds stronger"

    def __str__(self) :
        return self.str_aux(0) #never print brackets on toplevel.

    def make_tt(self) :
        out = ""
        header = ""
        for x in self.vars():
            header += x + "\t| "
        header += str(self)
        out += header + "\n"
        tt = truthtable(list(self.vars()))
        for env in tt :
            line = ""
            for x in env :
                line += str(env[x]) + "\t| "
            line += str(self.eval(env))
            out += line + "\n"
        return out
            
    
    def isTauto(self) :
        "is this expression a tautology?"
        "create all dictionaries"
        tt = truthtable(list(self.vars())) #need to coerce to list
        "check wether they all evaluate to true."
        for env in tt :
            if not self.eval(env) :
                return False
        return True
    
class Not(Expr) :

    def __init__(self,e) :
        self.e = e

    def str_aux(self,fix) :
        return "!"+self.e.str_aux(3)
        
    def eval(self,env) :
        return not (self.e.eval(env))

    def vars(self) :
        return self.e.vars()
        
class BinOp(Expr) :

    def __init__(self,l,r) :
        self.l = l
        self.r = r

    def str_aux(self,fix) :
        s=self.l.str_aux(self.fix)+\
          self.sym+self.r.str_aux(self.fix)
        "s = print expression without brackets"
        "then add brackets if sorounding level is higher,"
        if fix > self.fix :
            return "("+s+")"
        else :
            return s

    def vars(self) :
        return self.l.vars().union(self.r.vars())
    
    def eval(self,env) :
        return self.op(self.l.eval(env),self.r.eval(env))
 
class And(BinOp) :

    fix = 2
    sym = "&"
    
    def op(self,l,r) :
        return l&r
    
class Or(BinOp) :

    fix = 1
    sym = "|"

    def op(self,l,r) :
        return l|r
    
class Eq(BinOp) :
    
    fix = 0
    sym = "=="

    def op(self,l,r) :
        return l==r
    
class Const(Expr) :

    def __init__(self,val) :
        self.val = val

    def str_aux(self,fix) :
        return str(self.val)
    
    def eval(self,env) :
        return self.val

    def vars(self) :
        return {}
               
class Var(Expr) :

    def __init__(self,name) :
        self.name = name

    def str_aux(self,fix) :
        return self.name

    def eval(self,env) :
        return env[self.name]

    def vars(self) :
        return { self.name }
    

"test data"

e1 = Or(Var("x"),Not(Var("x")))
e2 = Eq(Var("x"),Not(Not(Var("x"))))
e3 = Eq(Not(And(Var("x"),Var("y"))),Or(Not(Var("x")),Not(Var("y"))))
e4 = Eq(Not(And(Var("x"),Var("y"))),And(Not(Var("x")),Not(Var("y"))))
e5 = Eq(Eq(Eq(Var("p"),Var("q")),Var("r")),Eq(Var("p"),Eq(Var("q"),Var("r"))))

print(e1)
print(e2)
print(e3)
print(e4)
print(e5)

print(And(Not(Var("p")),Var("q")))
print(Not(And(Var("p"),Var("q"))))
print(Or(And(Var("p"),Var("q")),Var("r")))
print(And(Var("p"),Or(Var("q"),Var("r"))))
print(Eq(Or(Var("p"),Var("q")),Var("r")))
print(Or(Var("p"),Eq(Var("q"),Var("r"))))

print (e2.eval({"x" : True}))
print (e3.eval({"x" : True, "y" : True}))
print (e4.eval({"x" : False, "y" : True}))

print(e1.make_tt())
print(e2.make_tt())
print(e3.make_tt())
print(e4.make_tt())
print(e5.make_tt())

print (And(Var("x"),And(Var("y"),Var("z"))))
print (And(And(Var("x"),Var("y")),Var("z")))

print (e1.isTauto())
print (e2.isTauto())
print (e3.isTauto())
print (e4.isTauto())
print (e5.isTauto())

"""
x|!x
x==!!x
!(x&y)==!x|!y
!(x&y)==!x&!y
p==q==r==p==q==r
!p&q
!(p&q)
p&q|r
p&(q|r)
p|q==r
p|(q==r)
True
True
False
x       | x|!x
True    | True
False   | True

x       | x==!!x
True    | True
False   | True

y       | x     | !(x&y)==!x|!y
True    | True  | True
False   | True  | True
True    | False | True
False   | False | True

y       | x     | !(x&y)==!x&!y
True    | True  | True
False   | True  | False
True    | False | False
False   | False | True

p       | q     | r     | p==q==r==p==q==r
True    | True  | True  | True
False   | True  | True  | True
True    | False | True  | True
False   | False | True  | True
True    | True  | False | True
False   | True  | False | True
True    | False | False | True
False   | False | False | True

x&y&z
x&y&z
True
True
True
False
True
"""
