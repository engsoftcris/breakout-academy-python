import tkinter as tk
# Importamos a missão 4 para que o botão saiba o que carregar
import src.tutor.missao_4 as m4 

def carregar_missao_3(container, root, cor_fundo, larg_r, vel_r, callback_proxima=None):
    for widget in container.winfo_children():
        widget.destroy()

    conteudo = tk.Frame(container, bg="#1e1e1e")
    conteudo.place(relx=0.5, rely=0.5, anchor="center")

    # --- PAINEL DE CONTROLE ---
    painel = tk.Frame(conteudo, bg="#2d2d2d", width=380, height=580)
    painel.pack(side="left", fill="y", padx=10)
    painel.pack_propagate(False)

    tk.Label(painel, text="🕵️ SENSOR DE TOQUE", fg="#FF9800", bg="#2d2d2d", font=("Arial", 18, "bold")).pack(pady=15)

    # Entrada de Velocidade
    tk.Label(painel, text="Velocidade da Bola (3-10):", fg="white", bg="#2d2d2d").pack()
    ent_v = tk.Entry(painel, bg="#1e1e1e", fg="white", justify="center", borderwidth=0)
    ent_v.insert(0, "5")
    ent_v.pack(pady=5, padx=40, fill="x")

    # Escolha da Lógica
    tk.Label(painel, text="O que a raquete deve fazer?", fg="#4CAF50", bg="#2d2d2d").pack(pady=(15,0))
    opcao_var = tk.StringVar(root)
    opcao_var.set("Atravessar (Fantasma)") 
    menu_acao = tk.OptionMenu(painel, opcao_var, "Atravessar (Fantasma)", "Rebater (Sólido)")
    menu_acao.pack(pady=10, padx=40, fill="x")

    lbl_status = tk.Label(painel, text="Aguardando Teste...", fg="#888", bg="#2d2d2d", font=("Arial", 10, "bold"))
    lbl_status.pack(pady=20)

    # --- ÁREA DO JOGO ---
    canvas = tk.Canvas(conteudo, width=400, height=600, bg=cor_fundo, highlightthickness=0)
    canvas.pack(side="left")

    paddle = canvas.create_rectangle(200-(larg_r/2), 550, 200+(larg_r/2), 565, fill="white", tags="paddle")
    bola = canvas.create_oval(190, 290, 210, 310, fill="#FFD700", tags="bola")

    conf = {"dx": 0, "dy": 0, "ativo": False}

    def engine():
        if conf["ativo"]:
            canvas.move("bola", conf["dx"], conf["dy"])
            pos = canvas.coords("bola")
            if pos[0] <= 0 or pos[2] >= 400: conf["dx"] *= -1
            if pos[1] <= 0 or pos[3] >= 600: conf["dy"] *= -1
            
            if opcao_var.get() == "Rebater (Sólido)":
                toque = canvas.find_overlapping(*pos)
                if paddle in toque:
                    conf["dy"] = -abs(conf["dy"])
                    lbl_status.config(text="⚡ REBATENDO!", fg="#4CAF50")
            root.after(16, engine)

    def testar():
        try:
            v = int(ent_v.get())
            conf["dx"], conf["dy"] = v, -v
            if not conf["ativo"]:
                conf["ativo"] = True
                engine()
        except: pass

    def validar():
        if opcao_var.get() == "Rebater (Sólido)":
            lbl_status.config(text="✅ SENSOR VALIDADO!", fg="#4CAF50")
            
            # CRIANDO O BOTÃO PARA A MISSÃO 4
            # Se não veio callback, usamos a função da missao_4 que importamos
            comando = callback_proxima if callback_proxima else lambda: m4.carregar_missao_4(container, root, cor_fundo, larg_r, vel_r)
            
            btn_proxima = tk.Button(painel, text="MISSÃO 4 ➡️", 
                                    command=comando, 
                                    bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
            btn_proxima.pack(pady=10, fill="x", padx=40)
        else:
            lbl_status.config(text="⚠️ Selecione 'Rebater'!", fg="#FF9800")

    # Botões Principais
    btn_frame = tk.Frame(painel, bg="#2d2d2d")
    btn_frame.pack(fill="x", padx=40)
    tk.Button(btn_frame, text="🧪 TESTAR", command=testar, bg="#2196F3", fg="white").pack(side="left", expand=True, fill="x", padx=2)
    tk.Button(btn_frame, text="✅ VALIDAR", command=validar, bg="#4CAF50", fg="white").pack(side="left", expand=True, fill="x", padx=2)

    root.bind("<Left>", lambda e: canvas.move("paddle", -vel_r, 0) if canvas.coords("paddle")[0] > 0 else None)
    root.bind("<Right>", lambda e: canvas.move("paddle", vel_r, 0) if canvas.coords("paddle")[2] < 400 else None)