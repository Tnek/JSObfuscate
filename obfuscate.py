#!/usr/bin/python3
import random
import sys

from slimit.parser import Parser
from slimit.visitors import nodevisitor
from slimit import ast
from slimit import minify

import boolean_obfuscator
import number_obfuscator
import string_obfuscator


def lvl1(src):
    parser = Parser()
    tree = parser.parse(src)
    for node in nodevisitor.visit(tree):
        #: Obfuscate all constants
        if isinstance(node, ast.Boolean):
            node.value = str(boolean_obfuscator.make_expression(node.value.lower() == 'true', random.randint(5,20)))
        if isinstance(node, ast.Number):
            node.value = str(number_obfuscator.make_expression(int(node.value), random.randint(5, 8)))
        if isinstance(node, ast.String):
            node.value = string_obfuscator.obfuscate_string(str(node.value[1:-1]))
    return tree.to_ecma() # print awesome javascript :)

def lvl2(src):
    pass

def obfuscate_js(src, times=1):
    """ Goes through every level of obfuscation """
    for i in range(times):
        for level in lvls:
            src = level(src)
    return src

def main():
    with open("asdf.js", "r") as FILE:
        src = FILE.read()
    src = lvl1(src)
    print(src)

    with open("lol.js", "w") as FILE:
        FILE.write(minify(src, mangle=True))

if __name__ == "__main__":
    main()
