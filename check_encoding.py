import sys

with open('C:/Users/HP/OneDrive/Desktop/Projects/ZAPphysics/examples/demo_game.zap', 'rb') as f:
    data = f.read()
lines = data.split(b'\n')
for i in range(22, min(37, len(lines))):
    line = lines[i]
    decoded = line.decode('utf-8')
    has_non_ascii = any(b > 127 for b in line)
    print(f'  L{i+1}: {decoded!r} non_ascii={has_non_ascii}')
    if has_non_ascii:
        for j, b in enumerate(line):
            if b > 127:
                print(f'    byte {j}: 0x{b:02x}')

# Also tokenize it
sys.path.insert(0, 'C:/Users/HP/OneDrive/Desktop/Projects/zap')
from src.lexer import Lexer
text = data.decode('utf-8')
tokens = Lexer(text, 'examples/demo_game.zap').tokenize()
for t in tokens[40:80]:
    print(f'  token: {t.type.name:20s} line={t.line:3d} col={t.col:3d} val={t.value!r}')
