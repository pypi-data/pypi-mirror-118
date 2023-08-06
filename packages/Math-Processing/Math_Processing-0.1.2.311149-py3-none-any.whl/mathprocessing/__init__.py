import cmath
import math

class Mathematical_constant:
    e = math.e
    minus_e = 0 - math.e
    #
    pi = math.pi
    minus_pi = 0 - math.pi
    #
    tau = math.tau
    minus_tau = 0 - math.tau
    #
    inf = math.inf
    minus_inf = 0 - math.inf
    #
    nanj = cmath.nanj
    #
    nan = math.nan
class MC:
    e = math.e
    minus_e = 0 - math.e
    #
    pi = math.pi
    minus_pi = 0 - math.pi
    #
    tau = math.tau
    minus_tau = 0 - math.tau
    #
    inf = math.inf
    minus_inf = 0 - math.inf
    #
    nanj = cmath.nanj
    #
    nan = math.nan

from .math import *

class Number():
    def __init__(self, number=0):
        self.number = number
    def get(self):
        return self.number
    def set(self, number):
        self.number = number
    #
    def use(self, mode, x=0):
        run(mode, self.number, x)
    #
    def floating_point_numbers_retain_decimal_digit(self, decimal_digit=2):
        dd = decimal_digit
        a = 10 ** dd * self.number
        a = int(a)
        a /= 10 ** dd
        self.number = a
    def floatdd(self, decimal_digit=2):
        self.floating_point_numbers_retain_decimal_digit(decimal_digit)
    #
    def reserved_digits(self, digit=2):
        if digit > 0:
            a = self.number / ( 10 ** digit )
            a = int(a)
            a *= 10 ** digit
            self.number = a
        elif digit < 0:
            self.floating_point_numbers_retain_decimal_digit(abs(digit))
        else:
            pass
    def rd(self, digit=2):
        self.reserved_digits(digit)
    #
    def rounding(self, digit=2):
        if type(self.number) == type(1):
            index = 0 - digit
            self.number = str(self.number)
            if int(self.number[index]) >= 5:
                self.number = float(self.number)
                self.number = self.number / ( 10 ** digit )
                self.number = int(self.number)
                self.number += 1
                self.number *= 10 ** digit
            else:
                self.number = float(self.number)
                self.number = self.number / ( 10 ** digit )
                self.number = int(self.number)
                self.number *= 10 ** digit
        elif type(self.number) == type(0.1):
            self.number = str(self.number)
            a = len(self.number) - len(str(int(float(self.number)))) - 1
            if digit <= a:
                index = 0 - digit
            elif digit > a:
                index = 0 - digit - 1
            if int(self.number[index]) >= 5:
                self.number = float(self.number)
                self.number *= 10 ** digit
                self.number = int(self.number)
                self.number += 1
                self.number = self.number / ( 10 ** digit )
            else:
                self.number = float(self.number)
                self.number *= 10 ** digit
                self.number = int(self.number)
                self.number = self.number / ( 10 ** digit )
