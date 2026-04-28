import tkinter as tk
from src.tutor.missao_2 import carregar_missao_2

def carregar_missao_1(container, root):
    # Limpa o palco da AppPrincipal
    for widget in container.winfo_children():
        widget.destroy()

    conteudo = tk.Frame(container, bg="#1e1e1e")
    conteudo.place(relx=0.5, rely=0.5, anchor="center")

    # --- PAINEL DE CONTROLE (O LABORATÓRIO) ---
    painel = tk.Frame(conteudo, bg="#2d2d2d", width=420, height=600)
    painel.pack(side="left", fill="y", padx=20)
    painel.pack_propagate(False)

    tk.Label(painel, text="🏗️ MISSÃO 1: O ARQUITETO", fg="#4CAF50", 
             bg="#2d2d2d", font=("Courier", 18, "bold")).pack(pady=15)

    # --- MANUAL DA MISSÃO (TEXTO QUE VOCÊ GOSTOU) ---
    missao_info = tk.Frame(painel, bg="#3d3d3d", padx=15, pady=10)
    missao_info.pack(fill="x", padx=25, pady=5)
    
    tk.Label(missao_info, text="🎯 SEU OBJETIVO:", fg="#FFD700", bg="#3d3d3d", font=("Arial", 10, "bold")).pack(anchor="w")
    objetivo = (
        "Para o jogo começar, você precisa configurar\n"
        "as regras básicas do Motor Gráfico.\n"
        "Nesta missão, você vai aprender a enviar\n"
        "sua primeira instrução: o comando de COR!"
    )
    tk.Label(missao_info, text=objetivo, fg="#e0e0e0", bg="#3d3d3d", font=("Arial", 10), justify="left").pack(pady=5)

    # --- SEÇÃO DE APRENDIZADO ---
    aprenda = tk.Frame(painel, bg="#3d3d3d", padx=15, pady=10)
    aprenda.pack(fill="x", padx=25, pady=5)
    
    tk.Label(aprenda, text="💡 VOCÊ SABIA?", fg="#FFD700", bg="#3d3d3d", font=("Arial", 10, "bold")).pack(anchor="w")
    info = (
        "Na programação, textos são chamados de STRINGS.\n"
        "As aspas \" \" servem para avisar ao computador\n"
        "onde o texto começa e onde ele termina!"
    )
    tk.Label(aprenda, text=info, fg="#e0e0e0", bg="#3d3d3d", font=("Arial", 9, "italic"), justify="left").pack(pady=5)

    # PALETA TÉCNICA
    tk.Label(painel, text="🎨 PALETA DE CORES:", fg="#FFD700", bg="#2d2d2d", font=("Arial", 10, "bold")).pack(pady=(10,0))
    CORES = ["blue", "red", "green", "purple", "yellow", "orange", "black", "white"]
    tk.Label(painel, text=", ".join(CORES), fg="#4CAF50", bg="#2d2d2d", font=("Courier", 10, "bold"), wraplength=350).pack()

    # EDITOR DE CÓDIGO
    editor = tk.Frame(painel, bg="#1e1e1e", padx=20, pady=20, highlightbackground="#444", highlightthickness=1)
    editor.pack(fill="x", padx=25, pady=10)

    tk.Label(editor, text="# Escreva sua String de cor:", fg="#6A9955", bg="#1e1e1e", font=("Courier", 10)).pack(anchor="w")
    f_cor = tk.Frame(editor, bg="#1e1e1e")
    f_cor.pack(fill="x", pady=5)
    
    tk.Label(f_cor, text='cor_fundo = "', fg="#ce9178", bg="#1e1e1e", font=("Courier", 14)).pack(side="left")
    ent_cor = tk.Entry(f_cor, bg="#1e1e1e", fg="#9cdcfe", insertbackground="white", font=("Courier", 14), borderwidth=0, width=12)
    ent_cor.pack(side="left")
    tk.Label(f_cor, text='"', fg="#ce9178", bg="#1e1e1e", font=("Courier", 14)).pack(side="left")

    lbl_feedback = tk.Label(painel, text="Aguardando comando...", fg="#888888", bg="#2d2d2d", font=("Arial", 11, "bold"))
    lbl_feedback.pack(pady=10)

    # --- BOTÕES PADRONIZADOS ---
    frame_botoes = tk.Frame(painel, bg="#2d2d2d")
    frame_botoes.pack(fill="x", padx=25, pady=5)

    estilo_btn = {"font": ("Arial", 10, "bold"), "pady": 15, "fg": "white", "relief": "flat", "cursor": "hand2"}

    tk.Button(frame_botoes, text="🧪 TESTAR", bg="#2196F3", 
              command=lambda: validar_e_testar(ent_cor.get(), canvas, lbl_feedback, CORES), **estilo_btn).pack(side="left", fill="x", expand=True, padx=2)

    tk.Button(frame_botoes, text="✅ VALIDAR", bg="#4CAF50", 
              command=lambda: concluir_missao(ent_cor.get(), canvas, frame_botoes, lbl_feedback, CORES, container, root), **estilo_btn).pack(side="left", fill="x", expand=True, padx=2)

    # --- TELA DO JOGO (CANVAS) ---
    canvas = tk.Canvas(conteudo, width=400, height=600, bg="#111111", highlightthickness=2, highlightbackground="#444")
    canvas.pack(side="left", padx=20)

# --- FUNÇÕES DE LÓGICA ---

def validar_e_testar(valor, canvas, label, lista):
    cor = valor.strip().lower()
    if cor in lista:
        canvas.configure(bg=cor)
        label.configure(text=f"✔️ String '{cor}' aceita!", fg="#4CAF50")
        return True
    label.configure(text="❌ ERRO: Cor não reconhecida!", fg="#FF5252")
    return False

def concluir_missao(valor, canvas, frame_botoes, label, lista, container, root):
    if validar_e_testar(valor, canvas, label, lista):
        # A 'valor' aqui já é a cor que foi validada
        cor_escolhida = valor 
        
        for widget in frame_botoes.winfo_children():
            widget.destroy()
        
        label.configure(text="✨ MISSÃO CUMPRIDA!", fg="#FFD700", font=("Arial", 14, "bold"))
        
        # O BOTÃO AGORA PASSA A COR ADIANTE
        tk.Button(frame_botoes, text="CONSTRUIR RAQUETE ➡️", bg="#FF9800", fg="white", 
                  font=("Arial", 12, "bold"), pady=15,
                  # Adicionamos 'cor_escolhida' como o terceiro argumento:
                  command=lambda: carregar_missao_2(container, root, cor_escolhida)).pack(fill="x", pady=10)