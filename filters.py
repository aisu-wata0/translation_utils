import re

block_start = r"((^|\n)[ \t]*)"
block_cont = r"([ \t]+[^\n]*\n)*"
block_cont_s = r"([^\S\r\n]*\n[ \t]+[^\n]+)"
block_nl = r"[^\S\r\n]*\n"

code_patterns = [
    r'```.*?```',           # Match triple backtick code blocks
    r'`.*?`',               # Match single backtick code blocks
    # Match try-except blocks
    fr'{block_start}(try:|except(\s+[^\n]+)?:|finally:){block_cont_s}+',
    # Match if-else blocks
    fr'{block_start}(else:|elif [^\n]+:|if [^\n]+:){block_cont_s}+',
    # Match for loops
    fr'{block_start}for [^\n]+:{block_cont_s}+',
    # Match while loops
    fr'{block_start}while [^\n]+:{block_cont_s}+',
    # Match function definitions
    fr'{block_start}def [^\n]+:{block_cont_s}+',
    # Match class definitions
    fr'{block_start}class [^\n]+:{block_cont_s}+',

    # Match import statements
    fr'{block_start}(from [^\n]+? )?import [^\n]+\n',

    # # Match if statements
    fr'{block_start}if\s*\(([^\n]+\n?)+\){block_nl}*' + '{'+ block_cont_s+ '+}',
    # Match for loops
    fr'{block_start}for\s*\(([^\n]+\n?)+\){block_nl}*' + '{'+ block_cont_s+ '+}',
    # Match while loops
    fr'{block_start}while\s*\(([^\n]+\n?)+\){block_nl}*' + '{'+ block_cont_s+ '+}',
    # Match function definitions
    fr'{block_start}function\s+[^\n]*\s+\(([^\n]*?\n?)+\){block_nl}*' + '{'+ block_cont_s+ '+}',
    # Match class definitions
    fr'{block_start}class\s+[^\n]*{block_nl}*' + '{'+ block_cont_s+ '+}',
    # Match assignment statements
    fr'{block_start}(?<!\w)(?P<var_name>[a-zA-Z_]\w*)\s*=\s*(?P<value>[^\n]+)',
]

def re_code_blocks():
    # Define regular expressions for code-like patterns
    # Combine the patterns into a single regular expression
    code_regex = '((' + ')|('.join(code_patterns) + f')\n*?)+'
    return code_regex

for p in code_patterns:
    print(p)

print(re_code_blocks())

re_code_blocks_c = re.compile(re_code_blocks(), flags=re.DOTALL)

def filter_fix_nl(text):
    return re.sub('\r\n', '\n', text)

def filter_code_blocks(text, repl=''):
    # Remove code-like blocks from the text
    filtered_text = re_code_blocks_c.sub(repl, text)
    filtered_text = re.sub(fr'({re.escape(repl)}[^\S\r\n]*\n*)+', fr"{repl}\n", filtered_text)
    return filtered_text

if __name__ == "__main__":
    # Example usage
    input_text = '''Here's an example with exception handling:

from pathlib import Path

file_path = Path("path/to/my/file.txt")

try:
    # Delete the file
    print("File deleted successfully.")
except FileNotFoundError as e:
    print("File not found.")
finally:
    print("Permission denied. Unable to delete the file.")

In this example...'''

    filtered_text = filter_code_blocks(input_text)
    print(filtered_text)
