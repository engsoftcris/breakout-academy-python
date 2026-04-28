import tkinter as tk
from src.tutor.missao_3 import carregar_missao_3

def carregar_missao_2(container, root, cor_fundo):
    """
    MISSÃO 2: O HERÓI (Criação da Raquete/Paddle)
    Conceitos: Variáveis Inteiras, Limites Numéricos e Eventos de Teclado.
    """
    
    # --- 1. LIMPEZA DE RASTRO E EVENTOS ---
    # Importante: Desvincula as teclas para que não haja conflito com missões anteriores
    root.unbind("<Left>")
    root.unbind("<Right>")
    # Remove todos os elementos da tela anterior (Missão 1)
    for widget in container.winfo_children():
        widget.destroy()

    # Estrutura de organização central
    conteudo = tk.Frame(container, bg="#1e1e1e")
    conteudo.place(relx=0.5, rely=0.5, anchor="center")

    # --- 2. PAINEL DE CONTROLE (BARRA LATERAL) ---
    painel = tk.Frame(conteudo, bg="#2d2d2d", width=420, height=600)
    painel.pack(side="left", fill="y", padx=20)
    painel.pack_propagate(False) # Força o frame a respeitar o tamanho definido (width/height)

    # Título da Missão
    tk.Label(painel, text="🏓 MISSÃO 2: O HERÓI", fg="#4CAF50", 
             bg="#2d2d2d", font=("Arial", 16, "bold")).pack(pady=15)

    # --- 3. MANUAL DO GAME DESIGNER (STORYTELLING) ---
    # Bloco de texto que explica o objetivo para a criança (8-12 anos)
    info = tk.Frame(painel, bg="#3d3d3d", padx=15, pady=10)
    info.pack(fill="x", padx=25, pady=5)
    tk.Label(info, text="🎯 SUA TAREFA:", fg="#FFD700", bg="#3d3d3d", font=("Arial", 10, "bold")).pack(anchor="w")
    
    instrucoes_kids = (
        "Um herói precisa de um escudo! Sua missão é criar a\n"
        "raquete do jogo. Escolha o tamanho e a velocidade!"
    )
    tk.Label(info, text=instrucoes_kids, fg="#e0e0e0", bg="#3d3d3d", font=("Arial", 10), justify="left").pack(pady=5)

    # --- 4. CONCEITOS DE PROGRAMAÇÃO (DICA DO MAGO) ---
    # Explicação pedagógica sobre números Inteiros (int)
    aprenda = tk.Frame(painel, bg="#3d3d3d", padx=15, pady=10)
    aprenda.pack(fill="x", padx=25, pady=5)
    tk.Label(aprenda, text="💡 DICA DO MAGO:", fg="#FFD700", bg="#3d3d3d", font=("Arial", 10, "bold")).pack(anchor="w")
    regras = (
        "Números sem aspas são chamados de INTEIROS.\n"
        "• LARGURA: 100 a 150 (tamanho)\n"
        "• VELOCIDADE: 10 a 30 (agilidade)"
    )
    tk.Label(aprenda, text=regras, fg="#e0e0e0", bg="#3d3d3d", font=("Arial", 9, "italic"), justify="left").pack(pady=5)

    # --- 5. EDITOR DE ATRIBUTOS (CAMPOS DE ENTRADA) ---
    # Onde o aluno digita os valores para configurar o objeto raquete
    editor = tk.Frame(painel, bg="#1e1e1e", padx=20, pady=15, highlightthickness=1, highlightbackground="#444")
    editor.pack(fill="x", padx=25, pady=10)

    # Entrada para a LARGURA (Width)
    tk.Label(editor, text="# Tamanho da Raquete (100-150):", fg="#6A9955", bg="#1e1e1e", font=("Courier", 10)).pack(anchor="w")
    ent_largura = tk.Entry(editor, bg="#1e1e1e", fg="#b5cea8", font=("Courier", 14), borderwidth=0, 
                          highlightthickness=1, highlightbackground="#444", highlightcolor="#4CAF50")
    ent_largura.pack(fill="x", pady=5)
    ent_largura.focus_set() # Cursor já começa aqui para facilitar

    # Entrada para a VELOCIDADE (Speed)
    tk.Label(editor, text="# Agilidade/Velocidade (10-30):", fg="#6A9955", bg="#1e1e1e", font=("Courier", 10)).pack(anchor="w", pady=(10,0))
    ent_vel = tk.Entry(editor, bg="#1e1e1e", fg="#b5cea8", font=("Courier", 14), borderwidth=0, 
                      highlightthickness=1, highlightbackground="#444", highlightcolor="#4CAF50")
    ent_vel.pack(fill="x", pady=5)

    # Texto que muda para dar dicas ou avisar erros
    lbl_feedback = tk.Label(painel, text="Aguardando definições...", fg="#888888", bg="#2d2d2d", font=("Arial", 11, "bold"))
    lbl_feedback.pack(pady=10)

    # --- 6. ÁREA DOS BOTÕES (INTERAÇÃO) ---
    # Este frame armazena os botões e será limpo na validação final (conforme Missão 1)
    frame_acao = tk.Frame(painel, bg="#2d2d2d")
    frame_acao.pack(fill="x", padx=25, pady=5)

    estilo_btn = {"font": ("Arial", 10, "bold"), "pady": 15, "fg": "white", "relief": "flat", "cursor": "hand2"}

    # Botão de Teste: permite ver a raquete e movê-la sem concluir a missão
    btn_testar = tk.Button(frame_acao, text="🧪 TESTAR", bg="#2196F3", 
                           command=lambda: testar_paddle(canvas, ent_largura, ent_vel, root, lbl_feedback, editor))
    btn_testar.config(**estilo_btn)
    btn_testar.pack(side="left", expand=True, fill="x", padx=2)

    # Botão de Validar: verifica os números e libera a próxima fase
    btn_validar = tk.Button(frame_acao, text="✅ VALIDAR", bg="#4CAF50", 
                            command=lambda: concluir_missao(ent_largura, ent_vel, lbl_feedback, frame_acao, container, root, cor_fundo, editor))
    btn_validar.config(**estilo_btn)
    btn_validar.pack(side="left", expand=True, fill="x", padx=2)

    # --- 7. ESPAÇO VISUAL (CANVAS) ---
    # Exibe o jogo em tempo real com a cor de fundo herdada da Missão 1
    canvas = tk.Canvas(conteudo, width=400, height=600, bg=cor_fundo, highlightthickness=2, highlightbackground="#444")
    canvas.pack(side="left", padx=20)

