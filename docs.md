
# Table of contents:

- [Table of contents:](#table-of-contents)
- [Starting point](#starting-point)
	- [Testing, testing, 1, 2, 3...](#testing-testing-1-2-3)
	- [First program](#first-program)
		- [Background proccesses](#background-proccesses)
- [Documentation](#documentation)
	- [Statements](#statements)
		- [Variables](#variables)
		- [Branches](#branches)
	- [Expressions](#expressions)
		- [Variables](#variables-1)
		- [Comparisons](#comparisons)
	- [Interpetation](#interpetation)
		- [Tokens](#tokens)
		- [Syntax tree](#syntax-tree)
		- [Execution](#execution)


# Starting point

Hello! This is the XIAT programming language.
Specifically, the second iteration, written in Python 3.0.
It is currently a work in progress, and contributions are recommended.
Any reports should be directed to [here](https://github.com/xiat-lang/xiat-IT2/issues).
There is an HTML version of this Markdown coming soon (and maybe a man page).

## Testing, testing, 1, 2, 3...
You can check the interpreter by running:
```
python3 check.py
```

## First program

Create the file `hello.xiat`, and write this familliar but odd line:
```
print("hello"); @ comment!
```
and run (bash/zsh is preferred) with:
```
python3 main.py hello.xiat
```

### Background proccesses

Now this got tokenized as:
```
('ALNUM', 'print')
('BLOCKOPEN', '(')
('STRLIT', '"hello"')
('BLOCKCLOSE', ')')
('SEMI', ';')
```
You can see this by running `python main.py docs/hello.xiat --vopt tokens`.

This then gets parsed as:
```
('ROOT', None)
	('ALNUM', 'print')
		('STRLIT', '"hello"')
	('SEMI', ';')
```
You can see this by changing the flag to `--vopt syntaxt`.

# Documentation

This documentation is tentative, id est it is likely to change in the near future.

## Statements

### Variables

You set a variable by using the `=` operator in Polish notation, like this:
```
=var exp;
```
Note how we did not use `$`. That is for dereferencing it (See Expressions)

### Branches

TODO

## Expressions

### Variables

Currently, all variables contain strings that are converted when needed.

You dereference a variable name using the `$` operator, prefix.
This is currently only evaluated in if statements, which
there is a demonstration of in `test/ifcomp.xiat`.

### Comparisons

Suprisingly, comparisons are only evaluated once needed,
and thus their values are only ever accesed by the interpreter.
Therefore, there are no direct Booleans in the language.

These operators compare tokens as strings.
- `==` checks for equality.
- `!=` checks for inequality.

These operators compare tokens as integers using Python's `int` function.
The failure of these checks is therefore dependent on it.
- `<` checks for truth of the mathematical 'less than' operator.
- `>` checks for truth of the mathematical 'greater than' operator.

## Interpetation

The program that is interpreted first gets a lexical analysis,
and is proccesed into tokens. these tokens are then parsed into an
abstract syntax tree. The tree is then passed to a running
procedure, where external procceses are ran throughit.

### Tokens

Tokens are stored in an ordered pair as `('TOKENNAME', ch)`.
Here is the EBNF of the tokens, lowercase:
```
strlit = '"', ? Anything except '"' ?, '"';
alnum = ? /[:alnum:]/ in RegEx ?+;
blockopen = '[' | '(' | '{';
blockclose = ']' | ')' | '}';
comm = '.' | ',';
semi = ';';
equal = '=';
varptr = '$';
plus = '+';
minus = '-';
star = '*';
slash = '/';
cright = '>';
cleft = '<';
```
The `'CH'` token is the general character token.

### Syntax tree

TODO

### Execution

TODO
