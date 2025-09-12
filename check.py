import subprocess
import sys

def test(command: str, expect: str, file: str = None):
    result = subprocess.run(command, capture_output=True, text=True)
    # assert result.stdout.strip() != expect.strip(), f"command: {file} dint match expected:\n{expect}\nbut got:\n{result.stdout}"
    if result.stdout.strip() != expect.strip():
        print(f"""
command: {file}
was expected to match:
{expect}
but got:
{result.stdout}""",
        file=sys.stderr)
    else:
        print(f"file {file} matched!")

if __name__ == '__main__':    
    # python3 main.py test/lexer.xiat --nout --vopt tokens
    test(["python3", "main.py", "test/lexer.xiat", "--nout", "--vopt", "tokens"],
"""('STRLIT', '\"abc\"')
('ALNUM', 'a')
('ALNUM', 'a')
('VARPTR', '$')
('ALNUM', 'a')
('ALNUM', 'func')
('BLOCKOPEN', '(')
('STRLIT', '\"arg\"')
('COMM', ',')
('ALNUM', '1')
('BLOCKCLOSE', ')')""", "lexer.xiat")

    # python3 main.py test/lexer.xiat --nout --vopt syntaxt
    test(["python3", "main.py", "test/parser.xiat", "--nout", "--vopt", "syntaxt"],
"""('ROOT', None)
->->-> ('STRLIT', '\"HAI\"')
->->->-> ('ALNUM', '1')
->->->-> ('COMM', ',')
->->->-> ('ALNUM', '2')""",
"parser.xiat")    

