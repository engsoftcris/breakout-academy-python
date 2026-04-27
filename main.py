import tkinter as tk  # Importa a "caixa de ferramentas" para criar janelas e botões
from src.core.game_engine import GameEngine  # Importa o "cérebro" do nosso jogo

def iniciar_app():
    try:
        # 1. CRIANDO A JANELA PRINCIPAL
        root = tk.Tk()  # Cria a base de tudo, como se fosse a moldura de um quadro
        root.title("Breakout Academy")  # Define o nome que aparece lá em cima na barra da janela

        # 2. CALCULANDO O TAMANHO DA TELA DO ALUNO
        # Aqui perguntamos ao computador qual o tamanho do monitor dele
        largura_monitor = root.winfo_screenwidth()
        altura_monitor = root.winfo_screenheight()

        # Queremos que a janela ocupe 80% da tela (0.8), para não ficar nem gigante nem pequena
        largura_janela = int(largura_monitor * 0.8)
        altura_janela = int(altura_monitor * 0.8)
        
        # Fazemos uma conta matemática para descobrir onde é o meio exato da tela
        pos_x = (largura_monitor // 2) - (largura_janela // 2)
        pos_y = (altura_monitor // 2) - (altura_janela // 2)
        
        # Aplicamos o tamanho e a posição centralizada na janela
        root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
        root.configure(bg="#1e1e1e")  # Pintamos o fundo da janela de cinza escuro

        # 3. CRIANDO OS ESPAÇOS (CONTAINERS)
        # O Frame funciona como uma "caixa" dentro da janela para organizar as coisas
        main_container = tk.Frame(root, bg="#1e1e1e")
        main_container.pack(expand=True, fill="both")  # Mandamos a caixa esticar para ocupar tudo

        # 4. ONDE O JOGO ACONTECE (CANVAS)
        # O Canvas é a nossa "folha de desenho" preta onde vamos desenhar a bola e os blocos
        canvas = tk.Canvas(main_container, width=400, height=600, bg="black", highlightthickness=0)
        canvas.pack(side="right", padx=50)  # Colocamos a folha de desenho à direita com um espaço (padx)

        # 5. LIGANDO O MOTOR DO JOGO
        # Aqui chamamos o motor (Engine) e entregamos a "folha de desenho" (canvas) para ele cuidar
        engine = GameEngine(canvas)
        engine.configurar_mundo()  # Mandamos o motor criar os blocos, a raquete e a bolinha

        # 6. MANTENDO TUDO LIGADO
        root.mainloop()  # Este comando diz ao computador: "Não feche a janela, fique rodando o jogo!"
        
    except Exception as e:
        # Se acontecer algum erro (tipo esquecer um arquivo), ele avisa aqui embaixo no terminal
        print(f"Erro ao iniciar a aplicação: {e}")

# Este comando garante que o jogo só comece se rodarmos este arquivo diretamente
if __name__ == "__main__":
    iniciar_app()