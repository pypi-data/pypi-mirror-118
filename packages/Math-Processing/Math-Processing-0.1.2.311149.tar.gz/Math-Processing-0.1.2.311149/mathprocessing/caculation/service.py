import sys

if sys.version_info[0] == 2 and sys.version_info[1] <= 6:
    raise SystemExit('Python version is not supported')
if sys.version_info[0] == 1 or sys.version_info[0] == 0:
    raise SystemExit('Python version is not supported')
if sys.version_info[0] > 3:
    raise SystemExit('Python version is not supported')
# Path Test

if sys.version_info[0] == 3 and sys.version_info[1] >= 6:
    import tkinter as tk
    import tkinter.messagebox as msgbox
elif sys.version_info[0] == 3 and sys.version_info[1] < 6 and sys.version_info[1] >= 0:
    import tkinter as tk
    import messagebox as msgbox
elif sys.version_info[0] == 2:
    import Tkinter as tk
    import tkMessageBox as msgbox
import math
import time
import sys
# Import

class Caculation():
    def __init__(self, title=''):
        if sys.version_info[0] == 3 and sys.version_info[1] >= 8:
            self.data = [
                '# Four Fundamental Operations ----- ----- -----', '+', '-', '*', '/', '//',
                '# Compare ----- ----- -----', '<', '>', '>=', '<=', '==', '!='
                '# Power ----- ----- -----', '!', '^', 'sqrt()',
                '# Other ----- ----- -----', 'x / y ... ?', 'Type',
                '# Trigonometric Function ----- ----- -----', 'cos()', 'sin()', 'tan()', 'acos()', 'asin()', 'atan()', 'dist()', 'hypot()',
                '# Hyperbolic Functions ----- ----- -----', 'acosh()', 'asinh()', 'atanh()', 'cosh()', 'sinh()', 'tanh()',
                '# Power And Logarithmic Functions ----- ----- -----', 'exp()', 'expm1()',
                '# Angular Conversion ----- ----- -----', 'Degrees', 'Radians',
                '# Type Conversion ----- ----- -----', 'Int / Float',
                '# Shortcuts ----- ----- -----', 'Successive Addition of Arithmetic Sequence'
                ]
        elif sys.version_info[0] == 3 and sys.version_info[1] >= 2 and sys.version_info[1] < 8:
            self.data = [
                '# Four Fundamental Operations ----- ----- -----', '+', '-', '*', '/', '//',
                '# Compare ----- ----- -----', '<', '>', '>=', '<=', '==', '!='
                '# Power ----- ----- -----', '!', '^', 'sqrt()',
                '# Other ----- ----- -----', 'x / y ... ?', 'Type',
                '# Trigonometric Function ----- ----- -----', 'cos()', 'sin()', 'tan()', 'acos()', 'asin()', 'atan()', 'dist()', 'hypot()',
                '# Hyperbolic Functions ----- ----- -----', 'acosh()', 'asinh()', 'atanh()', 'cosh()', 'sinh()', 'tanh()',
                '# Power And Logarithmic Functions ----- ----- -----', 'exp()', 'expm1()',
                '# Angular Conversion ----- ----- -----', 'Degrees', 'Radians',
                '# Type Conversion ----- ----- -----', 'Int / Float',
                '# Shortcuts ----- ----- -----', 'Successive Addition of Arithmetic Sequence'
                ]
        else:
            self.data = [
                '# Four Fundamental Operations ----- ----- -----', '+', '-', '*', '/', '//',
                '# Compare ----- ----- -----', '<', '>', '>=', '<=', '==', '!='
                '# Power ----- ----- -----', '!', '^', 'sqrt()',
                '# Other ----- ----- -----', 'x / y ... ?', 'Type',
                '# Trigonometric Function ----- ----- -----', 'cos()', 'sin()', 'tan()', 'acos()', 'asin()', 'atan()', 'dist()', 'hypot()',
                '# Hyperbolic Functions ----- ----- -----', 'acosh()', 'asinh()', 'atanh()', 'cosh()', 'sinh()', 'tanh()',
                '# Power And Logarithmic Functions ----- ----- -----', 'exp()', 'expm1()',
                '# Angular Conversion ----- ----- -----', 'Degrees', 'Radians',
                '# Type Conversion ----- ----- -----', 'Int / Float',
                '# Shortcuts ----- ----- -----', 'Successive Addition of Arithmetic Sequence'
                ]
        self.result = []
        # Value
        self.window = tk.Tk()
        self.window.title(title)
        self.window.minsize(300, 200)
        # Tkinter
        self.a = tk.Spinbox(self.window, from_=0.0, to=100000000.0)
        self.a.place(relx=0.25, rely=0.2, relheight=0.2, relwidth=0.5, anchor='center')
        self.b = tk.Spinbox(self.window, from_=0, to=100000000)
        self.b.place(relx=0.25, rely=0.4, relheight=0.2, relwidth=0.5, anchor='center')
        self.listbox = tk.Listbox(self.window)
        self.listbox.place(relx=0.2, rely=0.8, relheight=0.4, relwidth=0.4, anchor='center')
            # Left
        tk.Button(self.window,text='Delete Choosen Item',command=self.delete).place(relx=0.75,rely=0.1,anchor='center')
        tk.Button(self.window,text='Delete All',command=self.deleteALL).place(relx=0.75,rely=0.2,anchor='center')
        tk.Button(self.window,text='See Meaning',command=self.meaning).place(relx=0.75,rely=0.3,anchor='center')
        self.resultlb = tk.Listbox(self.window)
        self.resultlb.place(relx=0.7, rely=0.8, relheight=0.4, relwidth=0.6, anchor='center')
            # Right
        for item in self.data:
            self.listbox.insert('end', item)
        # Window
        self.window.bind('Double-ButtonRelease-3', sys._clear_type_cache)
        self.listbox.bind('<Double-ButtonRelease-1>', self.caculation)
        self.resultlb.bind('<Double-ButtonRelease-1>', self.set)
    def mainloop(self):
        if sys.version_info[0] == 3:
            for x in range(0, 100):
                self.window.attributes('-alpha', x / 100)
                self.window.update()
                time.sleep(0.001)
        elif sys.version_info[0] == 2:
            for x in range(0, 100):
                self.window.attributes('-alpha', 1 - x / 100)
                self.window.update()
                time.sleep(0.001)
        self.window.mainloop()
    def delete(self):
        get = self.resultlb.index('active')
        print(get)
        del self.result[get]
        self.resultlb.delete(get)
    def deleteALL(self):
        data = msgbox.askokcancel('','Realy ? Delete All ?')
        if data == True:
            self.result = []
            self.resultlb.delete(0,'end')
    def set(self, event):
        self.b.delete(0, 'end')
        self.b.insert('end', self.result[self.resultlb.curselection()[-1]])
    def meaning(self):
        try:
            data = self.data[self.listbox.curselection()[-1]]
            if data == '+':
                message = 'Find the sum of A and B, indicating A plus B'
            elif data == '-':
                message = 'Find the difference between A and B, which means A minus B'
            elif data == '*':
                message = 'Find the product of A and B, representing A times B'
            elif data == '/':
                message = 'The quotient of A and B, which means A divided by B'
            elif data == '//':
                message = 'Find the integer part of a divided by B'
            # Four Fundamental Operations
            elif data == '>':
                message = 'Find whether A is greater than B. If yes, return True; If not, False is returned'
            elif data == '<':
                message = 'Find whether A is less than B. If yes, return true; If not, false is returned'
            elif data == '==':
                message = 'Find whether A is equal to B. If yes, return true; If not, false is returned'
            elif data == '>=':
                message = 'Find whether A is greater than or equal to B. If yes, return true; If not, false is returned'
            elif data == '<=':
                message = 'Find whether A is less than or equal to B. If yes, return true; If not, false is returned'
            elif data == '!=':
                message = 'Find whether A is not equal to B. If yes, return true; If not, false is returned'
            # Compare
            elif data == '!':
                message = 'Find the factorial of A'
            elif data == '^':
                message = 'Seeking the b-th of a'
            elif data == 'sqrt()':
                message = 'Find the square root of A'
            # Power
            elif data == 'x / y ... ?':
                message = 'Find the remainder of a divided by B'
            elif data == 'Type':
                message = 'Returns the type of A, integer returns Int, decimal returns Float \n ( Note: if decimal part is 0, Int is returned )'
            # Other
            elif data == 'cos()':
                message = 'Return the cosine of x radians'
            elif data == 'sin()':
                message = 'Return the sine of x radians'
            elif data == 'tan()':
                message = 'Return the tangent of x radians'
            elif data == 'acos()':
                message = 'Return the arc cosine of A, in radians'
            elif data == 'asin()':
                message = 'Return the arc sine of A, in radians'
            elif data == 'atan()':
                message = 'Return the arc tangent of A, in radians'
            elif data == 'dist()':
                message = 'Return the Euclidean distance between two points A and B, \n each given as a sequence (or iterable) of coordinates. \n The two points must have the same dimension'
            elif data == 'hypot()':
                message = '''Return the Euclidean norm,
sqrt(sum(A**2 for A in coordinates)).
This is the length of the vector from the origin to the point given by the coordinates.
For a two dimensional point (A, B),
this is equivalent to computing the hypotenuse of a right triangle using the Pythagorean theorem, sqrt(A*A + B*B)'''
            # Trigonometric Function
            elif data == 'acosh()':
                message = 'Return the inverse hyperbolic cosine of A'
            elif data == 'asinh()':
                message = 'Return the inverse hyperbolic sine of A'
            elif data == 'atanh()':
                message = 'Return the inverse hyperbolic tangent of A'
            elif data == 'cosh()':
                message = 'Return the hyperbolic cosine of A'
            elif data == 'sinh()':
                message = 'Return the hyperbolic sine of A'
            elif data == 'tanh()':
                message = 'Return the hyperbolic tangent of A'
            # Hyperbolic Functions
            elif data == 'exp()':
                message = 'Return e raised to the power A, where e = 2.718281… is the base of natural logarithms. \n This is usually more accurate than math.e ** A or pow(math.e, A)'
            elif data == 'expm1()':
                message = '''Return e raised to the power A, minus 1.
Here e is the base of natural logarithms.
For small floats A, the subtraction in exp(A) - 1 can result in a significant loss of precision;
the expm1() function provides a way to compute this quantity to full precision:

>>> from math import exp, expm1
>>> exp(1e-5) - 1  # gives result accurate to 11 places
1.0000050000069649e-05
>>> expm1(1e-5)    # result accurate to full precision
1.0000050000166668e-05'''
            # Power And Logarithmic Functions
            elif data == 'Degrees':
                message = 'Convert angle A from radians to degrees'
            elif data == 'Radians':
                message = 'Convert angle A from degrees to radians'
            # Angular Conversion
            elif data == 'Int / Float':
                message = 'Force integer A to be converted to decimal, or convert decimal A to integer ( Note: if the decimal part of A is 0, A will be converted to decimal x.0 )'
            # Type Conversion
            elif data == 'Successive Addition of Arithmetic Sequence':
                message = '''For continuous addition operation,
the calculation starts from A and ends at B, and C is the equal difference sequence of the number of items.
The formula is: (A + B) * C / 2'''
            # Shortcuts
            elif data == '# Four Fundamental Operations ----- ----- -----'\
                 or data == '# Compare ----- ----- -----'\
                 or data == '# Power ----- ----- -----'\
                 or data == '# Other ----- ----- -----'\
                 or data == '# Trigonometric Function ----- ----- -----'\
                 or data == '# Hyperbolic Functions ----- ----- -----'\
                 or data == '# Power And Logarithmic Functions ----- ----- -----'\
                 or data == '# Angular Conversion ----- ----- -----'\
                 or data == '# Type Conversion ----- ----- -----'\
                 or data == '# Shortcuts ----- ----- -----':
                message = 'An index label'
            msgbox.showinfo('',message)
        except OSError:
            pass
    def caculation(self, event):
        data = self.data[self.listbox.curselection()[-1]]
        try:
            a = float(self.a.get())
            if a - int(a) == 0:
                a = int(a)
            b = float(self.b.get())
            if b - int(b) == 0:
                b = int(b)
            if data == '+':
                result = a + b
                message = '%s + %s = %s' % (a, b, result)
            elif data == '-':
                result = a - b
                message = '%s - %s = %s' % (a, b, result)
            elif data == '*':
                result = a * b
                message = '%s * %s = %s' % (a, b, result)
            elif data == '/':
                result = a / b
                message = '%s / %s = %s' % (a, b, result)
            elif data == '//':
                result = a // b
                message = '%s // %s = %s' % (a, b, result)
            elif data == '!':
                result = 1
                for x in range(1, a + 1):
                    result *= x
                message = '%s ! = %s' % (a, result)
            elif data == '^':
                result = a ** b
                message = '%s ^( %s ) = %s' % (a, b, result)
            elif data == 'sqrt()':
                result = math.sqrt(a)
                message = 'sqrt( %s ) = %s' % (a, result)
            # Four Fundamental Operations
            elif data == 'Type':
                result = type(a)
                message = 'Type %s = %s' % (a, result)
            elif data == 'x / y ... ?':
                result = a % b
                message = '%s / %s ... %s' % (a, b, result)
            # Other
            elif data == 'acos()':
                result = math.acos(a)
                message = 'acos( %s ) = %s' % (a, result)
            elif data == 'cos()':
                result = math.cos(a)
                message = 'cos( %s ) = %s' % (a, result)
            elif data == 'asin()':
                result = math.asin(a)
                message = 'asin( %s ) = %s' % (a, result)
            elif data == 'sin()':
                result = math.sin(a)
                message = 'sin( %s ) = %s' % (a, result)
            elif data == 'atan()':
                result = math.atan(a)
                message = 'atan( %s ) = %s' % (a, result)
            elif data == 'tan()':
                result = math.tan(a)
                message = 'tan( %s ) = %s' % (a, result)
            elif data == 'dist()':
                result = math.dist(a, b)
                message = 'dist( %s, %s ) == %s' % (a, b, result)
            elif data == 'hypot()':
                result = math.hypot(a, b)
                message = 'hypot( %s, %s ) = %s' % (a, b, result)
            # Trigonometric Function
            elif data == 'acosh()':
                result = math.acosh(a)
                message = 'acosh( %s ) == %s' % (a, result)
            elif data == 'asinh()':
                result = math.asinh(a)
                message = 'asinh( %s ) == %s' % (a, result)
            elif data == 'atanh()':
                result = math.atanh(a)
                message = 'atanh( %s ) == %s' % (a, result)
            elif data == 'cosh()':
                result = math.cosh(a)
                message = 'cosh( %s ) == %s' % (a, result)
            elif data == 'sinh()':
                result = math.sinh(a)
                message = 'sinh( %s ) == %s' % (a, result)
            elif data == 'tanh()':
                result = math.tanh(a)
                message = 'tanh( %s ) == %s' % (a, result)
            # Hyperbolic Functions
            elif data == 'exp()':
                result = math.exp(a)
                message = 'exp( %s ) = %s' % (a, result)
            elif data == 'expm1()':
                result = math.expm1(a)
                message = 'expm1( %s ) = %s' % (a, result)
            # Power And Logarithmic Functions
            elif data == '>':
                if a > b:
                    result = True
                else:
                    result = False
                message = '%s > %s = %s' % (a, b, result)
            elif data == '<':
                if a < b:
                    result = True
                else:
                    result = False
                message = '%s < %s = %s' % (a, b, result)
            elif data == '>=':
                if a >= b:
                    result = True
                else:
                    result = False
                message = '%s >= %s = %s' % (a, b, result)
            elif data == '<=':
                if a <= b:
                    result = True
                else:
                    result = False
                message = '%s <= %s = %s' % (a, b, result)
            elif data == '==':
                if a == b:
                    result = True
                else:
                    result = False
                message = '%s == %s = %s' % (a, b, result)
            elif data == '!=':
                if a != b:
                    result = True
                else:
                    result = False
                message = '%s != %s = %s' % (a, b, result)
            # Compare
            elif data == 'Degrees':
                result = math.degrees(a)
                message = 'Degrees %s = %s' % (a, result)
            elif data == 'Radians':
                result = math.radians(a)
                message = 'Radians %s = %s' % (a, result)
            elif data == 'Int / Float':
                if type(a) == type(1):
                    result = float(a)
                    message = 'Float %s = %s' % (a, result)
                elif type(a) == type(1.0):
                    result = int(a)
                    message = 'Int %s = %s' % (a, result)
            # Change
            elif data == 'Successive Addition of Arithmetic Sequence':
                ctk = tk.Tk()
                ctk.title('')
                ctk.resizable(0, 0)
                tk.Label(ctk, text='The Number of Items : ').grid(column=0, row=0)
                spinbox = tk.Spinbox(ctk, from_=1, to=10000)
                spinbox.grid(column=1, row=0)
                tk.Button(ctk, text='Pack', command=ctk.quit).grid(column=0, row=1, columnspan=2)
                ctk.mainloop()
                try:
                    c = int(spinbox.get())
                except:
                    if a > b:
                        c = a - b + 1
                    elif a < b:
                        c = b - a + 1
                    else:
                        c = 2
                try:
                    ctk.destroy()
                except:
                    pass
                result = (a + b) * c / 2
                message = '%s + ... + %s == %s' % (a, b, result)
            # Shortcuts
            elif data == '# Four Fundamental Operations ----- ----- -----'\
                 or data == '# Compare ----- ----- -----'\
                 or data == '# Power ----- ----- -----'\
                 or data == '# Other ----- ----- -----'\
                 or data == '# Trigonometric Function ----- ----- -----'\
                 or data == '# Hyperbolic Functions ----- ----- -----'\
                 or data == '# Power And Logarithmic Functions ----- ----- -----'\
                 or data == '# Angular Conversion ----- ----- -----'\
                 or data == '# Type Conversion ----- ----- -----'\
                 or data == '# Shortcuts ----- ----- -----':
                result = '/pass'
                message = '/pass'
            else:
                raise AttributeError('No attribute name " %s "' % data)
            # Add
            if result != '/pass' and message != '/pass':
                print(message)
                self.result.append(result)
                self.resultlb.insert('end', message)
            # Show
        except TypeError as msg:
            msgbox.showerror('Type Error', msg)
            print(msg)
        except ValueError as msg:
            msgbox.showerror('Value Error', msg)
            print(msg)
        except IndexError as msg:
            print(msg)
        except AttributeError as msg:
            msgbox.showerror('Attribute Error', msg)
            print(msg)
        except ZeroDivisionError as msg:
            msgbox.showerror('Zero Division Error', msg)
            print(msg)

Caculation().mainloop()
