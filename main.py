import tkinter as tk
from src.core.game_engine import GameEngine

class TutorialApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Breakout Academy")
        
        # Configuração de tamanho (80% da tela) e centralização
        largura = int(root.winfo_screenwidth() * 0.8)
        altura = int(root.winfo_screenheight() * 0.8)
        self.root.geometry(f"{largura}x{altura}")
        self.root.configure(bg="#1e1e1e")

        # Container principal que faz a troca das telas
        self.main_container = tk.Frame(self.root, bg="#1e1e1e")
        self.main_container.pack(expand=True, fill="both")

        # Inicia pela tela de Boas-Vindas
        self.mostrar_tela_boas_vindas()

    def limpar_tela(self):
        # Limpa a janela para carregar o próximo passo
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def mostrar_tela_boas_vindas(self):
        self.limpar_tela()
        
        # Menu Inicial Centralizado
        frame_menu = tk.Frame(self.main_container, bg="#1e1e1e")
        frame_menu.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame_menu, text="BEM-VINDO AO", fg="white", bg="#1e1e1e", 
                 font=("Arial", 16)).pack()
        
        tk.Label(frame_menu, text="BREAKOUT ACADEMY", fg="#4CAF50", bg="#1e1e1e", 
                 font=("Courier", 40, "bold")).pack(pady=10)

        tk.Label(frame_menu, text="Onde você constrói seu próprio jogo de tijolos!", 
                 fg="#cccccc", bg="#1e1e1e", font=("Arial", 12)).pack(pady=20)

        # Botão para entrar no ambiente (por enquanto só muda a tela)
        tk.Button(frame_menu, text="INICIAR JORNADA 🚀", 
                  command=self.mostrar_ambiente_estudo,
                  bg="#4CAF50", fg="white", font=("Arial", 14, "bold"), 
                  padx=30, pady=15, cursor="hand2", relief="flat").pack(pady=20)

    def mostrar_ambiente_estudo(self):
        self.limpar_tela()
        
        # Frame que agrupa Painel e Jogo lado a lado no centro
        conteudo = tk.Frame(self.main_container, bg="#1e1e1e")
        conteudo.place(relx=0.5, rely=0.5, anchor="center")

        # --- LADO ESQUERDO: PAINEL DE CONTROLE (VAZIO) ---
        self.painel_controle = tk.Frame(conteudo, bg="#2d2d2d", width=400, height=600)
        self.painel_controle.pack(side="left", fill="y", padx=20)
        self.painel_controle.pack_propagate(False)

        # Apenas um título de cabeçalho, sem instruções de missão ainda
        tk.Label(self.painel_controle, text="PAINEL DE CÓDIGO", fg="#888888", 
                 bg="#2d2d2d", font=("Courier", 18, "bold")).pack(pady=20)

        # O botão fica aqui, mas não executa nada por enquanto
        self.btn_executar = tk.Button(self.painel_controle, text="AGUARDANDO CÓDIGO...", 
                                     state="disabled", bg="#444444", 
                                     fg="#888888", font=("Arial", 12, "bold"), pady=10)
        self.btn_executar.pack(side="bottom", fill="x", pady=20, padx=20)

        # --- LADO DIREITO: ÁREA DO JOGO (VAZIA) ---
        self.canvas = tk.Canvas(conteudo, width=400, height=600, 
                                bg="#111111", highlightthickness=0)
        self.canvas.pack(side="left", padx=20)
        
        # O motor não é iniciado aqui para o jogo não aparecer do nada
        self.engine = None

if __name__ == "__main__":
    root = tk.Tk()
    app = TutorialApp(root)
    root.mainloop()