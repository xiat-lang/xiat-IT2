#!/bin/python3 

import sys

def readf(file):
    with open(file, 'r') as f:
        return f.read()

class Node:
    def __init__(self, type: str = None, value: str = None, initc: list = None):
        self.type = type
        self.value = value
        self.children = initc if initc is not None else []
    def append(self, child): # maybe rename to push
        self.children.append(child)
    def pop(self):
        return self.children.pop()

def lexer(program):
    global i
    i = 0
    tokens = []
    
    def inc_safe() -> bool:
        global i
        i += 1
        return i >= len(program)

    def handle(ch: str) -> tuple[str, str]:
        if ch in "([{":
            return ("BLOCKOPEN", ch)
        elif ch in "}])":
            return ("BLOCKCLOSE", ch)
        elif ch in ".,": 
            return ("COMM", ch)
        elif ch == ';': # match case from here?
            return ("SEMI", ch)
        elif ch == '=':
            return ("SIGN", ch)
        elif ch == '$':
            return ("VARPTR", ch)
        elif ch == '+':
            return ("PLUS", ch)
        elif ch == '-':
            return ("SUBT", ch)
        elif ch == '*':
            return ("ASTE", ch)
        elif ch == '/':
            return ("SLASH", ch)
        elif ch == '>':
            return ("RIGHT", ch)
        elif ch == '<':
            return ("LEFT", ch)
        else:
            return ("CH", ch)
        
    while i < len(program):
    
        if program[i] == "\"":
            # add string to tokens
            temp = '"'
            
            while i < len(program):
                if inc_safe():
                    raise Exception("Unclosed string")
                if program[i] == '"':
                    temp += '"'
                    break
                temp += program[i]
            tokens.append(("STRLIT", temp))
            
        elif program[i] == '@':
            while i < len(program):
                if program[i] == "\n":
                    break
                i += 1
                
        elif program[i].isalnum():
            temp = ''
            file_ended = False
            while i < len(program):
                if not program[i].isalnum():
                    i -= 1 # i += 1 at the end of lexer's loop
                    break
                temp += program[i]
                if inc_safe():
                    tokens.append(temp)
                    file_ended = True
                    break
            tokens.append(("ALNUM", temp))
            
        elif program[i].isspace():
            if inc_safe():
                break
            continue
            
        else:
            tokens.append(handle(program[i]))
            
        inc_safe()
    return tokens

# class NodeCL(collections.UserList):
#     def __init__(children):
#         self.type = None
#         self.value = None
#         self.data = children


def parse(tokens):
    head = Node("ROOT", None)
    # global current, stack
    stack: list[Node] = [head] # since we only use push & pop, this could be a node...
    current = stack[0]
    # def push(node):
    #     global current, stack
    #     current.children.append(new_node)
    #     stack.append(current)
    #     current = new_node # link
    # def pop()
    # global current
    #     current = stack.pop()
    global i
    i = 0
    
    while i < len(tokens):
        kind, char = tokens[i][0], tokens[i][1] # zip(*tokens)
        
        if kind == "BLOCKOPEN":
            new_node = Node("BLOCK", char)
            current.children.append(new_node)
            stack.append(current)
            current = new_node # link
            
        elif kind == "BLOCKCLOSE":
            current = stack.pop()

        elif kind == "EQ":
            i += 1
            kind, char = tokens[i][0], tokens[i][1]
            if kind == "ALNUM":
                var_name = char
            else:
                raise Exception("Currently can only set variables")
            i += 1
            tok = tokens[i]
            var_value = tok # is copying ok here?

            new_node = Node("SETVAR", var_name)
            new_node.append(Node("ALNUM", var_name)) # make var_name a node, too?
            new_node.append(var_value) # var_value is a Node
                             
        # TODO: extend
        
        # elif kind == "VARPTR":
        #     i += 1
        #     kind, char = tokens[i][0], tokens[i][1]
        #     if kind == "ALNUM":
        #         var_name = char
        #     else:
        #         current.append(Node("VARPTR", "$"))
        #         continue
        #     i += 1
        #     kind, char = tokens[i][0], tokens[i][1]
        #     if kind == "EQ":
        #         new_node = Node("SETVAR", char)
        #         current.children.append(new_node)
        #         stack.append(current)
        #         current = new_node # link
        #         current.append(Node("VAR", var_name))
        #     else:
        #         raise Exception("Expected = after variable name")
        else:
            current.children.append(Node(kind, char))
            
        i += 1
        
    #print([(i.type, i.value) for i in stack])
    return head

def print_ast(head, ind=0):
    if head.type != "BLOCK":
        print("->" * ind, (head.type, head.value))
    for c in head.children:
        print_ast(c, ind + 2)

def print_flat(head):
    if head.type != "BLOCK":
        print(head.type, head.value)
    for c in head.children:
        print(c.type, c.value)

