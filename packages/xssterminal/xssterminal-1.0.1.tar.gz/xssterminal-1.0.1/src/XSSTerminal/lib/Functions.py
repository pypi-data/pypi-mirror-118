import readline
from prompt_toolkit import prompt as input_prompt
from pygments.lexers.html import HtmlLexer
from prompt_toolkit.lexers import PygmentsLexer

from XSSTerminal.lib.Globals import Color

def xss_input_readline(prompt, text):
         def hook():
             readline.insert_text(text)
             readline.redisplay()
         readline.set_pre_input_hook(hook)
         result = input(prompt)
         readline.set_pre_input_hook()
         return result

def xss_input_prompt_toolkit(prompt, text):
    return input_prompt(prompt, default=text, lexer=PygmentsLexer(HtmlLexer))

def banner():
    pass

def starter(argv):
    if argv.banner:
        banner()
        exit()
    if not argv.url:
        print(f"{Color.bad} Use --help")
        exit()
    return argv.url

def exit_handler(*args, filename=None):
    pass
