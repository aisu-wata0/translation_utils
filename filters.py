import re


def filter_everything(text):
    text = filter_fix_nl(text)
    comments = []
    text = filter_code_comments(text, "", comments)
    text = filter_code_blocks(text, "[... code block]")
    text = filter_magnet_links(text)
    text = filter_urls(text)
    return text

block_start = r"((^|\n)[ \t]*)"
block_cont = r"([ \t]+[^\n]*\n)*"
block_cont_s = r"([^\S\r\n]*\n[ \t]+[^\n]+)"
block_nl = r"[^\S\r\n]*\n"
brackets = r"([{} ]+)?"

code_patterns = [
    r'```.*?```',           # Match triple backtick code blocks
    r'`.*?`',               # Match single backtick code blocks
    
    # Match assignment statements
    fr'''{block_start}([a-zA-Z]+[^\S\r\n]+)?{brackets}(?P<var_name>[a-zA-Z_][\w.[\](), \t]*){brackets}\s*[-+*\/=]+\s*([a-zA-Z]+[^\S\r\n]+)?(?P<var_name_assignment>(?:[a-zA-Z_]+[\w.[\](), \t]*)|(?:['`"].*?['`"])|[0-9=+*\/&|^%! \t]+);?($|\n)''',
    # Match Function call inline
    fr'''{block_start}([a-zA-Z]+[^\S\r\n]+)?(?P<function_call_inline>(?:[a-zA-Z_]+\([\w.[\](), \t"'`\\=+*\/&|^%!:]*?\)));?($|\n)''',
    # Match Function call mulitline
    fr'''{block_start}([a-zA-Z]+[^\S\r\n]+)?(?P<function_call_multiline>(?:[a-zA-Z_]+\((.*{block_cont_s})+))''',

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
    fr'{block_start}([a-zA-Z]+[^\S\r\n]+)?function\s+[^\n]*\s+\(([^\n]*?\n?)+\){block_nl}*' + '{'+ block_cont_s + '+}',
    # Match class definitions
    fr'{block_start}class\s+[^\n]*{block_nl}*' + '{'+ block_cont_s+ '+}',
]

def re_code_blocks():
    # Define regular expressions for code-like patterns
    # Combine the patterns into a single regular expression
    code_regex = '((' + ')|('.join(code_patterns) + f')\n*?)+'
    return code_regex

re_code_blocks_c = re.compile(re_code_blocks(), flags=re.DOTALL)

def filter_fix_nl(text):
    return re.sub('\r\n', '\n', text)

def filter_code_blocks(text, repl=''):
    # Remove code-like blocks from the text
    filtered_text = re_code_blocks_c.sub(repl, text)
    filtered_text = re.sub(fr'({re.escape(repl)}[^\S\r\n]*\n*)+', fr"{repl}\n", filtered_text)
    return filtered_text


def filter_code_comments(text, repl='', comments=[]):
    filtered_text = text
    return filtered_text

re_uri =r'[-a-zA-Z0-9()@:%_\+.~#?&\/=]'
re_url = r'(?P<protocol>https?:\/\/)?(www\.)?(?P<subdomain>([-a-zA-Z0-9@:%_\+~#=]{1,256}\.)+)?(?P<domain>([-a-zA-Z0-9@:%_\+~#=]{1,256})+)(?P<TLD>(\.[a-zA-Z0-9()]{1,6})+)\b([-a-zA-Z0-9()@:%_\+.~#?&\/=]*)'
re_url_c = re.compile(re_url, flags=re.DOTALL)

def filter_urls(text, repl='link to {domain}{TLD}'):
    def replace_url(match: re.Match[str]):
        # print("match", match, match.groups())
        return repl.format(**{k: match.group(k) for k in ['domain', 'TLD', 'protocol']})
    filtered_text = re_url_c.sub(replace_url, text)
    return filtered_text


import urllib.parse
re_magnet_link = r'magnet:\?xt=urn:btih:[a-fA-F0-9]{32,}(&dn=(?P<name>[-a-zA-Z0-9()@:%_\+.~#?&\/=]+?)(?P<tracker>&tr=(?:(?!magnet:\?xt=)[-a-zA-Z0-9()@:%_\+.~#?&\/=])+))?'
re_magnet_link_c = re.compile(re_magnet_link, flags=re.DOTALL)
def filter_magnet_links(text, repl='magnet link {name}'):
    def replace_url(match):
        return repl.format(**{k: urllib.parse.unquote(match.group(k)) for k in ['name', 'tracker']})
    filtered_text = re_magnet_link_c.sub(replace_url, text)
    return filtered_text

if __name__ == "__main__":
    # Debug patterns
    for p in code_patterns:
        print(p)

    print(re_code_blocks())

    # Example usage
    input_text = '''Here's an example with exception handling:


async function readyPrompt() {

}

    async function readyPrompt() {

    }

        let { messages, model } = generate_data

        userData[user.id].promptCount += 1

        await printUser(
                user,
                "user.isGame =",
                user.isGame,
                "\nmechanicsIdx =",
                mechanicsIdx
        )

In this example...'''


    filtered_text = filter_code_blocks(input_text, '[... code block]')
    print(filtered_text)
