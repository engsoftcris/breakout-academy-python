import tkinter as tk

def carregar_missao_2(container, root, cor_fundo):
    # 1. Limpeza de rastro e eventos
    root.unbind("<Left>")
    root.unbind("<Right>")
    for widget in container.winfo_children():
        widget.destroy()

    conteudo = tk.Frame(container, bg="#1e1e1e")
    conteudo.place(relx=0.5, rely=0.5, anchor="center")

    # --- PAINEL DE CONTROLE ---
    painel = tk.Frame(conteudo, bg="#2d2d2d", width=420, height=600)
    painel.pack(side="left", fill="y", padx=20)
    painel.pack_propagate(False)

    tk.Label(painel, text="🏓 MISSÃO 2: O HERÓI", fg="#4CAF50", 
             bg="#2d2d2d", font=("Courier", 18, "bold")).pack(pady=15)

    # Manual de Instruções
    info = tk.Frame(painel, bg="#3d3d3d", padx=15, pady=10)
    info.pack(fill="x", padx=25, pady=5)
    tk.Label(info, text="🎯 REGRAS DO MOTOR:", fg="#FFD700", bg="#3d3d3d", font=("Arial", 10, "bold")).pack(anchor="w")
    instrucoes = (
        "Para a raquete funcionar bem, use estes limites:\n"
        "• LARGURA: 100 a 150 (pixels)\n"
        "• VELOCIDADE: 10 a 30 (pixels/frame)"
    )
    tk.Label(info, text=instrucoes, fg="#e0e0e0", bg="#3d3d3d", font=("Arial", 10), justify="left").pack(pady=5)

    # --- EDITOR (FOCO INDEPENDENTE) ---
    editor = tk.Frame(painel, bg="#1e1e1e", padx=20, pady=15)
    editor.pack(fill="x", padx=25, pady=10)

    # Campo Largura
    tk.Label(editor, text="# Largura (100-150):", fg="#6A9955", bg="#1e1e1e", font=("Courier", 10)).pack(anchor="w")
    ent_largura = tk.Entry(editor, bg="#1e1e1e", fg="#b5cea8", font=("Courier", 14), 
                          borderwidth=0, highlightthickness=1, 
                          highlightbackground="#444", highlightcolor="#4CAF50")
    ent_largura.pack(fill="x", pady=5)

    # Campo Velocidade
    tk.Label(editor, text="# Velocidade (10-30):", fg="#6A9955", bg="#1e1e1e", font=("Courier", 10)).pack(anchor="w", pady=(10,0))
    ent_vel = tk.Entry(editor, bg="#1e1e1e", fg="#b5cea8", font=("Courier", 14), 
                      borderwidth=0, highlightthickness=1, 
                      highlightbackground="#444", highlightcolor="#4CAF50")
    ent_vel.pack(fill="x", pady=5)

    lbl_feedback = tk.Label(painel, text="Aguardando definições...", fg="#888888", bg="#2d2d2d", font=("Arial", 10, "bold"))
    lbl_feedback.pack(pady=10)

    # Frame de Botões
    btn_frame = tk.Frame(painel, bg="#2d2d2d")
    btn_frame.pack(fill="x", padx=25, pady=5)
    
    frame_proxima = tk.Frame(painel, bg="#2d2d2d")
    frame_proxima.pack(fill="x", padx=25, pady=5)

    tk.Button(btn_frame, text="🧪 TESTAR", bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
              command=lambda: testar_paddle(canvas, ent_largura.get(), ent_vel.get(), root, lbl_feedback)).pack(side="left", expand=True, fill="x", padx=2)

    tk.Button(btn_frame, text="✅ VALIDAR", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
              command=lambda: validar_missao(ent_largura.get(), ent_vel.get(), lbl_feedback, frame_proxima, container, root, cor_fundo)).pack(side="left", expand=True, fill="x", padx=2)

    # --- CANVAS ---
    canvas = tk.Canvas(conteudo, width=400, height=600, bg=cor_fundo, highlightthickness=2, highlightbackground="#444")
    canvas.pack(side="left", padx=20)

def testar_paddle(canvas, larg_str, vel_str, root, label):
    try:
        l, v = int(larg_str), int(vel_str)
        canvas.delete("paddle")
        x1 = 200 - (l / 2)
        x2 = 200 + (l / 2)
        paddle_id = canvas.create_rectangle(x1, 550, x2, 565, fill="white", tags="paddle")
        
        # Movimentação com "if" para não sair da tela
        root.bind("<Left>", lambda e: canvas.move(paddle_id, -v, 0) if canvas.coords(paddle_id)[0] > 0 else None)
        root.bind("<Right>", lambda e: canvas.move(paddle_id, v, 0) if canvas.coords(paddle_id)[2] < 400 else None)
        label.configure(text="✔️ Teste ativo! Use as setas.", fg="#4CAF50")
    except ValueError:
        label.configure(text="❌ Digite apenas números!", fg="#FF5252")

def validar_missao(larg_str, vel_str, label, frame_proxima, container, root, cor):
    try:
        l, v = int(larg_str), int(vel_str)
        if 100 <= l <= 150 and 10 <= v <= 30:
            label.configure(text="✨ Excelente! Raquete aprovada.", fg="#FFD700")
            for w in frame_proxima.winfo_children(): w.destroy()
            
            tk.Button(frame_proxima, text="MISSÃO 3: A BOLA ➡️", bg="#FF9800", fg="white", 
                      font=("Arial", 12, "bold"), pady=15,
                      command=lambda: print("Lançando Missão 3...")).pack(fill="x")
        else:
            label.configure(text="❌ Valores fora do limite permitido!", fg="#FF5252")
    except ValueError:
        label.configure(text="❌ Preencha os campos corretamente!", fg="#FF5252")