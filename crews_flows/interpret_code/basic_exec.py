exec_locals = {}
code = "print('hello world')\na = 6\nc=5\nprint(a)"
exec(code, {}, exec_locals)
print(exec_locals)

exec_locals = {}
code = "a = sum([20, 28])\nprint(a)"
exec(code, {}, exec_locals)
print(exec_locals)

gen_code = """
a = 5
y = 6
result = a + y
"""
exec(gen_code, {}, exec_locals)
print(exec_locals)
