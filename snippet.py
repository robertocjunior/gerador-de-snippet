import os
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import ImageFormatter
import io
from PIL import Image

# Caminho do arquivo de entrada com o código
caminho_arquivo = "gerar_num_primos.py"  # exemplo: "code.txt" ou "main.py"

# Definições personalizáveis:
linguagem = "python"           # ex: "python", "c", "java", "javascript", "html"

# Lê o conteúdo do arquivo
with open(caminho_arquivo, "r", encoding="utf-8") as f:
    codigo_fonte = f.read()

# Obtém o lexer apropriado para a linguagem
lexer = get_lexer_by_name(linguagem)

# Gera imagem com destaque de sintaxe
formatter = ImageFormatter(
    font_name='Consolas',
    font_size=16,
    line_numbers=True,
    style='monokai',
    image_pad=10,
    line_pad=2,
)
image_data = highlight(codigo_fonte, lexer, formatter)

# Gera nome do arquivo de saída com extensão .png
nome_base = os.path.splitext(caminho_arquivo)[0]
nome_imagem = f"{nome_base}.png"

# Salva a imagem
with open(nome_imagem, "wb") as f:
    f.write(image_data)

# Mostra a imagem (opcional)
image = Image.open(io.BytesIO(image_data))
image.show()
