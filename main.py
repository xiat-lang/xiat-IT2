import sys

def readf(file):
    with open(file, 'r') as f: return f.read()

def lexer(program):
    i = 0
    tokens = []
    while i < len(program):
        if program[i] == '\"':
            temp = ''
            while i < len(program):
                temp += program[i]
                i += 1
                if program[i] == '"': break
            temp += program[i]
            tokens.append(temp)
        elif program[i].isalnum():
            temp = ''
            while i < len(program):
                if not program[i].isalnum(): break
                temp += program[i]
                i += 1
            i -= 1
            tokens.append(temp)
        elif program[i] == '@':
            while i < len(program):
                i += 1
                if program[i] == '\n': break
        elif not program[i].isspace():
            tokens.append(program[i])
        i += 1
    return tokens
def run(tokens):
    ...
if __name__ == '__main__':
    program = readf(sys.argv[1])
    tokens = lexer(program)
    #for t in tokens: print(t)
