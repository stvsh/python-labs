from string import ascii_lowercase

vars = list(ascii_lowercase)
ops = {'~' : 4, '^' : 3, '&' : 2, '|' : 2, '/' : 2, '>' : 1}

def var(expr):
  return ''.join(sorted(set([c for c in expr if c.isalpha()])))


def wstrim(expr):
  expr = ''.join(expr.split())
  return expr


def check(expr):
  correct = True
  parens = 0

  for c in expr:
    if correct:
      if c in vars:
        correct = False
      elif c in ([')'] + list(ops.keys())):
        return False
    else:
      if c in ops:
        correct = True
      elif c in (vars + ['(']):
        return False

    if c == '(':
      parens += 1
    if c == ')':
      parens -= 1

    if parens < 0:
      return False

  if parens != 0:
    return False

  return not correct

# sprawdzanie czy wyrazenie ma poprawna liczbe nawiasow
# @expr - wyrazenie
# @ops  - dostepne operatory
def bal(expr, ops):
  pcounter = 0

  for i in range(len(expr) - 1, -1, -1):
    if expr[i] == '(':
      pcounter += 1
    elif expr[i] == ')':
      pcounter -= 1
    elif expr[i] in ops and pcounter == 0:
      return i
  
  return -1


def onp(expr):
  expr = wstrim(expr)

  # usuwanie zbednych zewnetrznych nawiasow
  while expr[0] == '(' and expr[len(expr) - 1] == ')' and check(expr[1:-1]):
    expr = expr[1:-1]
  
  p = bal(expr, ">")
  
  if p >= 0:
    return onp(expr[:p]) + onp(expr[p + 1:]) + expr[p]
  
  p = bal(expr, "&|")

  if p >= 0:
    return onp(expr[:p]) + onp(expr[p + 1:]) + expr[p]

  return expr


def onp_map(expr, vars, values):
  l = expr
  for i, c in enumerate(l):
    p = vars.find(c)
    if p >= 0:
      l[i] = values[i]

  return ''.join(l)
  
def OR(a, b):
  return a or b

def AND(a, b):
  return a and b


def value(onp_expr, values, vars):
  onp_expr = onp_map(onp_expr, vars, values)
  stack = []

  for c in onp_expr:
    if c in "01":
      stack.append(int(c))
    elif c == '|':
      stack.append(OR(stack.pop(), stack.pop()))
    elif c == '&':
      stack.append(AND(stack.pop(), stack.pop()))
    elif c == '>':
      stack.append(OR(stack.pop(), 1 - stack.pop()))

  return stack.pop()


def gen(n):
  for i in range(2**n):
    yield bin(i)[2:].rjust(n, '0')


def main():
  while True:
    expr = input('> ')

    print(check(expr))

    #print(expr)
    #expr = onp(expr)
    #print(expr)
    #vars = var(expr)
    #print(vars)
    #for v in gen(len(vars)):
    #  print(v, value(expr, v, vars))


if __name__ == "__main__":
  main()