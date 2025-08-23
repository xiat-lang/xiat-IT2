import sys


def readf(file):
	with open(file, 'r') as f:
		return f.read()


def lexer(program):
	global i
	i = 0
	tokens = []
	def inc_safe():
		global i
		i += 1
		return i >= len(program)
	def Handle(ch):
		if ch in '([{': return ('BLOCKOPEN', ch)
		elif ch in '}])': return ('BLOCKCLOSE', ch)
		elif ch in '.,': return ('COMM', ch)
		elif ch == ';': return ('SEMI', ch)
		elif ch == '=': return ('SIGN', ch)
		elif ch == '$': return ('VARPTR', ch)
		elif ch == '+': return ('PLUS', ch)
		elif ch == '-': return ('SUBT', ch)
		elif ch == '*': return ('ASTE', ch)
		elif ch == '/': return ('SLASH', ch)
		elif ch == '>': return ('RIGHT', ch)
		elif ch == '<': return ('LEFT', ch)
		else: return ('CH', ch)
	while i < len(program):
		if program[i] == '\"':
			# add string to tokens
			temp = '"'
			while i < len(program):
				if inc_safe():
					raise Exception('Unclosed string')
				if program[i] == '"':
					temp += '"'
					break
				temp += program[i]
			tokens.append(('STRLIT', temp))
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
			if not file_ended:
				tokens.append(('ALNUM', temp))
		elif program[i] == '@':
			# i recommend that you use # or // for comments. #update: we aredy use // for int div
			# # will be for macros
			# also @ is cool
			while i < len(program):
				if program[i] == '\n':
					break
				i += 1
		elif program[i].isspace(): # any space
			if inc_safe():
				break
			continue
		else:
			tokens.append(Handle(program[i]))
		i += 1
	return tokens


class Node:
	def __init__(self, type=None, value=None, children=None):
		self.type = type
		self.value = value
		self.children = children if children else []

def parse(tokens):
	Head = Node('ROOT', '???')
	stack = [Head]
	current = Head
	i = 0
	while i < len(tokens):
		if tokens[i][0] == 'BLOCKOPEN':
			new_node = Node('BLOCK', '{')
			current.children.append(new_node)
			stack.append(current)
			current = new_node
		elif tokens[i][0] == 'BLOCKCLOSE':
			current = stack.pop()
		else:
			current.children.append(Node(tokens[i][0], tokens[i][1]))
		i += 1
	return Head

def print_ast(head, ind=0):
    if head.type != 'BLOCK':
        print(' '*ind, (head.type, head.value))
    for c in head.children:
        print_ast(c, ind+2)
def print_flat(head):
	if head.type != 'BLOCK':
		print(head.type, head.value)
	for c in head.children:
		print(c.type, c.value)

def run(head):
	varibles = {}
	i = 0
	stack = []
	Cchild = head.children
	def Is(command, expect):
		if command == expect:
			return True
		return False
	def stdoutprintxiat(Node):
		t = ""
		j = 0
		while j < len(Node):
			t += Node[j].value.replace('"','')
			j += 1
		print(t)
	def evalcomp(N):
		j = 0
		t = []
		while j < len(N):
			if N[j].type == 'VARPTR':
				t.append(varibles[N[j+1].value])
			elif N[j].type == 'SIGN' and N[j+1].type == 'SIGN':
				a, b = t.pop(), N[j+2].value
				t.append(a == b)
				j += 2
			elif N[j].type == 'SIGN' and N[j+1].type == 'SUBT':
				a, b = t.pop(), N[j+2].value
				t.append(a != b)
				j += 2
			elif N[j].type == 'LEFT':
				a, b = t.pop(), N[j+1].value
				t.append(str(int(a) < int(b)))
				j += 1
			elif N[j].type == 'RIGHT':
				a, b = t.pop(), N[j+1].value
				t.append(str(int(a) > int(b)))
				j += 1
			j += 1
		return t.pop()
	
	while i < len(Cchild):
		if Cchild[i].type == 'SIGN':
			name = Cchild[i+1]
			value = Cchild[i+2]
			varibles[name.value] = value.value
			i += 3
		elif Is(Cchild[i].value, 'if'):
			IfHead = Cchild[i+1]
			IfBody = Cchild[i+2]
			if evalcomp(IfHead.children):
				stack.append((i+3, Cchild))
				Cchild = IfBody.children
				i = -1
			else:
				i += 3
		elif Is(Cchild[i].value, 'print'):
			stdoutprintxiat(Cchild[i+1].children)
			i += 1
		i += 1
		if i >= len(Cchild) and stack:
			i, Cchild = stack.pop()
	
if __name__ == '__main__':
	program = readf(sys.argv[1])
	tokens = lexer(program)
	ast = parse(tokens)
	#print_ast(ast)
	#print_flat(ast)
	run(ast)
