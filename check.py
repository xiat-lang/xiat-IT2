import subprocess
import sys
import main

exit_code = 0

def test(command: str, expect: str, file: str = None):
    result = subprocess.run(command, capture_output=True, text=True)
    # assert result.stdout.strip() != expect.strip(), f"command: {file} dint match expected:\n{expect}\nbut got:\n{result.stdout}"
    if result.stdout.strip() != expect.strip():
        print(f"""
command: {file}
was expected to match:
{expect}
but got:
{result.stdout}"""
        , file=sys.stderr)
        global exit_code
        exit_code = max(result.returncode, 1)
    else:
        print(f"file {file} matched!")
        
def test2(file: str, expect: str): # uses import module main
    argv = ["main.py", file, "--nout", "--vopt", "tokens"]
    result = main.main(argv) # until it can return something useful, this can't be used
    if result.strip() != expect.strip():
        print(f"""
command: {file}
was expected to match:
{expect}
but got:
{result}"""
        , file=sys.stderr)
        global exit_code
        exit_code = 1
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
('BLOCKCLOSE', ')')"""
    , "lexer.xiat")

    # python3 main.py test/lexer.xiat --nout --vopt syntaxt
    test(["python3", "main.py", "test/parser.xiat", "--nout", "--vopt", "syntaxt"],
"""('ROOT', None)
->->-> ('STRLIT', '\"HAI\"')
->->->-> ('ALNUM', '1')
->->->-> ('COMM', ',')
->->->-> ('ALNUM', '2')"""
    , "parser.xiat")
    exit(exit_code)

