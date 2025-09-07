import subprocess
import sys

def test(command, expect, file=None):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.stdout.strip() != expect.strip():
        sys.stderr.write(f"command: {file} dint match expected:\n{expect}\nbut got:\n{result.stdout}")
    else:
        sys.stdout.write(f"file: {file} matched!\n")

if __name__ == '__main__':    
    test(["python3", "main.py", "test/lexer.xiat", "-nout", "-vtt"],"('STRLIT', '\"abc\"')\n('ALNUM', 'a')\n('ALNUM', 'a')\n('VARPTR', '$')\n('ALNUM', 'a')\n('ALNUM', 'func')\n('BLOCKOPEN', '(')\n('STRLIT', '\"arg\"')\n('COMM', ',')\n('ALNUM', '1')\n('BLOCKCLOSE', ')')","lexer.xiat")
    test(["python3", "main.py", "test/parser.xiat", "-nout", "-vsynt"],
    " ('ROOT', None)\n`````` ('STRLIT', '\"HAI\"')\n```````` ('ALNUM', '1')\n```````` ('COMM', ',')\n```````` ('ALNUM', '2')","parser.xiat")    

