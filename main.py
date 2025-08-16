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
			tokens.append(temp)
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
				tokens.append(temp)
		elif program[i] == '@':
			# i recommend that you use # or // for comments.
			while i < len(program):
				if program[i] == '\n':
					tokens.append('\n')
					break
				i += 1
		elif program[i] == ' ':
			if inc_safe():
				break
			continue
		else:
			tokens.append(program[i])
		i += 1
	return tokens


def run(tokens):
	pass


if __name__ == '__main__':
	program = readf(sys.argv[1])
	tokens = lexer(program)
	print(tokens)
