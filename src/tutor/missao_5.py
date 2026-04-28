import tkinter as tk
import os
import pygame

def carregar_missao_5(container, root, cor_fundo, larg_r, vel_r):
    for widget in container.winfo_children():
        widget.destroy()

    # --- 1. SETUP DE ÁUDIO ---
    pygame.mixer.init()
    path_sounds = os.path.join("assets", "sounds")
    sons = {arq: pygame.mixer.Sound(os.path.join(path_sounds, arq)) 
            for arq in ["bounce.wav", "paddle_hit.wav", "block_hit.wav"] 
            if os.path.exists(os.path.join(path_sounds, arq))}

    # Configurações de jogo (Velocidade 6 para equilíbrio)
    game = {"score": 0, "vidas": 0, "ativo": False, "blocos": [], 
            "dx": 6, "dy": -6, "pts_bloco": 0, "tutorial_ok": False, "confirmando_saida": False}

    conteudo = tk.Frame(container, bg="#1e1e1e")
    conteudo.place(relx=0.5, rely=0.5, anchor="center")

    # --- 2. PAINEL DE CONFIGURAÇÃO ---
    painel = tk.Frame(conteudo, bg="#2d2d2d", width=280, height=580)
    painel.pack(side="left", fill="y", padx=10)
    painel.pack_propagate(False)

    tk.Label(painel, text="🛠️ CONFIGURAÇÃO", fg="#FF9800", bg="#2d2d2d", font=("Arial", 16, "bold")).pack(pady=15)

    estilo_in = {"bg": "#1e1e1e", "fg": "#888", "insertbackground": "white", 
                 "highlightthickness": 1, "highlightbackground": "#444", 
                 "highlightcolor": "#FF9800", "relief": "flat", "justify": "center"}

    def tratar_foco(entry, txt, acao):
        if acao == "in" and entry.get() == txt:
            entry.delete(0, tk.END)
            entry.config(fg="white")
        elif acao == "out" and not entry.get():
            entry.insert(0, txt)
            entry.config(fg="#888")

    # VIDAS
    f1 = tk.Frame(painel, bg="#2d2d2d")
    f1.pack(fill="x", padx=20, pady=10)
    tk.Label(f1, text="1. NÚMERO DE VIDAS", fg="#aaa", bg="#2d2d2d", font=("Arial", 9, "bold")).pack(anchor="w")
    ent_vds = tk.Entry(f1, **estilo_in)
    ent_vds.insert(0, "Ex: 3")
    ent_vds.bind("<FocusIn>", lambda e: tratar_foco(ent_vds, "Ex: 3", "in"))
    ent_vds.bind("<FocusOut>", lambda e: tratar_foco(ent_vds, "Ex: 3", "out"))
    ent_vds.pack(fill="x", pady=5, ipady=3)
    btn_vds = tk.Button(f1, text="Validar Vidas", command=lambda: validar_v())
    btn_vds.pack(fill="x")

    # SCORE
    f2 = tk.Frame(painel, bg="#2d2d2d")
    ent_pts = tk.Entry(f2, **estilo_in)
    btn_pts = tk.Button(f2, text="Validar Pontos")

    # --- BOTÃO PARA FECHAR TUDO (COM CONFIRMAÇÃO) ---
    def encerrar_sistema():
        if not game["confirmando_saida"]:
            game["confirmando_saida"] = True
            btn_sair.config(text="CONFIRMAR SAÍDA?", bg="#FF9800", fg="black")
            root.after(3000, cancelar_saida)
        else:
            # FECHA A JANELA E O PROGRAMA
            pygame.mixer.quit()
            root.destroy()

    def cancelar_saida():
        game["confirmando_saida"] = False
        btn_sair.config(text="FECHAR TUDO", bg="#f44336", fg="white")

    lbl_msg = tk.Label(painel, text="", fg="#4CAF50", bg="#2d2d2d", font=("Arial", 10, "bold"))
    btn_sair = tk.Button(painel, text="FECHAR TUDO", bg="#f44336", fg="white", 
                         font=("Arial", 11, "bold"), command=encerrar_sistema)

    # --- 3. ÁREA DO JOGO ---
    canvas = tk.Canvas(conteudo, width=400, height=600, bg=cor_fundo, highlightthickness=0)
    canvas.pack(side="left")
    paddle = canvas.create_rectangle(160, 550, 240, 565, fill="white", tags="paddle")
    bola = canvas.create_oval(190, 190, 210, 210, fill="#FFD700", tags="bola")
    txt_v = canvas.create_text(330, 30, text="", fill="#FF5252", font=("Arial", 12, "bold"))
    txt_s = canvas.create_text(70, 30, text="", fill="white", font=("Arial", 12, "bold"))

    # --- 4. VALIDAÇÕES ---
    def validar_v():
        try:
            game["vidas"] = int(ent_vds.get())
            canvas.itemconfig(txt_v, text="❤️" * game["vidas"])
            btn_vds.config(text="✅ VIDAS OK", bg="#2E7D32", state="disabled")
            ent_vds.config(state="disabled", highlightbackground="#2E7D32")
            f2.pack(fill="x", padx=20, pady=10)
            tk.Label(f2, text="2. PONTOS POR BLOCO", fg="#aaa", bg="#2d2d2d", font=("Arial", 9, "bold")).pack(anchor="w")
            ent_pts.insert(0, "Ex: 10")
            ent_pts.bind("<FocusIn>", lambda e: tratar_foco(ent_pts, "Ex: 10", "in"))
            ent_pts.bind("<FocusOut>", lambda e: tratar_foco(ent_pts, "Ex: 10", "out"))
            ent_pts.pack(fill="x", pady=5, ipady=3)
            btn_pts.config(command=validar_s)
            btn_pts.pack(fill="x")
        except: ent_vds.config(highlightbackground="red")

    def validar_s():
        try:
            game["pts_bloco"] = int(ent_pts.get())
            canvas.itemconfig(txt_s, text="SCORE: 0")
            btn_pts.config(text="✅ SCORE OK", bg="#2E7D32", state="disabled")
            ent_pts.config(state="disabled", highlightbackground="#2E7D32")
            game["tutorial_ok"] = True
            lbl_msg.config(text="✓ TUTORIAL CONCLUÍDO!\n[ Espaço ] p/ Jogar")
            lbl_msg.pack(pady=10)
            btn_sair.pack(pady=20, fill="x", padx=40)
        except: ent_pts.config(highlightbackground="red")

    # --- 5. LÓGICA DO JOGO ---
    def engine():
        if game["ativo"]:
            canvas.move(bola, game["dx"], game["dy"])
            p = canvas.coords(bola)
            if p[0] <= 0 or p[2] >= 400: game["dx"] *= -1
            if p[1] <= 0: game["dy"] *= -1
            if p[3] >= 600:
                game["vidas"] -= 1
                canvas.itemconfig(txt_v, text="❤️" * game["vidas"] if game["vidas"] > 0 else "💀")
                game["ativo"] = False 
                canvas.coords(bola, 190, 190, 210, 210)
                if game["vidas"] > 0: root.after(800, retomar)
                else: canvas.create_text(200, 300, text="GAME OVER\n[ Espaço ]", fill="red", font=("Arial", 16, "bold"), tags="msg")
                return
            
            items = canvas.find_overlapping(*p)
            if paddle in items:
                game["dy"] = -abs(game["dy"])
                if "paddle_hit.wav" in sons: sons["paddle_hit.wav"].play()
            
            for b in game["blocos"][:]:
                if b in items:
                    canvas.delete(b)
                    game["blocos"].remove(b)
                    game["score"] += game["pts_bloco"]
                    game["dy"] *= -1
                    canvas.itemconfig(txt_s, text=f"SCORE: {game['score']}")
                    if "block_hit.wav" in sons: sons["block_hit.wav"].play()
                    if not game["blocos"]:
                        game["ativo"] = False
                        canvas.create_text(200, 300, text="VITÓRIA! 🏆\n[ Espaço ]", fill="#4CAF50", font=("Arial", 20, "bold"), tags="msg")
                    break
            root.after(16, engine)

    def retomar():
        if not game["ativo"] and game["vidas"] > 0:
            game["ativo"] = True
            engine()

    def comando_espaco(e):
        if game["tutorial_ok"] and not game["ativo"]:
            if game["vidas"] <= 0 or not game["blocos"]:
                game["score"] = 0
                game["vidas"] = int(ent_vds.get())
                canvas.itemconfig(txt_v, text="❤️" * game["vidas"])
                canvas.itemconfig(txt_s, text="SCORE: 0")
                for b in game["blocos"]: canvas.delete(b)
                game["blocos"].clear()
                criar_blocos()
                canvas.coords(bola, 190, 190, 210, 210)
            
            canvas.delete("msg")
            game["ativo"] = True
            engine()

    def criar_blocos():
        cores = ["#FF5252", "#FFEB3B", "#2196F3"]
        for l in range(3):
            for c in range(5):
                b = canvas.create_rectangle(10+c*78, 60+l*25, 83+c*78, 80+l*25, fill=cores[l], outline="#1e1e1e")
                game["blocos"].append(b)

    criar_blocos()
    root.bind("<Left>", lambda e: canvas.move(paddle, -vel_r, 0) if canvas.coords(paddle)[0] > 0 else None)
    root.bind("<Right>", lambda e: canvas.move(paddle, vel_r, 0) if canvas.coords(paddle)[2] < 400 else None)
    root.bind("<space>", comando_espaco)