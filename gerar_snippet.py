import os
import webbrowser
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import ImageFormatter
from pygments.styles import get_all_styles
import io
from PIL import Image
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
import time

# Configurações iniciais
config = {
    "caminho_arquivo": "",
    "linguagem": "python",
    "Fonte": "Consolas",
    "Tamanho da Fonte": 16,
    "Números nas Linha": True,
    "estilo": "material",
    "Espaçamento da Imagem (Image Pad)": 10,
    "Espaçamento da Linha (Line Pad)": 2
}

console = Console()

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_configuracao():
    """Mostra a configuração atual em um painel bonito"""
    table = Table(show_header=False, box=box.SIMPLE)
    table.add_column("Opção", style="cyan")
    table.add_column("Valor", style="magenta")
    
    for chave, valor in config.items():
        table.add_row(chave, str(valor))
    
    console.print(Panel.fit(table, title="[bold]Configuração Atual[/]", border_style="blue"))

def menu_principal():
    """Menu principal interativo"""
    limpar_tela()
    mostrar_configuracao()
    
    opcoes = [
        "📂 Caminho do Arquivo",
        "🖋️ Linguagem",
        "🔠 Fonte",
        "🔢 Tamanho da Fonte",
        "📊 Números nas Linha",
        "🎨 Estilo de Cores",
        "🖼️ Espaçamento da Imagem (Image Pad)",
        "📏 Espaçamento da Linha (Line Pad)",
        "👀 Ver Estilos Disponíveis",
        "✨ Gerar Imagem",
        "❌ Sair"
    ]
    
    opcao = questionary.select(
        "O que você deseja configurar?",
        choices=opcoes,
        default=opcoes[0]
    ).ask()
    
    return opcao

def abrir_documentacao_estilos():
    """Abre a documentação de estilos do Pygments no navegador"""
    webbrowser.open("https://pygments.org/styles/")
    console.print("[yellow]Abrindo documentação de estilos no navegador...[/]")
    time.sleep(1)

def configurar_caminho():
    """Configura o caminho do arquivo"""
    caminho = questionary.path("Digite o caminho do arquivo:").ask()
    if caminho and os.path.exists(caminho):
        config["caminho_arquivo"] = caminho
    else:
        console.print("[red]Arquivo não encontrado![/]")
        time.sleep(1)

def configurar_linguagem():
    """Configura a linguagem de programação"""
    linguagens = ["python", "text", "javascript", "java", "c", "cpp", "html", "css", "Outra linguagem..."]
    escolha = questionary.select(
        "Selecione a linguagem:",
        choices=linguagens,
        default=config["linguagem"]
    ).ask()
    
    if escolha == "Outra linguagem...":
        nova_linguagem = questionary.text(
            "Digite o nome da linguagem (como é reconhecida pelo Pygments):",
            validate=lambda x: len(x.strip()) > 0
        ).ask()
        if nova_linguagem:
            config["linguagem"] = nova_linguagem.strip().lower()
    else:
        config["linguagem"] = escolha

def configurar_fonte():
    """Configura o tipo de fonte"""
    fontes = ["Consolas", "Courier New", "DejaVu Sans Mono", "Lucida Console"]
    config["Fonte"] = questionary.select(
        "Selecione a fonte:",
        choices=fontes,
        default=config["Fonte"]
    ).ask()

def configurar_tamanho_fonte():
    """Configura o tamanho da fonte"""
    tamanho = questionary.text(
        f"Tamanho atual: {config['Tamanho da Fonte']}. Digite o novo tamanho:",
        validate=lambda x: x.isdigit() and 8 <= int(x) <= 36
    ).ask()
    if tamanho:
        config["Tamanho da Fonte"] = int(tamanho)

def configurar_numeros_linha():
    """Configura se mostra números de linha"""
    opcoes = [
        {"name": "✅ Sim", "value": True},
        {"name": "❌ Não", "value": False}
    ]
    
    escolha = questionary.select(
        "Mostrar números de linha?",
        choices=opcoes,
        default=opcoes[0] if config["Números nas Linha"] else opcoes[1]
    ).ask()
    
    config["Números nas Linha"] = escolha

def configurar_estilo():
    """Configura o estilo de cores"""
    estilos = list(get_all_styles())
    config["estilo"] = questionary.select(
        "Selecione o estilo de cores:",
        choices=estilos,
        default=config["estilo"]
    ).ask()

def configurar_image_pad():
    """Configura o espaçamento da imagem"""
    pad = questionary.text(
        f"Espaçamento atual da imagem: {config['Espaçamento da Imagem (Image Pad)']}. Digite o novo valor:",
        validate=lambda x: x.isdigit() and 0 <= int(x) <= 50
    ).ask()
    if pad:
        config["Espaçamento da Imagem (Image Pad)"] = int(pad)

def configurar_line_pad():
    """Configura o espaçamento entre linhas"""
    pad = questionary.text(
        f"Espaçamento atual entre linhas: {config['Espaçamento da Linha (Line Pad)']}. Digite o novo valor:",
        validate=lambda x: x.isdigit() and 0 <= int(x) <= 10
    ).ask()
    if pad:
        config["Espaçamento da Linha (Line Pad)"] = int(pad)

def gerar_imagem():
    """Gera a imagem com as configurações atuais"""
    if not config["caminho_arquivo"]:
        console.print("[red]Erro: Nenhum arquivo selecionado![/]")
        time.sleep(1)
        return
    
    try:
        with open(config["caminho_arquivo"], "r", encoding="utf-8") as f:
            codigo_fonte = f.read()
        
        lexer = get_lexer_by_name(config["linguagem"])
        formatter = ImageFormatter(
            font_name=config["Fonte"],
            font_size=config["Tamanho da Fonte"],
            line_numbers=config["Números nas Linha"],
            style=config["estilo"],
            image_pad=config["Espaçamento da Imagem (Image Pad)"],
            line_pad=config["Espaçamento da Linha (Line Pad)"]
        )
        
        image_data = highlight(codigo_fonte, lexer, formatter)
        
        nome_base = os.path.splitext(config["caminho_arquivo"])[0]
        nome_imagem = f"{nome_base}.png"
        
        with open(nome_imagem, "wb") as f:
            f.write(image_data)
        
        console.print(f"[green]Imagem gerada com sucesso: {nome_imagem}[/]")
        
        image = Image.open(io.BytesIO(image_data))
        image.show()
        
        time.sleep(2)
    except Exception as e:
        console.print(f"[red]Erro ao gerar imagem: {e}[/]")
        time.sleep(2)

def main():
    """Função principal"""
    while True:
        opcao = menu_principal()
        
        if opcao == "❌ Sair":
            break
        elif opcao == "📂 Caminho do Arquivo":
            configurar_caminho()
        elif opcao == "🖋️ Linguagem":
            configurar_linguagem()
        elif opcao == "🔠 Fonte":
            configurar_fonte()
        elif opcao == "🔢 Tamanho da Fonte":
            configurar_tamanho_fonte()
        elif opcao == "📊 Números nas Linha":
            configurar_numeros_linha()
        elif opcao == "🎨 Estilo de Cores":
            configurar_estilo()
        elif opcao == "🖼️ Espaçamento da Imagem (Image Pad)":
            configurar_image_pad()
        elif opcao == "📏 Espaçamento da Linha (Line Pad)":
            configurar_line_pad()
        elif opcao == "👀 Ver Estilos Disponíveis":
            abrir_documentacao_estilos()
        elif opcao == "✨ Gerar Imagem":
            gerar_imagem()

if __name__ == "__main__":
    main()
