import sys

sys.path.insert(0, 'C:/Users/HP/OneDrive/Desktop/Projects/zap')
from src.lexer import Lexer
from src.parser import Parser

with open('C:/Users/HP/OneDrive/Desktop/Projects/ZAPphysics/examples/demo_game.zap', encoding='utf-8') as f:
    text = f.read()

tokens = Lexer(text, 'examples/demo_game.zap').tokenize()
parser = Parser(tokens)
prog = parser.parse()
print(f'Statements: {len(prog.stmts)}')
for i, stmt in enumerate(prog.stmts):
    t = type(stmt).__name__
    line = getattr(stmt, 'line', '?')
    name = getattr(stmt, 'name', getattr(stmt, 'var', ''))
    print(f'  [{i}] {t} line={line} name/var={name!r}')
    if hasattr(stmt, 'body') and hasattr(stmt.body, 'stmts'):
        for j, s in enumerate(stmt.body.stmts):
            st = type(s).__name__
            print(f'    [{j}] {st} line={getattr(s, "line", "?")}')
print(f'Parser errors: {len(parser.errors)}')
for err in parser.errors[:5]:
    print(f'  {err}')
