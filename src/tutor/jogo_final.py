import tkinter as tk
import os
import pygame
import src.tutor.missao_1 as m1 # IMPORTANTE: Importamos a Missão 1 para permitir o reinício

def iniciar_jogo_final(container, root, cor_fundo, larg_r, vel_r, vidas_ini, pts_bloco):
    """
    MODO ARCADE DEFINITIVO:
    - Reinício automático após perder vida.
    - Proteção contra erros de fechamento (TclError).
    - Reiniciar Tutorial agora funciona na mesma janela.
    
    """
    
    # --- 1. LIMPEZA DE TELA ---
    # Limpa o container para garantir que não haja sobreposição de missões anteriores
    for widget in container.winfo_children():
        widget.destroy()

    # --- 2. SETUP DE ÁUDIO (SONOPLASTIA) ---
    # Inicializa o mixer para tocar os arquivos de som carregados da pasta assets
    pygame.mixer.init()
    path_sounds = os.path.join("assets", "sounds")
    sons = {arq: pygame.mixer.Sound(os.path.join(path_sounds, arq)) 
            for arq in ["bounce.wav", "paddle_hit.wav", "block_hit.wav"] 
            if os.path.exists(os.path.join(path_sounds, arq))}

    # --- 3. ESTADO DO JOGO (VARIÁVEIS DE CONTROLE) ---
    # Usamos um dicionário para agrupar as variáveis e facilitar o acesso em funções internas
    game = {
        "score": 0, 
        "vidas": vidas_ini, 
        "ativo": False, # O jogo começa pausado aguardando o ESPAÇO
        "blocos": [], 
        "dx": 5, 
        "dy": 5, 
        "loop_id": None   
    }

    # Frame para centralizar o Canvas na tela
    frame_arcade = tk.Frame(container, bg="#1e1e1e")
    frame_arcade.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame_arcade, text="🕹️ BREAKOUT PRO: ARCADE", fg="#FF9800", 
             bg="#1e1e1e", font=("Arial", 20, "bold")).pack(pady=10)

    # --- 4. CRIAÇÃO DO MUNDO GRÁFICO (CANVAS) ---
    canvas = tk.Canvas(frame_arcade, width=400, height=600, bg=cor_fundo, 
                       highlightthickness=4, highlightbackground="#FF9800")
    canvas.pack()

    # Criação dos objetos: Raquete (paddle) e Bola
    paddle_id = canvas.create_rectangle(200-(larg_r/2), 550, 200+(larg_r/2), 565, fill="white")
    bola_id = canvas.create_oval(190, 250, 210, 270, fill="#FFD700")
    
    # Interface de Usuário (HUD) para mostrar Vidas e Pontuação
    txt_v = canvas.create_text(330, 30, text="❤️" * game["vidas"], fill="#FF5252", font=("Arial", 12, "bold"))
    txt_s = canvas.create_text(70, 30, text="SCORE: 0", fill="white", font=("Arial", 12, "bold"))

    # --- 5. MOTOR DO JOGO (ENGINE) ---
    def engine():
        """ Loop principal que processa a física e as colisões. """
        # SEGURANÇA: Se o usuário trocou de tela, o canvas não existe mais. Paramos o loop aqui.
        if not canvas.winfo_exists():
            return
            
        if not game["ativo"]: return 

        try:
            # Move a bola de acordo com as velocidades dx e dy
            canvas.move(bola_id, game["dx"], game["dy"])
            pos = canvas.coords(bola_id)

            # Colisão com as paredes laterais (Eixo X)
            if pos[0] <= 0 or pos[2] >= 400: 
                game["dx"] *= -1
                if "bounce.wav" in sons: sons["bounce.wav"].play()

            # Colisão com o teto (Eixo Y)
            if pos[1] <= 0: 
                game["dy"] = abs(game["dy"])

            # EVENTO: BOLA CAIU NO CHÃO (Perda de vida)
            if pos[3] >= 600:
                recomeçar_vida()
                return

            # Busca objetos que estão encostando na bola
            items = canvas.find_overlapping(*pos)
            
            # Colisão com a Raquete do jogador
            if paddle_id in items:
                game["dy"] = -abs(game["dy"]) # Garante que a bola suba
                if "paddle_hit.wav" in sons: sons["paddle_hit.wav"].play()

            # Colisão com os Blocos (Loop de destruição)
            for b in game["blocos"][:]:
                if b in items:
                    canvas.delete(b) # Remove visualmente
                    game["blocos"].remove(b) # Remove da lista lógica
                    game["score"] += pts_bloco
                    game["dy"] *= -1 # Rebate a bola
                    canvas.itemconfig(txt_s, text=f"SCORE: {game['score']}")
                    if "block_hit.wav" in sons: sons["block_hit.wav"].play()
                    break

            # Verifica se o jogador venceu (limpou o tabuleiro)
            if not game["blocos"]:
                finalizar_jogo("VITÓRIA! 🏆", "#4CAF50")
                return

            # Agenda o próximo frame (aproximadamente 60 FPS)
            game["loop_id"] = root.after(16, engine)

        except tk.TclError:
            pass # Ignora erros se a janela for fechada durante o movimento

    # --- 6. LÓGICA DE REINÍCIO E ESTADOS ---
    def recomeçar_vida():
        """ Perde uma vida e reseta a bola sem parar o fluxo do jogo. """
        game["vidas"] -= 1
        canvas.itemconfig(txt_v, text="❤️" * game["vidas"] if game["vidas"] > 0 else "💀")
        
        if game["vidas"] <= 0:
            finalizar_jogo("GAME OVER\n[ ESPAÇO ] REINICIAR", "red")
        else:
            # Posiciona a bola no centro e continua após 500ms
            canvas.coords(bola_id, 190, 250, 210, 270)
            game["dy"] = 5 
            game["dx"] = 5
            root.after(500, engine)

    def finalizar_jogo(texto, cor):
        """ Para o motor e exibe a mensagem de fim de jogo. """
        game["ativo"] = False
        canvas.create_text(200, 300, text=texto, fill=cor, font=("Arial", 20, "bold"), tags="msg", justify="center")

    def comando_espaco(e):
        """ Controla o início da partida ou o reset após Game Over. """
        if not game["ativo"]:
            # Se o jogo acabou ou não há blocos, reinicia o tabuleiro inteiro
            if game["vidas"] <= 0 or not game["blocos"]:
                game["vidas"] = vidas_ini
                game["score"] = 0
                canvas.itemconfig(txt_v, text="❤️" * game["vidas"])
                canvas.itemconfig(txt_s, text="SCORE: 0")
                reiniciar_tabuleiro()
            
            canvas.delete("msg") 
            game["ativo"] = True
            engine()

    def reiniciar_tabuleiro():
        """ Limpa blocos antigos e cria novos para uma nova partida. """
        for b in game["blocos"]: canvas.delete(b)
        game["blocos"].clear()
        criar_blocos()
        canvas.coords(bola_id, 190, 250, 210, 270)
        game["dy"] = 5

    def criar_blocos():
        """ Função clássica para gerar a grade de alvos. """
        cores = ["#FF5252", "#FFEB3B", "#2196F3"]
        for l in range(3):
            for c in range(5):
                b = canvas.create_rectangle(10+c*78, 60+l*25, 83+c*78, 80+l*25, fill=cores[l], outline="#1e1e1e")
                game["blocos"].append(b)

    # --- 7. AJUSTE DE REINÍCIO (NA MESMA JANELA) ---
    def reiniciar_tutorial_mesma_janela():
        """ Para o jogo arcade e volta para a Missão 1 limpando o container. """
        game["ativo"] = False 
        # Chamamos a missão 1 
        m1.carregar_missao_1(container, root)

    # --- 8. CONTROLES E INTERFACE FINAL ---
    criar_blocos()
    canvas.create_text(200, 400, text="[ ESPAÇO ] PARA COMEÇAR", fill="#FFD700", font=("Arial", 14, "bold"), tags="msg")
    
    # Eventos de teclado
    root.bind("<Left>", lambda e: canvas.move(paddle_id, -vel_r, 0) if canvas.coords(paddle_id)[0] > 0 else None)
    root.bind("<Right>", lambda e: canvas.move(paddle_id, vel_r, 0) if canvas.coords(paddle_id)[2] < 400 else None)
    root.bind("<space>", comando_espaco)

    # Botões de rodapé para navegação
    btn_frame = tk.Frame(frame_arcade, bg="#1e1e1e")
    btn_frame.pack(pady=10)
    
    # Botão REINICIAR: Agora volta para a Missão 1 sem abrir novas janelas
    tk.Button(btn_frame, text="🔄 REINICIAR TUTORIAL", bg="#444", fg="white", font=("Arial", 9, "bold"),
              command=reiniciar_tutorial_mesma_janela).pack(side="left", padx=5)
              
    tk.Button(btn_frame, text="❌ FECHAR JOGO", bg="#b91c1c", fg="white", font=("Arial", 9, "bold"),
              command=root.destroy).pack(side="left", padx=5)