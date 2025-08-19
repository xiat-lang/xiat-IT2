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
		
	def handle(ch): # from enum import Enum
		if ch in '([{':
			return ('BLOCKOPEN', ch)
		elif ch in '}])':
			return ('BLOCKCLOSE', ch)
		elif ch in '.,':
			return ('COMM', ch)
		elif ch == ';':
			return ('SEMI', ch)
		elif ch == '$':
			return ('VARPTR', ch)
		elif ch == '+':
			return ('PLUS', ch)
		elif ch == '-':
			return ('SUBT', ch)
		elif ch == '*':
			return ('ASTE', ch)
		elif ch == '/':
			return ('SLASH', ch)
		elif ch == '=':
			return ('EQ', ch)
		else:
			return ('CH', ch)
		# return (x, ch)
			
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
		elif program[i] == '@':
			while i < len(program):
				if program[i] == '\n':
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
			tokens.append(('ALNUM', temp))
		elif program[i].isspace():
			if inc_safe():
				break
			continue
		else:
			tokens.append(handle(program[i]))
		i += 1
	return tokens

# class NodeCL(collections.UserList):
# 	def __init__(children):
# 		self.type = None
# 		self.value = None
# 		self.data = children

class Node:
	def __init__(self, type=None, value=None):
		self.type = type
		self.value = value
		self.children = []
	def append(self, child):
		self.children.append(child)
	def pop():
		return self.children.pop()

def parse(tokens):
	head = Node('ROOT', None)
	# global current, stack
	stack = [head]
	current = stack[0]
	# def push(node):
	# 	global current, stack
	# 	current.children.append(new_node)
	# 	stack.append(current)
	# 	current = new_node # link
	# def pop()
	# global current
	# 	current = stack.pop()
	i = 0
	while i < len(tokens):
		kind, char = tokens[i][0], tokens[i][1]
		if kind == 'BLOCKOPEN':
			new_node = Node('BLOCK', char)
			current.children.append(new_node)
			stack.append(current)
			current = new_node # link
		elif kind == 'BLOCKCLOSE':
			current = stack.pop()
		elif kind == 'VARPTR':
			i += 1
			kind, char = tokens[i][0], tokens[i][1]
			if kind == 'ALNUM':
				var_name = char
			else:
				current.append(Node('VARPTR', '$'))
				continue
			i += 1
			kind, char = tokens[i][0], tokens[i][1]
			if kind == 'EQ':
				new_node = Node('SETVAR', char)
				current.children.append(new_node)
				stack.append(current)
				current = new_node # link
				current.append(Node('VAR', var_name))
			else:
				raise Exception('Expected = after variable name')
		else:
			current.children.append(Node(kind, char))
			if current.type == 'SETVAR':
				current = stack.pop()
		i += 1
	print([(i.type, i.value) for i in stack])
	return head

def print_ast(head, ind=0):
	if head.type != 'BLOCK':
		print('`' * ind, (head.type, head.value))
	for c in head.children:
		print_ast(c, ind + 2)

def print_flat(head):
	if head.type != 'BLOCK':
		print(head.type, head.value)
	for c in head.children:
		if c.type != 'BLOCK':
			print(c.type, c.value)

def run(head):
	pass

if __name__ == '__main__':
	program = readf(sys.argv[1])
	tokens = lexer(program)
	ast = parse(tokens)
	# ast.children[0]'s child is its own self.
	# print("ast.children[0] is ast.children[0].children[0]:",
	# 	ast.children[0] is ast.children[0].children[0])
	print_ast(ast)
	print_flat(ast)
	run(ast)
