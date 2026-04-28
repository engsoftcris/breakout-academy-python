import tkinter as tk
import os
import pygame
import src.tutor.missao_5 as m5  # Preparado para a próxima missão

def carregar_missao_4(container, root, cor_fundo, larg_r, vel_r, callback_proxima=None):
    for widget in container.winfo_children():
        widget.destroy()

    # --- 1. PRÉ-CARREGAMENTO (PRELOAD) DOS SONS ---
    pygame.mixer.init()
    path_sounds = os.path.join("assets", "sounds")
    sons = {}
    
    for arquivo in ["bounce.wav", "paddle_hit.wav", "block_hit.wav"]:
        caminho = os.path.join(path_sounds, arquivo)
        if os.path.exists(caminho):
            sons[arquivo] = pygame.mixer.Sound(caminho)

    # --- 2. INTERFACE ---
    conteudo = tk.Frame(container, bg="#1e1e1e")
    conteudo.place(relx=0.5, rely=0.5, anchor="center")

    painel = tk.Frame(conteudo, bg="#2d2d2d", width=350, height=580)
    painel.pack(side="left", fill="y", padx=10)
    painel.pack_propagate(False)

    tk.Label(painel, text="🧱 MISSÃO 4: FÍSICA E SOM", fg="#FF9800", bg="#2d2d2d", font=("Arial", 16, "bold")).pack(pady=15)

    # --- VARIÁVEIS DIDÁTICAS (O que o aluno vai controlar) ---
    ativar_quique_fundo = tk.BooleanVar(value=False)
    ativar_destruicao = tk.BooleanVar(value=False)
    ativar_sons = tk.BooleanVar(value=False)

    tk.Label(painel, text="PROGRAME O COMPORTAMENTO:", fg="white", bg="#2d2d2d", font=("Arial", 10, "bold")).pack(pady=5)
    
    tk.Checkbutton(painel, text="Bola quica no chão (Não trava)", variable=ativar_quique_fundo, 
                   bg="#2d2d2d", fg="#4CAF50", selectcolor="#1e1e1e", activebackground="#2d2d2d").pack(anchor="w", padx=40)
    
    tk.Checkbutton(painel, text="Destruir blocos no impacto", variable=ativar_destruicao, 
                   bg="#2d2d2d", fg="#4CAF50", selectcolor="#1e1e1e", activebackground="#2d2d2d").pack(anchor="w", padx=40)

    tk.Checkbutton(painel, text="Ligar efeitos sonoros (SFX)", variable=ativar_sons, 
                   bg="#2d2d2d", fg="#4CAF50", selectcolor="#1e1e1e", activebackground="#2d2d2d").pack(anchor="w", padx=40)

    lbl_status = tk.Label(painel, text="O jogo está mudo e incompleto...", fg="#888", bg="#2d2d2d", font=("Arial", 9, "italic"))
    lbl_status.pack(pady=20)

    # --- 3. ÁREA DO JOGO ---
    canvas = tk.Canvas(conteudo, width=400, height=600, bg=cor_fundo, highlightthickness=0)
    canvas.pack(side="left")

    paddle = canvas.create_rectangle(200-(larg_r/2), 550, 200+(larg_r/2), 565, fill="white", tags="paddle")
    bola = canvas.create_oval(190, 290, 210, 310, fill="#FFD700", tags="bola")

    blocos = []
    def criar_blocos():
        for b in blocos: canvas.delete(b)
        blocos.clear()
        cores = ["#FF5252", "#FFEB3B", "#2196F3"]
        for l in range(3):
            for c in range(5):
                b = canvas.create_rectangle(10+c*78, 50+l*25, 83+c*78, 70+l*25, fill=cores[l], tags="bloco")
                blocos.append(b)

    criar_blocos()
    conf = {"dx": 5, "dy": -5, "ativo": False}

    def engine():
        if conf["ativo"]:
            canvas.move("bola", conf["dx"], conf["dy"])
            pos = canvas.coords("bola")

            # REBOTE PAREDES E TETO
            if pos[0] <= 0 or pos[2] >= 400:
                conf["dx"] *= -1
                if ativar_sons.get() and "bounce.wav" in sons: sons["bounce.wav"].play()
            
            if pos[1] <= 0:
                conf["dy"] *= -1
                if ativar_sons.get() and "bounce.wav" in sons: sons["bounce.wav"].play()

            # REBOTE NO CHÃO (AQUI O ALUNO APRENDE)
            if pos[3] >= 600:
                if ativar_quique_fundo.get():
                    conf["dy"] = -abs(conf["dy"])
                    if ativar_sons.get() and "bounce.wav" in sons: sons["bounce.wav"].play()
                else:
                    conf["ativo"] = False
                    lbl_status.config(text="⚠️ A bola caiu! Ative o rebote.", fg="#FF5252")

            # COLISÃO RAQUETE
            toque = canvas.find_overlapping(*pos)
            if paddle in toque:
                conf["dy"] = -abs(conf["dy"])
                if ativar_sons.get() and "paddle_hit.wav" in sons: sons["paddle_hit.wav"].play()

            # COLISÃO BLOCOS (LÓGICA DIDÁTICA)
            for b in blocos[:]:
                if b in toque:
                    if ativar_destruicao.get():
                        canvas.delete(b)
                        blocos.remove(b)
                        conf["dy"] *= -1
                        if ativar_sons.get() and "block_hit.wav" in sons: sons["block_hit.wav"].play()
                    break

            root.after(16, engine)

    # --- 4. FUNÇÕES DE AÇÃO ---
    def lancar():
        if not conf["ativo"]:
            conf["ativo"] = True
            engine()
            lbl_status.config(text="🚀 Bola em jogo!", fg="#2196F3")

    def validar():
        if ativar_quique_fundo.get() and ativar_destruicao.get() and ativar_sons.get():
            lbl_status.config(text="✅ PERFEITO! TUDO FUNCIONANDO.", fg="#4CAF50")
            prox = callback_proxima if callback_proxima else lambda: m5.carregar_missao_5(container, root, cor_fundo, larg_r, vel_r)
            tk.Button(painel, text="IR PARA MISSÃO 5 ➡️", command=prox, bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(pady=20, fill="x", padx=40)
        else:
            lbl_status.config(text="❌ O jogo ainda tem erros de lógica!", fg="#FF9800")

    # Botões de Comando
    btn_box = tk.Frame(painel, bg="#2d2d2d")
    btn_box.pack(fill="x", padx=40, pady=10)
    tk.Button(btn_box, text="🧪 LANÇAR", command=lancar, bg="#2196F3", fg="white").pack(side="left", expand=True, fill="x", padx=2)
    tk.Button(btn_box, text="✅ VALIDAR", command=validar, bg="#4CAF50", fg="white").pack(side="left", expand=True, fill="x", padx=2)

    # Controles da Raquete
    root.bind("<Left>", lambda e: canvas.move("paddle", -vel_r, 0) if canvas.coords("paddle")[0] > 0 else None)
    root.bind("<Right>", lambda e: canvas.move("paddle", vel_r, 0) if canvas.coords("paddle")[2] < 400 else None)