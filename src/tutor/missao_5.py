import tkinter as tk
import os
import pygame
import src.tutor.jogo_final as jf 

def carregar_missao_5(container, root, cor_fundo, larg_r, vel_r):
    """
    MISSÃO 5: O MESTRE DO JOGO
    Aqui o aluno define as regras finais e 'publica' seu projeto.
    """
    
    # --- 1. LIMPEZA E SETUP DE ÁUDIO ---
    for widget in container.winfo_children():
        widget.destroy()

    pygame.mixer.init()
    # Carregamento dos sons originais
    path_sounds = os.path.join("assets", "sounds")
    sons = {arq: pygame.mixer.Sound(os.path.join(path_sounds, arq)) 
            for arq in ["bounce.wav", "paddle_hit.wav", "block_hit.wav"] 
            if os.path.exists(os.path.join(path_sounds, arq))}

    # --- 2. DICIONÁRIO DE ESTADO DO JOGO ---
    game = {
        "score": 0, "vidas": 0, "ativo": False, "blocos": [], 
        "dx": 6, "dy": -6, "pts_bloco": 0, "tutorial_ok": False,
        "loop_id": None # Controle para não duplicar velocidade
    }

    conteudo = tk.Frame(container, bg="#1e1e1e")
    conteudo.place(relx=0.5, rely=0.5, anchor="center")

    # --- 3. PAINEL DE CONFIGURAÇÃO ---
    painel = tk.Frame(conteudo, bg="#2d2d2d", width=420, height=600)
    painel.pack(side="left", fill="y", padx=20)
    painel.pack_propagate(False)

    tk.Label(painel, text="🛠️ MISSÃO 5: O MESTRE", fg="#FF9800", bg="#2d2d2d", font=("Arial", 16, "bold")).pack(pady=15)

    # Textos Didáticos Originais
    info = tk.Frame(painel, bg="#3d3d3d", padx=15, pady=10)
    info.pack(fill="x", padx=25, pady=5)
    tk.Label(info, text="🎯 SUA TAREFA:", fg="#FFD700", bg="#3d3d3d", font=("Arial", 10, "bold")).pack(anchor="w")
    tk.Label(info, text="Agora você define as regras! Escolha\nquantas chances o jogador tem e quanto\nvale cada ponto.", 
             fg="#e0e0e0", bg="#3d3d3d", font=("Arial", 10), justify="left").pack(pady=5)

    aprenda = tk.Frame(painel, bg="#3d3d3d", padx=15, pady=10)
    aprenda.pack(fill="x", padx=25, pady=5)
    tk.Label(aprenda, text="💡 DICA DO MAGO:", fg="#FFD700", bg="#3d3d3d", font=("Arial", 10, "bold")).pack(anchor="w")
    tk.Label(aprenda, text="Um bom jogo precisa de EQUILÍBRIO.\nVidas demais deixam o jogo fácil,\npontos demais quebram o Score!", 
             fg="#e0e0e0", bg="#3d3d3d", font=("Arial", 9, "italic"), justify="left").pack(pady=5)

    # --- 4. EDITOR DE REGRAS ---
    editor = tk.Frame(painel, bg="#1e1e1e", padx=20, pady=15, highlightthickness=1, highlightbackground="#444")
    editor.pack(fill="x", padx=25, pady=10)

    estilo_in = {"bg": "#2d2d2d", "fg": "white", "insertbackground": "white", 
                 "highlightthickness": 1, "highlightbackground": "#444", 
                 "highlightcolor": "#FF9800", "relief": "flat", "justify": "center", "font": ("Courier", 12)}

    # Função para limpar o campo automaticamente ao clicar
    def limpar_ao_clicar(event, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)

    # Entrada de Vidas
    tk.Label(editor, text="# Número de Vidas (1-10):", fg="#6A9955", bg="#1e1e1e", font=("Courier", 10)).pack(anchor="w")
    ent_vds = tk.Entry(editor, **estilo_in)
    ent_vds.insert(0, "Ex: 3")
    ent_vds.bind("<FocusIn>", lambda e: limpar_ao_clicar(e, ent_vds, "Ex: 3")) 
    ent_vds.pack(fill="x", pady=5)

    btn_vds = tk.Button(editor, text="Validar Vidas", bg="#444", fg="white", font=("Arial", 9, "bold"), 
                        command=lambda: validar_v())
    btn_vds.pack(fill="x", pady=(0, 10))

    # Campo de Pontos
    f_pontos = tk.Frame(editor, bg="#1e1e1e")
    ent_pts = tk.Entry(f_pontos, **estilo_in)
    btn_pts = tk.Button(f_pontos, text="Validar Pontos", bg="#444", fg="white", font=("Arial", 9, "bold"))

    lbl_msg = tk.Label(painel, text="", fg="#4CAF50", bg="#2d2d2d", font=("Arial", 10, "bold"))

    # --- 5. TELA DO JOGO (CANVAS) ---
    canvas = tk.Canvas(conteudo, width=400, height=600, bg=cor_fundo, highlightthickness=2, highlightbackground="#444")
    canvas.pack(side="left", padx=20)

    paddle = canvas.create_rectangle(200-(larg_r/2), 550, 200+(larg_r/2), 565, fill="white", tags="paddle")
    bola = canvas.create_oval(190, 190, 210, 210, fill="#FFD700", tags="bola")
    
    txt_v = canvas.create_text(330, 30, text="", fill="#FF5252", font=("Arial", 12, "bold"))
    txt_s = canvas.create_text(70, 30, text="", fill="white", font=("Arial", 12, "bold"))

    # --- 6. FUNÇÕES DE VALIDAÇÃO (COM TRAVAS DE MIN/MAX) ---
    def validar_v():
        try:
            val = int(ent_vds.get())
            # VALIDAÇÃO: Mínimo 1, Máximo 10
            if 1 <= val <= 10:
                game["vidas"] = val
                canvas.itemconfig(txt_v, text="❤️" * val)
                btn_vds.config(text="✅ VIDAS OK", bg="#2E7D32", state="disabled")
                ent_vds.config(state="disabled")
                
                f_pontos.pack(fill="x")
                tk.Label(f_pontos, text="# Pontos por Bloco (1-1000):", fg="#6A9955", bg="#1e1e1e", font=("Courier", 10)).pack(anchor="w")
                ent_pts.insert(0, "Ex: 10")
                ent_pts.bind("<FocusIn>", lambda e: limpar_ao_clicar(e, ent_pts, "Ex: 10"))
                ent_pts.pack(fill="x", pady=5)
                btn_pts.config(command=validar_s)
                btn_pts.pack(fill="x")
            else: 
                ent_vds.config(highlightbackground="red") # Valor fora do limite
        except: 
            ent_vds.config(highlightbackground="red") # Não é número

    def validar_s():
        try:
            val = int(ent_pts.get())
            # VALIDAÇÃO: Mínimo 1, Máximo 1000
            if 1 <= val <= 1000:
                game["pts_bloco"] = val
                canvas.itemconfig(txt_s, text="SCORE: 0")
                btn_pts.config(text="✅ SCORE OK", bg="#2E7D32", state="disabled")
                ent_pts.config(state="disabled")
                game["tutorial_ok"] = True
                lbl_msg.config(text="✨ CONFIGURAÇÃO SALVA!")
                lbl_msg.pack(pady=10)
                btn_publicar.pack(pady=10, fill="x", padx=40)
            else:
                ent_pts.config(highlightbackground="red")
        except: 
            ent_pts.config(highlightbackground="red")

    # --- 7. BOTÃO DE PUBLICAÇÃO ---
    btn_publicar = tk.Button(painel, text="🚀 PUBLICAR JOGO", bg="#4CAF50", fg="white", 
                             font=("Arial", 12, "bold"), 
                             command=lambda: jf.iniciar_jogo_final(container, root, cor_fundo, larg_r, vel_r, game["vidas"], game["pts_bloco"]))

    # --- 8. MOTOR DE JOGO ---
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
                canvas.coords(bola, 190, 300, 210, 320)
                if game["vidas"] > 0: root.after(800, retomar)
                return
            
            items = canvas.find_overlapping(*p)
            if paddle in items: game["dy"] = -abs(game["dy"])
            
            for b in game["blocos"][:]:
                if b in items:
                    canvas.delete(b)
                    game["blocos"].remove(b)
                    game["score"] += game["pts_bloco"]
                    game["dy"] *= -1
                    canvas.itemconfig(txt_s, text=f"SCORE: {game['score']}")
                    break
            game["loop_id"] = root.after(16, engine)

    def retomar():
        game["ativo"] = True
        engine()

    def comando_espaco(e):
        if game["loop_id"]:
            root.after_cancel(game["loop_id"])
            game["loop_id"] = None

        if game["tutorial_ok"] and not game["ativo"]:
            game["ativo"] = True
            engine()

    def criar_blocos():
        cores = ["#FF5252", "#FFEB3B", "#2196F3"]
        for l in range(3):
            for c in range(5):
                b = canvas.create_rectangle(10+c*78, 60+l*25, 83+c*78, 80+l*25, fill=cores[l], outline="#1e1e1e")
                game["blocos"].append(b)

    # --- 9. CONTROLES ---
    criar_blocos()
    root.bind("<Left>", lambda e: canvas.move(paddle, -vel_r, 0) if canvas.coords(paddle)[0] > 0 else None)
    root.bind("<Right>", lambda e: canvas.move(paddle, vel_r, 0) if canvas.coords(paddle)[2] < 400 else None)
    root.bind("<space>", comando_espaco)