def run(head: Node, vo_nout=False):
    variables: dict[str, str] = {}
    functions: dict[str, Node] = {}
    i: int = 0
    stack: list[Node] = []
    Cchild: Node = head.children # current children

    def evalcomp(N: list[Node]):
        j = 0
        t: list[str] = []
        while j < len(N):
            kind = N[j].type
            if j + 1 < len(N):
                nxkind = N[j+1].type
            else:
                nxkind = ""
            # nxkind, nxval = N[j+1].type, N[j+1].value
        
            if kind == "VARPTR":
                t.append(variables[N[j+1].value])
                
            elif kind == "SIGN" and nxkind == "SIGN":
                a, b = t.pop(), N[j+2].value
                t.append(a == b)
                j += 2
                
            elif kind == "SIGN" and nxkind == "SUBT": # =- ???
                a, b = t.pop(), N[j+2].value
                t.append(a != b)
                j += 2
                
            elif kind == "LEFT":
                a, b = t.pop(), N[j+1].value # kinda weird how SETVAR is polish notation, yet these are infix.
                t.append(str(int(a) < int(b))) # NOTE: error handling
                j += 1
                
            elif kind == "RIGHT":
                a, b = t.pop(), N[j+1].value
                t.append(str(int(a) > int(b)))
                j += 1
                
            j += 1
        return t.pop()
    
    while i < len(Cchild):
        
        if Cchild[i].type == 'SIGN':
            name = Cchild[i+1]
            value = Cchild[i+2]
            variables[name.value] = value.value
            i += 3
            
        elif Cchild[i].value == "if":
            IfHead = Cchild[i+1]
            IfBody = Cchild[i+2]
            if evalcomp(IfHead.children):
                stack.append((i+3, Cchild))
                Cchild = IfBody.children
                i = -1
            else:
                i += 3

        elif Cchild[i].value == "fc":
            fcname: str = Cchild[i + 1].value
            fcargs: Node = Cchild[i + 2]
            fcbody: Node = Cchild[i + 3]
            functions[fcname] = Node("FUNCTION", fcname, [fcargs, fcbody])
            i += 3 # i += 1 at the end of the loop

        elif Cchild[i].value == "print":
            t = ""
            j = 0
            while j < len(Cchild[i+1].children):
                t += Cchild[i+1].children[j].value.replace('"', '')
                j += 1
            if not vo_nout:
                print(t)
            i += 1
# <<<<<<< HEAD
#         elif Cchild[i].value in functions:
#             func: Node = functions[Cchild[i].value]
#             fargs: list[Node] = func.children[0].children
#             fbody: list[Node] = func.children[1].children
#             callargs: list[Node] = Cchild[i+1].children
#             if len(fargs) != len(callargs):
#                 raise Exception(f"Function {func.value} expects {len(fargs)} arguments,\
#                     got {callargs} ({len(callargs)} arguments)")
#             # set args
#             for j in range(len(fargs)):
#                 variables[fargs[j].value] = callargs[j].value
#             stack.append((i+2, Cchild))
#             Cchild = fbody
#             i = -1 # will become 0 at the end of the loop
# =======
            if not vo_nout:
                print(t)
            i += 1

        elif Cchild[i].value == 'fc':
            name = Cchild[i+1]
            arguments = Cchild[i+2]
            code = Cchild[i+3]
            functions[name.value] = (arguments, code)
            i += 3

        elif Cchild[i].value in functions: # TODO: make local varibles possible
            Fhead = functions[Cchild[i].value][0]
            Fbody = functions[Cchild[i].value][1]
            stack.append((i+2, Cchild))
            Cchild = Fbody.children
            i = -1
# >>>>>>> parent of 2377218 (broke some things, but stack trace added)

        i += 1
        if i >= len(Cchild) and stack:
            i, Cchild = stack.pop()

def parse_flags(args): # parse_flags
    flag = []
    for arg in enumerate(args): # list of (val, idx)
        if arg[1][0] == '-':
            if arg[1][1] == '-':
                if arg[0] == len(args) - 1:
                    flag.append(arg[1])
                else:
                    flag.append(f"{arg[1]} {args[arg[0] + 1]}")
            else:
                for i in arg[1][1:]:
                    flag.append(f"-{i}")
        else:
            flag.append(arg[1])
    return [True, flag]

if __name__ == "__main__":
    flags: list[bool, list[str]] = [False, []]
    if len(sys.argv) < 2:
        raise Exception("Deficient arguments. Try --help?")
        
    flags = parse_flags(sys.argv[1:])

    if "--help" in flags[1] or "-h" in flags[1]:
        print(readf("help.txt")) # DUDE... what if we made a man page for this?
        exit()

    program = readf(sys.argv[1])
    tokens = lexer(program)

    if "--vopt tokens" in flags[1]:
        for t in tokens:
            print(t)

    ast = parse(tokens)

    if "--vopt syntaxt" in flags[1] or "-v" in flags[1]:
        print_ast(ast)
    if "--vopt syfl" in flags[1] or "-v" in flags[1]:
        print_flat(ast)
    if "--nout" in flags[1]:
        run(ast, True)
    else:
        run(ast)

