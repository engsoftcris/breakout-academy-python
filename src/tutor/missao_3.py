import tkinter as tk
import src.tutor.missao_4 as m4 

def carregar_missao_3(container, root, cor_fundo, larg_r, vel_r):
    """
    MISSÃO 3: SENSOR DE TOQUE (Colisões e Lógica Condicional)
    Conceitos: Estruturas de decisão (IF/ELSE), detecção de colisão e loops de jogo.
    """
    
    # --- 1. LIMPEZA DE AMBIENTE ---
    for widget in container.winfo_children():
        widget.destroy()

    conteudo = tk.Frame(container, bg="#1e1e1e")
    conteudo.place(relx=0.5, rely=0.5, anchor="center")

    # --- 2. PAINEL DE CONTROLE (BARRA LATERAL) ---
    painel = tk.Frame(conteudo, bg="#2d2d2d", width=420, height=600)
    painel.pack(side="left", fill="y", padx=20)
    painel.pack_propagate(False)

    tk.Label(painel, text="🕵️ MISSÃO 3: SENSOR", fg="#FF9800", bg="#2d2d2d", font=("Arial", 16, "bold")).pack(pady=15)

    # --- 3. MANUAL DO PROGRAMADOR ---
    info = tk.Frame(painel, bg="#3d3d3d", padx=15, pady=10)
    info.pack(fill="x", padx=25, pady=5)
    tk.Label(info, text="🎯 SUA TAREFA:", fg="#FFD700", bg="#3d3d3d", font=("Arial", 10, "bold")).pack(anchor="w")
    
    missao_texto = (
        "A bola está fantasma! Ela atravessa tudo.\n"
        "Sua missão é ativar o SENSOR DE COLISÃO para\n"
        "fazer a raquete rebater a bola mágica!"
    )
    tk.Label(info, text=missao_texto, fg="#e0e0e0", bg="#3d3d3d", font=("Arial", 10), justify="left").pack(pady=5)

    # --- 4. CONCEITOS TÉCNICOS ---
    aprenda = tk.Frame(painel, bg="#3d3d3d", padx=15, pady=10)
    aprenda.pack(fill="x", padx=25, pady=5)
    tk.Label(aprenda, text="💡 DICA DO MAGO:", fg="#FFD700", bg="#3d3d3d", font=("Arial", 10, "bold")).pack(anchor="w")
    regras = (
        "Usamos o comando 'IF' (SE) para decidir:\n"
        "SE a bola tocar na raquete -> mude a direção!\n"
        "• VELOCIDADE: 3 a 10 (agilidade da bola)"
    )
    tk.Label(aprenda, text=regras, fg="#e0e0e0", bg="#3d3d3d", font=("Arial", 9, "italic"), justify="left").pack(pady=5)

    # --- 5. EDITOR DE LÓGICA ---
    editor = tk.Frame(painel, bg="#1e1e1e", padx=20, pady=15, highlightthickness=1, highlightbackground="#444")
    editor.pack(fill="x", padx=25, pady=10)

    tk.Label(editor, text="# Velocidade da Bola (3-10):", fg="#6A9955", bg="#1e1e1e", font=("Courier", 10)).pack(anchor="w")
    ent_v = tk.Entry(editor, bg="#1e1e1e", fg="#b5cea8", font=("Courier", 14), borderwidth=0, 
                     highlightthickness=1, highlightbackground="#444", highlightcolor="#4CAF50", justify="center")
    ent_v.pack(fill="x", pady=5)

    tk.Label(editor, text="# Comportamento Físico:", fg="#6A9955", bg="#1e1e1e", font=("Courier", 10)).pack(anchor="w", pady=(10,0))
    opcao_var = tk.StringVar(root)
    opcao_var.set("Atravessar (Fantasma)") 
    menu_acao = tk.OptionMenu(editor, opcao_var, "Atravessar (Fantasma)", "Rebater (Sólido)")
    menu_acao.config(bg="#333", fg="#FFD700", highlightthickness=0, font=("Arial", 10, "bold"))
    menu_acao["menu"].config(bg="#333", fg="#FFD700")
    menu_acao.pack(fill="x", pady=5)

    lbl_status = tk.Label(painel, text="Aguardando teste de física...", fg="#888", bg="#2d2d2d", font=("Arial", 10, "bold"))
    lbl_status.pack(pady=10)

    # --- 6. CONTAINER DE BOTÕES ---
    frame_acao = tk.Frame(painel, bg="#2d2d2d")
    frame_acao.pack(fill="x", padx=25, pady=5)

    estilo_btn = {"font": ("Arial", 10, "bold"), "pady": 15, "fg": "white", "relief": "flat", "cursor": "hand2"}

    # --- 7. TELA DO JOGO (CANVAS) ---
    canvas = tk.Canvas(conteudo, width=400, height=600, bg=cor_fundo, highlightthickness=2, highlightbackground="#444")
    canvas.pack(side="left", padx=20)

    paddle_id = canvas.create_rectangle(200-(larg_r/2), 550, 200+(larg_r/2), 565, fill="white", tags="paddle")
    bola_id = canvas.create_oval(190, 290, 210, 310, fill="#FFD700", tags="bola")

    motor = {"dx": 0, "dy": 0, "ativo": False}

    def engine():
        """O 'coração' do jogo com proteção contra destruição do Canvas."""
        # Se o canvas não existir mais (mudou de missão), paramos o loop imediatamente
        if not canvas.winfo_exists():
            return

        if motor["ativo"]:
            try:
                canvas.move(bola_id, motor["dx"], motor["dy"])
                pos = canvas.coords(bola_id) 

                # 1. Colisão com Paredes Laterais
                if pos[0] <= 0 or pos[2] >= 400: motor["dx"] *= -1
                # 2. Colisão com Teto e Chão
                if pos[1] <= 0 or pos[3] >= 600: motor["dy"] *= -1
                
                # 3. LÓGICA DE REBATER
                if opcao_var.get() == "Rebater (Sólido)":
                    toque = canvas.find_overlapping(*pos)
                    if paddle_id in toque:
                        motor["dy"] = -abs(motor["dy"]) 
                        lbl_status.config(text="⚡ REBATENDO COM SUCESSO!", fg="#4CAF50")
                
                # Agenda a próxima execução
                root.after(16, engine)
            except tk.TclError:
                # Se o canvas for destruído enquanto a função tenta mover a bola, ignoramos o erro
                pass

    def testar():
        """Tenta rodar a física baseada no que o aluno escreveu."""
        try:
            v = int(ent_v.get())
            if 3 <= v <= 10:
                motor["dx"], motor["dy"] = v, -v 
                if not motor["ativo"]:
                    motor["ativo"] = True
                    engine() 
                lbl_status.config(text="🧪 Física em teste...", fg="#2196F3")
                editor.configure(highlightbackground="#2196F3")
                canvas.focus_set() 
            else:
                lbl_status.config(text="❌ Velocidade entre 3 e 10!", fg="#FF5252")
        except ValueError:
            lbl_status.config(text="❌ Digite um número!", fg="#FF5252")

    def validar():
        """Verifica se a lógica de 'Rebater' foi ativada corretamente."""
        try:
            v = int(ent_v.get())
            if opcao_var.get() == "Rebater (Sólido)" and 3 <= v <= 10:
                # SUCESSO - Desativa o motor da missão atual antes de mudar para evitar conflitos
                motor["ativo"] = False
                
                for w in frame_acao.winfo_children(): w.destroy()
                
                lbl_status.config(text="✅ SENSOR ATIVADO! INCRÍVEL!", fg="#FFD700", font=("Arial", 12, "bold"))
                editor.configure(highlightbackground="#4CAF50")
                
                tk.Button(frame_acao, text="MISSÃO 4: OS TIJOLOS ➡️", bg="#4CAF50", 
                          command=lambda: m4.carregar_missao_4(container, root, cor_fundo, larg_r, vel_r), 
                          **estilo_btn).pack(fill="x", pady=10)
            else:
                lbl_status.config(text="⚠️ A bola ainda atravessa tudo!", fg="#FF9800")
                editor.configure(highlightbackground="#FF9800")
        except:
            lbl_status.config(text="❌ Preencha os valores primeiro!", fg="#FF5252")

    tk.Button(frame_acao, text="🧪 TESTAR", bg="#2196F3", command=testar, **estilo_btn).pack(side="left", expand=True, fill="x", padx=2)
    tk.Button(frame_acao, text="✅ VALIDAR", bg="#4CAF50", command=validar, **estilo_btn).pack(side="left", expand=True, fill="x", padx=2)

    root.bind("<Left>", lambda e: canvas.move(paddle_id, -vel_r, 0) if canvas.coords(paddle_id)[0] > 0 else None)
    root.bind("<Right>", lambda e: canvas.move(paddle_id, vel_r, 0) if canvas.coords(paddle_id)[2] < 400 else None)