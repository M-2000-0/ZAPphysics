import sys

sys.path.insert(0, 'C:/Users/HP/OneDrive/Desktop/Projects/zap')
from src.lexer import Lexer

with open('C:/Users/HP/OneDrive/Desktop/Projects/ZAPphysics/examples/demo_game.zap', encoding='utf-8') as f:
    text = f.read()

tokens = Lexer(text, 'examples/demo_game.zap').tokenize()

# Find tokens around the for loop (lines 23-36)
for t in tokens:
    if t.line >= 23 and t.line <= 36:
        print(f'  L{t.line:2d}: {t.type.name:20s} val={t.value!r}')
