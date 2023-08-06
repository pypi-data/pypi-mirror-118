def message():
    msg = '''
Name : Math-Processing
Version : 0.1.2.311149
Author : Yile Wang
Copyright : Yile Wang
License : GNU General Public License 3.0
Python Requires : At least Python 2.7
'''
    return msg

def license():
    LICENSE = '''
Math-Processing
Copyright (C) 2021  Yile Wang
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
    return LICENSE

def open_sourse(module=None):
    if module == None:
        return (open_sourse('__init__'), open_sourse('math'), open_sourse('system'))
    elif module == '__init__' or module == 'mathprocessing':
        return open('__init__.py').read()
    elif module == 'caculation':
        return open('caculation/__init__.py').read()
    elif module == 'caculation.service':
        return open('caculation/service.py').read()
    elif module == 'math':
        return open('math.py').read()
    elif module == 'system':
        return open('system.py').read()
    else:
        raise ModuleNotFoundError('Module \'%s\' not found' % module)
