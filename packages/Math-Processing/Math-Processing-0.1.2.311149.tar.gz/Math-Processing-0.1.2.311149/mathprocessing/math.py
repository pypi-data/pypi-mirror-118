import sys

if sys.version_info[0] == 3 and sys.version_info[1] >= 6:
    import tkinter.messagebox as msgbox
elif sys.version_info[0] == 3 and sys.version_info[1] < 6:
    import messagebox as msgbox
elif sys.version_info[0] == 2:
    import tkMessageBox as msgbox
else:
    raise SystemExit('Python version is not supported')

import math

def caculation(self, mode, a, b):
    data = mode
    try:
        a = float(self.a.get())
        if a - int(a) == 0:
            a = int(a)
        b = float(self.b.get())
        if b - int(b) == 0:
            b = int(b)
        if data == '+':
            result = a + b
        elif data == '-':
            result = a - b
        elif data == '*':
            result = a * b
        elif data == '/':
            result = a / b
        elif data == '//':
            result = a // b
        elif data == '!':
            result = 1
            for x in range(1, a + 1):
                result *= x
        elif data == '^':
            result = a ** b
        elif data == 'sqrt()':
            result = math.sqrt(a)
        # Four Fundamental Operations
        elif data == 'Type':
            result = type(a)
        elif data == 'x / y ... ?':
            result = a % b
        # Other
        elif data == 'acos()':
            result = math.acos(a)
        elif data == 'cos()':
            result = math.cos(a)
        elif data == 'asin()':
            result = math.asin(a)
        elif data == 'sin()':
            result = math.sin(a)
        elif data == 'atan()':
            result = math.atan(a)
        elif data == 'tan()':
            result = math.tan(a)
        elif data == 'dist()':
            result = math.dist(a, b)
        elif data == 'hypot()':
            result = math.hypot(a, b)
        # Trigonometric Function
        elif data == 'acosh()':
            result = math.acosh(a)
        elif data == 'asinh()':
            result = math.asinh(a)
        elif data == 'atanh()':
            result = math.atanh(a)
        elif data == 'cosh()':
            result = math.cosh(a)
        elif data == 'sinh()':
            result = math.sinh(a)
        elif data == 'tanh()':
            result = math.tanh(a)
            # Hyperbolic Functions
        elif data == 'exp()':
            result = math.exp(a)
        elif data == 'expm1()':
            result = math.expm1(a)
        # Power And Logarithmic Functions
        elif data == '>':
            if a > b:
                result = True
            else:
                result = False
        elif data == '<':
            if a < b:
                result = True
            else:
                result = False
        elif data == '>=':
            if a >= b:
                result = True
            else:
                result = False
        elif data == '<=':
            if a <= b:
                result = True
            else:
                result = False
        elif data == '==':
            if a == b:
                result = True
            else:
                result = False
        elif data == '!=':
            if a != b:
                result = True
            else:
                result = False
        # Compare
        elif data == 'Degrees':
            result = math.degrees(a)
        elif data == 'Radians':
            result = math.radians(a)
        elif data == 'Int / Float':
            if type(a) == type(1):
                result = float(a)
            elif type(a) == type(1.0):
                result = int(a)
        # Change
        else:
            raise AttributeError('No attribute name " %s "' % data)
        # Add
        return result
    except TypeError as msg:
        msgbox.showerror('Type Error', msg)
    except ValueError as msg:
        msgbox.showerror('Value Error', msg)
    except AttributeError as msg:
        msgbox.showerror('Attribute Error', msg)
    except ZeroDivisionError as msg:
        msgbox.showerror('Zero Division Error', msg)
