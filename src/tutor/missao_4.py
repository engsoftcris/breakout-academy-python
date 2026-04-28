import tkinter as tk
import os
import pygame
import src.tutor.missao_5 as m5 

def carregar_missao_4(container, root, cor_fundo, larg_r, vel_r):
    """
    MISSÃO 4: SISTEMA DE BLOCOS E SONOPLASTIA
    Conceitos: Listas de objetos, Loops de verificação e Manipulação de Áudio.
    """
    
    # --- 1. LIMPEZA E INICIALIZAÇÃO DE ÁUDIO ---
    for widget in container.winfo_children():
        widget.destroy()

    # Inicializa o mixer do Pygame para tocar os efeitos sonoros (SFX)
    pygame.mixer.init()
    path_sounds = os.path.join("assets", "sounds")
    sons = {}
    
    # Tentamos carregar cada som. Se o arquivo não existir, o jogo não trava (robusto!)
    for arquivo in ["bounce.wav", "paddle_hit.wav", "block_hit.wav"]:
        caminho = os.path.join(path_sounds, arquivo)
        if os.path.exists(caminho):
            sons[arquivo] = pygame.mixer.Sound(caminho)

    # Layout centralizado
    conteudo = tk.Frame(container, bg="#1e1e1e")
    conteudo.place(relx=0.5, rely=0.5, anchor="center")

    # --- 2. PAINEL DE CONTROLE (SIDEBAR) ---
    painel = tk.Frame(conteudo, bg="#2d2d2d", width=420, height=600)
    painel.pack(side="left", fill="y", padx=20)
    painel.pack_propagate(False)

    tk.Label(painel, text="🧱 MISSÃO 4: FÍSICA E SOM", fg="#FF9800", 
             bg="#2d2d2d", font=("Arial", 16, "bold")).pack(pady=15)

    # --- 3. MANUAL DO DESENVOLVEDOR (STORYTELLING) ---
    info = tk.Frame(painel, bg="#3d3d3d", padx=15, pady=10)
    info.pack(fill="x", padx=25, pady=5)
    tk.Label(info, text="🎯 SUA TAREFA:", fg="#FFD700", bg="#3d3d3d", font=("Arial", 10, "bold")).pack(anchor="w")
    
    missao_texto = (
        "O jogo está sem graça: a bola cai no vazio,\n"
        "os blocos são indestrutíveis e não há som!\n"
        "Programe as regras finais para o protótipo."
    )
    tk.Label(info, text=missao_texto, fg="#e0e0e0", bg="#3d3d3d", font=("Arial", 10), justify="left").pack(pady=5)

    # --- 4. DICA DO MAGO (CONCEITOS) ---
    aprenda = tk.Frame(painel, bg="#3d3d3d", padx=15, pady=10)
    aprenda.pack(fill="x", padx=25, pady=5)
    tk.Label(aprenda, text="💡 DICA DO MAGO:", fg="#FFD700", bg="#3d3d3d", font=("Arial", 10, "bold")).pack(anchor="w")
    regras = (
        "• BOOLEANOS: Variáveis de Sim ou Não (True/False).\n"
        "• SFX: Sons curtos que dão vida às ações.\n"
        "• LISTAS: Usamos para controlar muitos blocos de vez!"
    )
    tk.Label(aprenda, text=regras, fg="#e0e0e0", bg="#3d3d3d", font=("Arial", 9, "italic"), justify="left").pack(pady=5)

    # --- 5. LABORATÓRIO DE PROGRAMAÇÃO (CHECKBOXES) ---
    editor = tk.Frame(painel, bg="#1e1e1e", padx=20, pady=15, highlightthickness=1, highlightbackground="#444")
    editor.pack(fill="x", padx=25, pady=10)

    ativar_quique = tk.BooleanVar(value=False)
    ativar_destruicao = tk.BooleanVar(value=False)
    ativar_sons = tk.BooleanVar(value=False)

    estilo_check = {"bg": "#1e1e1e", "fg": "#4CAF50", "selectcolor": "#2d2d2d", 
                    "activebackground": "#1e1e1e", "font": ("Courier", 10)}

    tk.Checkbutton(editor, text="> bola_quica_no_chao = True", variable=ativar_quique, **estilo_check).pack(anchor="w")
    tk.Checkbutton(editor, text="> destruir_blocos = True", variable=ativar_destruicao, **estilo_check).pack(anchor="w", pady=5)
    tk.Checkbutton(editor, text="> ligar_sons_sfx = True", variable=ativar_sons, **estilo_check).pack(anchor="w")

    lbl_status = tk.Label(painel, text="Sistema aguardando compilação...", fg="#888", bg="#2d2d2d", font=("Arial", 9, "italic"))
    lbl_status.pack(pady=10)

    # --- 6. ÁREA DE BOTÕES ---
    frame_acao = tk.Frame(painel, bg="#2d2d2d")
    frame_acao.pack(fill="x", padx=25, pady=5)
    estilo_btn = {"font": ("Arial", 10, "bold"), "pady": 15, "fg": "white", "relief": "flat", "cursor": "hand2"}

    # --- 7. ÁREA DO JOGO (CANVAS) ---
    canvas = tk.Canvas(conteudo, width=400, height=600, bg=cor_fundo, highlightthickness=2, highlightbackground="#444")
    canvas.pack(side="left", padx=20)

    paddle_id = canvas.create_rectangle(200-(larg_r/2), 550, 200+(larg_r/2), 565, fill="white", tags="paddle")
    bola_id = canvas.create_oval(190, 290, 210, 310, fill="#FFD700", tags="bola")

    blocos = []
    def criar_blocos():
        cores = ["#FF5252", "#FFEB3B", "#2196F3"]
        for l in range(3): 
            for c in range(5): 
                b = canvas.create_rectangle(10+c*78, 50+l*25, 83+c*78, 70+l*25, fill=cores[l], tags="bloco")
                blocos.append(b)

    criar_blocos()
    motor = {"dx": 5, "dy": -5, "ativo": False}

    def tocar_som(nome):
        """Toca um som se o aluno tiver ativado a opção."""
        if ativar_sons.get() and nome in sons:
            sons[nome].play()

    def engine():
        """O Loop de física com verificação de listas e proteção de memória."""
        # SEGURANÇA: Se o canvas foi destruído (mudança de missão), mata o loop
        if not canvas.winfo_exists():
            return

        if motor["ativo"]:
            try:
                canvas.move(bola_id, motor["dx"], motor["dy"])
                pos = canvas.coords(bola_id)

                # Rebote nas bordas e teto
                if pos[0] <= 0 or pos[2] >= 400:
                    motor["dx"] *= -1
                    tocar_som("bounce.wav")
                
                if pos[1] <= 0:
                    motor["dy"] *= -1
                    tocar_som("bounce.wav")

                # Lógica do Chão
                if pos[3] >= 600:
                    if ativar_quique.get():
                        motor["dy"] = -abs(motor["dy"])
                        tocar_som("bounce.wav")
                    else:
                        motor["ativo"] = False
                        lbl_status.config(text="⚠️ BOLA PERDIDA! Ative o quique no chão.", fg="#FF5252")

                # Colisão com Raquete
                toque = canvas.find_overlapping(*pos)
                if paddle_id in toque:
                    motor["dy"] = -abs(motor["dy"])
                    tocar_som("paddle_hit.wav")

                # Colisão com Blocos (Verificação em Lista)
                for b in blocos[:]: 
                    if b in toque:
                        if ativar_destruicao.get():
                            canvas.delete(b)
                            blocos.remove(b)
                            motor["dy"] *= -1
                            tocar_som("block_hit.wav")
                            if not blocos:
                                lbl_status.config(text="🏆 TODOS OS BLOCOS DESTRUÍDOS!", fg="#FFD700")
                        break

                root.after(16, engine)
            except tk.TclError:
                pass # Evita erro se fechar durante o movimento

    # --- FUNÇÕES DE BOTÃO ---
    def lancar():
        if not motor["ativo"]:
            motor["ativo"] = True
            engine()
            lbl_status.config(text="🚀 Simulação iniciada!", fg="#2196F3")
            editor.configure(highlightbackground="#2196F3")

    def validar():
        if ativar_quique.get() and ativar_destruicao.get() and ativar_sons.get():
            # SEGURANÇA: Para o motor antes de mudar de tela
            motor["ativo"] = False
            
            for w in frame_acao.winfo_children(): w.destroy()
            
            lbl_status.config(text="✅ MOTOR COMPLETO! VOCÊ É FERA!", fg="#4CAF50", font=("Arial", 12, "bold"))
            editor.configure(highlightbackground="#4CAF50")
            
            tk.Button(frame_acao, text="ÚLTIMA MISSÃO: O MESTRE ➡️", bg="#4CAF50", 
                      command=lambda: m5.carregar_missao_5(container, root, cor_fundo, larg_r, vel_r), 
                      **estilo_btn).pack(fill="x", pady=10)
        else:
            lbl_status.config(text="🤔 Algo falta... A física não está completa!", fg="#FF9800")
            editor.configure(highlightbackground="#FF9800")

    tk.Button(frame_acao, text="🧪 LANÇAR", bg="#2196F3", command=lancar, **estilo_btn).pack(side="left", expand=True, fill="x", padx=2)
    tk.Button(frame_acao, text="✅ VALIDAR", bg="#4CAF50", command=validar, **estilo_btn).pack(side="left", expand=True, fill="x", padx=2)

    root.bind("<Left>", lambda e: canvas.move(paddle_id, -vel_r, 0) if canvas.coords(paddle_id)[0] > 0 else None)
    root.bind("<Right>", lambda e: canvas.move(paddle_id, vel_r, 0) if canvas.coords(paddle_id)[2] < 400 else None)