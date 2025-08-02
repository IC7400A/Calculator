# core/evaluator.py
# A proper mathematical expression evaluator using the Shunting-yard algorithm.

import math
import re
from core.interface import lib

class Evaluator:
    def __init__(self, is_rad_mode=False):
        self.is_rad = is_rad_mode
        self.precedence = {'+': 1, '-': 1, 'x': 2, '/': 2, '%': 2, '^': 3}
        self.functions = self._get_functions()
        self.constants = {'π': math.pi, 'e': math.e}

    def _get_functions(self):
        # Use C library if available, otherwise fall back to Python's math module.
        if lib:
            return {
                'sin': (lib.sine, 1), 'cos': (lib.cosine, 1), 'tan': (lib.tangent, 1),
                'asin': (lib.arcsin, 1), 'acos': (lib.arccos, 1), 'atan': (lib.arctan, 1),
                'sinh': (lib.sinh_, 1), 'cosh': (lib.cosh_, 1), 'tanh': (lib.tanh_, 1),
                'asinh': (lib.asinh_, 1), 'acosh': (lib.acosh_, 1), 'atanh': (lib.atanh_, 1),
                'ln': (lib.natural_log, 1), 'log': (lib.base10_log, 1), '√': (lib.root, 1),
                '!': (lib.factorial, 1), 'exp': (lib.exp_func, 1),
                'x²': (lib.power_of_two, 1), 'x⁻¹': (lib.inverse, 1)
            }
        else: # Python fallback
            rad_conv = lambda x: x if self.is_rad else math.radians(x)
            deg_conv = lambda x: x if self.is_rad else math.degrees(x)
            return {
                'sin': (lambda x: math.sin(rad_conv(x)), 1), 'cos': (lambda x: math.cos(rad_conv(x)), 1),
                'tan': (lambda x: math.tan(rad_conv(x)), 1), 'asin': (lambda x: deg_conv(math.asin(x)), 1),
                'acos': (lambda x: deg_conv(math.acos(x)), 1), 'atan': (lambda x: deg_conv(math.atan(x)), 1),
                'sinh': (math.sinh, 1), 'cosh': (math.cosh, 1), 'tanh': (math.tanh, 1),
                'asinh': (math.asinh, 1), 'acosh': (math.acosh, 1), 'atanh': (math.atanh, 1),
                'ln': (math.log, 1), 'log': (math.log10, 1), '√': (math.sqrt, 1),
                '!': (lambda x: float(math.factorial(int(x))), 1), 'exp': (math.exp, 1),
                'x²': (lambda x: x**2, 1), 'x⁻¹': (lambda x: 1/x if x != 0 else float('nan'), 1)
            }

    def _apply_op(self, ops, values):
        op = ops.pop()
        if op in self.functions:
            func, num_args = self.functions[op]
            args = [values.pop() for _ in range(num_args)]
            if lib and op in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan']:
                args.append(1 if self.is_rad else 0)
            values.append(func(*reversed(args)))
        else:
            right, left = values.pop(), values.pop()
            op_map = {
                '+': (lambda a, b: a + b), '-': (lambda a, b: a - b),
                'x': (lambda a, b: a * b), '/': (lambda a, b: a / b),
                '%': (lambda a, b: a % b), '^': (lambda a, b: a ** b),
            }
            if lib:
                op_map = {'+': lib.add, '-': lib.sub, 'x': lib.mul, '/': lib.divide, '%': lib.modulo, '^': lib.power}
            
            values.append(op_map[op](left, right))

    def evaluate(self, expression):
        tokens = self._tokenize(expression)
        values, ops = [], []
        for token in tokens:
            if isinstance(token, (int, float)): values.append(token)
            elif token in self.constants: values.append(self.constants[token])
            elif token == '(': ops.append(token)
            elif token == ')':
                while ops and ops[-1] != '(': self._apply_op(ops, values)
                if ops: ops.pop()
            elif token in self.functions: ops.append(token)
            else: # Operator
                while ops and ops[-1] != '(' and self.precedence.get(ops[-1], 0) >= self.precedence.get(token, 0):
                    self._apply_op(ops, values)
                ops.append(token)
        
        while ops:
            self._apply_op(ops, values)
        return values[0] if values else 0

    def _tokenize(self, expression):
        # Improved tokenizer to handle special characters
        expression = expression.replace('x²', '(^2)').replace('x⁻¹', '(^-1)')
        
        token_specification = [
            ('NUMBER',   r'\d+(\.\d*)?'),
            ('CONSTANT', r'π|e'),
            ('FUNC',     r'[a-zA-Z√!²⁻¹]+'),
            ('OP',       r'[+\-x/%^()]'),
            ('MISMATCH', r'.'),
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        tokens = []
        for mo in re.finditer(tok_regex, expression):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'NUMBER': tokens.append(float(value))
            elif kind in ['CONSTANT', 'FUNC', 'OP']: tokens.append(value)
            elif kind == 'MISMATCH': raise RuntimeError(f'Unexpected character: {value}')
        return tokens