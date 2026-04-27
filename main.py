import tkinter as tk
from src.tutor.missao_1 import carregar_missao_1


class AppPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Breakout Academy")
        
        # Configuração de tamanho (80% da tela)
        largura = int(root.winfo_screenwidth() * 0.8)
        altura = int(root.winfo_screenheight() * 0.8)
        self.root.geometry(f"{largura}x{altura}")
        self.root.configure(bg="#1e1e1e")

        self.main_container = tk.Frame(self.root, bg="#1e1e1e")
        self.main_container.pack(expand=True, fill="both")

        self.tela_inicial()

    def tela_inicial(self):
        # Limpa o container
        for widget in self.main_container.winfo_children():
            widget.destroy()

        frame_menu = tk.Frame(self.main_container, bg="#1e1e1e")
        frame_menu.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame_menu, text="BEM-VINDO AO", fg="white", bg="#1e1e1e", font=("Arial", 16)).pack()
        tk.Label(frame_menu, text="BREAKOUT ACADEMY", fg="#4CAF50", bg="#1e1e1e", font=("Courier", 40, "bold")).pack(pady=10)

        # O BOTÃO QUE VOCÊ FALOU: Ele chama a função que traz a missão da pasta tutor
        tk.Button(frame_menu, text="INICIAR JORNADA 🚀", 
                  command=lambda: carregar_missao_1(self.main_container, self.root),
                  bg="#4CAF50", fg="white", font=("Arial", 14, "bold"), 
                  padx=30, pady=15, cursor="hand2").pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppPrincipal(root)
    root.mainloop()