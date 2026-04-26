import tkinter as tk
from src.core.game_engine import GameEngine

def iniciar_app():
    try:
        root = tk.Tk()
        root.title("Breakout Academy")

        # Pega o tamanho do monitor para ser responsivo
        largura_monitor = root.winfo_screenwidth()
        altura_monitor = root.winfo_screenheight()

        largura_janela = int(largura_monitor * 0.8)
        altura_janela = int(altura_monitor * 0.8)
        
        pos_x = (largura_monitor // 2) - (largura_janela // 2)
        pos_y = (altura_monitor // 2) - (altura_janela // 2)
        
        root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
        root.configure(bg="#1e1e1e")

        # Container principal
        main_container = tk.Frame(root, bg="#1e1e1e")
        main_container.pack(expand=True, fill="both")

        # Canvas do Jogo
        canvas = tk.Canvas(main_container, width=400, height=600, bg="black", highlightthickness=0)
        canvas.pack(side="right", padx=50)

        # Inicia o motor
        engine = GameEngine(canvas)
        engine.configurar_mundo()

        root.mainloop()
    except Exception as e:
        print(f"Erro ao iniciar a aplicação: {e}")

if __name__ == "__main__":
    iniciar_app()