# --- FUNÇÕES DE LÓGICA ---

def testar_paddle(canvas, ent_larg, ent_vel, root, label, editor):
    """Lógica para desenhar a raquete e habilitar o controle pelo teclado."""
    try:
        # Tenta converter o texto para número. Se não for número, vai para o 'except'
        l, v = int(ent_larg.get()), int(ent_vel.get())
        
        canvas.delete("paddle") # Remove raquetes antigas do cenário
        
        # Calcula as posições X para centralizar a raquete no início
        x1, x2 = 200 - (l / 2), 200 + (l / 2)
        paddle_id = canvas.create_rectangle(x1, 550, x2, 565, fill="white", tags="paddle")
        
        # Vincula as teclas de seta. O 'if' impede que a raquete saia dos limites do Canvas (0-400)
        root.bind("<Left>", lambda e: canvas.move(paddle_id, -v, 0) if canvas.coords(paddle_id)[0] > 0 else None)
        root.bind("<Right>", lambda e: canvas.move(paddle_id, v, 0) if canvas.coords(paddle_id)[2] < 400 else None)
        
        label.configure(text="✔️ Teste ativo! Use as setas.", fg="#4CAF50")
        editor.configure(highlightbackground="#4CAF50") # Borda verde de sucesso
        canvas.focus_set() # Tira o foco do teclado do campo de texto e manda para o jogo
        
    except ValueError:
        label.configure(text="❌ Use apenas números inteiros!", fg="#FF5252")
        editor.configure(highlightbackground="#FF5252") # Borda vermelha de erro

def concluir_missao(ent_larg, ent_vel, label, frame_acao, container, root, cor, editor):
    """Verifica as regras de negócio e prepara o terreno para a Missão 3."""
    try:
        l, v = int(ent_larg.get()), int(ent_vel.get())
        
        # Regra pedagógica: a raquete não pode ser minúscula nem gigante, nem rápida demais
        if 100 <= l <= 150 and 10 <= v <= 30:
            
            # Limpa todos os botões do frame_acao para não ficar 'espremido'
            for widget in frame_acao.winfo_children():
                widget.destroy()
            
            # Atualiza o feedback visual de vitória
            label.configure(text="✨ VOCÊ É UM DESIGNER! ✨", fg="#FFD700", font=("Arial", 14, "bold"))
            editor.configure(highlightbackground="#4CAF50")
            
            # Cria o botão de transição ocupando todo o espaço disponível
            tk.Button(frame_acao, text="PRÓXIMO PASSO: A BOLA MÁGICA ➡️", bg="#FF9800", fg="white", 
                      font=("Arial", 12, "bold"), pady=15, cursor="hand2",
                      command=lambda: carregar_missao_3(container, root, cor, l, v)).pack(fill="x", pady=10)
        else:
            # Caso o aluno use números fora da faixa sugerida
            label.configure(text="🤔 Valores fora das regras!", fg="#FF5252")
            editor.configure(highlightbackground="#FF5252")
            
    except ValueError:
        # Caso o aluno deixe vazio ou digite letras
        label.configure(text="❌ Preencha com números!", fg="#FF5252")
        editor.configure(highlightbackground="#FF5252")