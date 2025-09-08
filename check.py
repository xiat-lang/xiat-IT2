import subprocess
import sys

def test(command, expect, file=None):
    result = subprocess.run(command, capture_output=True, text=True)
    # assert result.stdout.strip() != expect.strip(), f"command: {file} dint match expected:\n{expect}\nbut got:\n{result.stdout}"
    if result.stdout.strip() != expect.strip():
        print(f"command: {file} did'nt match expected:\n{expect}\nbut got:\n{result.stdout}", file=sys.stderr)
    else:
        print(f"file: {file} matched!\n")

if __name__ == '__main__':    
    # python3 main.py test/lexer.xiat --nout --vopt tokens
    test(["python3", "main.py", "test/lexer.xiat", "--nout", "--vopt", "tokens"],
"('STRLIT', '\"abc\"')\n\
('ALNUM', 'a')\n\
('ALNUM', 'a')\n\
('VARPTR', '$')\n\
('ALNUM', 'a')\n\
('ALNUM', 'func')\n\
('BLOCKOPEN', '(')\n\
('STRLIT', '\"arg\"')\n\
('COMM', ',')\n\
('ALNUM', '1')\n\
('BLOCKCLOSE', ')')", "lexer.xiat")

    # python3 main.py test/lexer.xiat --nout --vopt syntaxt
    test(["python3", "main.py", "test/parser.xiat", "--nout", "--vopt", "syntaxt"],
" ('ROOT', None)\n\
`````` ('STRLIT', '\"HAI\"')\n\
```````` ('ALNUM', '1')\n\
```````` ('COMM', ',')\n\
```````` ('ALNUM', '2')", "parser.xiat")    

