import tkinter as tk
from src.tutor.missao_2 import carregar_missao_2

def carregar_missao_1(container, root):
    """
    Missão 1: O Pintor de Mundos.
    Objetivo Pedagógico: Ensinar o conceito de 'Strings' (textos) e como elas 
    alteram propriedades visuais em um programa.
    """
    
    # --- 1. LIMPEZA DE AMBIENTE ---
    # Destrói widgets antigos para garantir que a tela esteja limpa para a nova missão
    for widget in container.winfo_children():
        widget.destroy()

    # --- 2. LAYOUT PRINCIPAL ---
    # Container centralizado para organizar o painel (esquerda) e o canvas (direita)
    conteudo = tk.Frame(container, bg="#1e1e1e")
    conteudo.place(relx=0.5, rely=0.5, anchor="center")

    # --- 3. PAINEL DE COMANDOS (SIDEBAR) ---
    painel = tk.Frame(conteudo, bg="#2d2d2d", width=420, height=600)
    painel.pack(side="left", fill="y", padx=20)
    painel.pack_propagate(False) # Impede que o painel encolha com o conteúdo

    # Título amigável para a criança
    tk.Label(painel, text="🎨 MISSÃO 1: PINTOR DE MUNDOS", fg="#4CAF50", 
             bg="#2d2d2d", font=("Arial", 16, "bold")).pack(pady=15)

    # --- 4. ÁREA DE TEXTO LÚDICO (STORYTELLING) ---
    missao_info = tk.Frame(painel, bg="#3d3d3d", padx=15, pady=10)
    missao_info.pack(fill="x", padx=25, pady=5)
    
    tk.Label(missao_info, text="🎯 SUA TAREFA:", fg="#FFD700", bg="#3d3d3d", font=("Arial", 10, "bold")).pack(anchor="w")
    
    # Texto adaptado para 8-12 anos
    objetivo_kids = (
        "Sua primeira missão de Game Designer: escolher a cor\n"
        "do fundo do seu jogo! Use o comando de COR para\n"
        "dar vida ao cenário!"
    )
    tk.Label(missao_info, text=objetivo_kids, fg="#e0e0e0", bg="#3d3d3d", font=("Arial", 10), justify="left").pack(pady=5)

    # Explicação simplificada de conceitos técnicos (Dica do Mago)
    aprenda = tk.Frame(painel, bg="#3d3d3d", padx=15, pady=10)
    aprenda.pack(fill="x", padx=25, pady=5)
    
    tk.Label(aprenda, text="💡 DICA DO MAGO:", fg="#FFD700", bg="#3d3d3d", font=("Arial", 10, "bold")).pack(anchor="w")
    info_kids = (
        "Textos em código se chamam STRINGS.\n"
        "As aspas \" \" são como uma caixa que guarda\n"
        "o nome da cor para o computador entender!"
    )
    tk.Label(aprenda, text=info_kids, fg="#e0e0e0", bg="#3d3d3d", font=("Arial", 9, "italic"), justify="left").pack(pady=5)

    # --- 5. INVENTÁRIO (CORES DISPONÍVEIS - SEM AMARELO, BRANCO OU VERMELHO) ---
    # Removemos 'yellow' para não camuflar a bola, e 'white'/'red' pelos textos e vidas.
    tk.Label(painel, text="🌈 SEU INVENTÁRIO DE CORES:", fg="#FFD700", bg="#2d2d2d", font=("Arial", 10, "bold")).pack(pady=(10,0))
    CORES_LISTA = ["blue", "green", "purple", "orange", "black", "cyan", "magenta"]
    tk.Label(painel, text=", ".join(CORES_LISTA), fg="#4CAF50", bg="#2d2d2d", 
             font=("Courier", 11, "bold"), wraplength=350).pack()

    # --- 6. SIMULADOR DE CÓDIGO (IDE) ---
    editor = tk.Frame(painel, bg="#1e1e1e", padx=20, pady=20, highlightthickness=1, highlightbackground="#444")
    editor.pack(fill="x", padx=25, pady=10)

    tk.Label(editor, text="# Escolha a cor do seu mundo:", fg="#6A9955", bg="#1e1e1e", font=("Courier", 10)).pack(anchor="w")
    
    f_cor = tk.Frame(editor, bg="#1e1e1e")
    f_cor.pack(fill="x", pady=5)
    
    tk.Label(f_cor, text='cor_fundo = "', fg="#ce9178", bg="#1e1e1e", font=("Courier", 14)).pack(side="left")
    ent_cor = tk.Entry(f_cor, bg="#1e1e1e", fg="#9cdcfe", insertbackground="white", 
                       font=("Courier", 14), borderwidth=0, width=12)
    ent_cor.pack(side="left")
    ent_cor.focus_set() 
    tk.Label(f_cor, text='"', fg="#ce9178", bg="#1e1e1e", font=("Courier", 14)).pack(side="left")

    # Label de feedback para mensagens de erro ou elogios
    lbl_feedback = tk.Label(painel, text="Esperando seu comando...", fg="#888888", bg="#2d2d2d", font=("Arial", 11, "bold"))
    lbl_feedback.pack(pady=10)

    # --- 7. BOTÕES DE AÇÃO ---
    frame_botoes = tk.Frame(painel, bg="#2d2d2d")
    frame_botoes.pack(fill="x", padx=25, pady=5)
    estilo_btn = {"font": ("Arial", 10, "bold"), "pady": 15, "fg": "white", "relief": "flat", "cursor": "hand2"}

    # Atalho de teclado: ENTER
    root.bind('<Return>', lambda e: validar_e_testar(ent_cor.get(), canvas, lbl_feedback, CORES_LISTA, editor))

    tk.Button(frame_botoes, text="🧪 TESTAR COR", bg="#2196F3", 
              command=lambda: validar_e_testar(ent_cor.get(), canvas, lbl_feedback, CORES_LISTA, editor), **estilo_btn).pack(side="left", fill="x", expand=True, padx=2)

    tk.Button(frame_botoes, text="✅ VALIDAR", bg="#4CAF50", 
              command=lambda: concluir_missao(ent_cor.get(), canvas, frame_botoes, lbl_feedback, CORES_LISTA, container, root, editor), **estilo_btn).pack(side="left", fill="x", expand=True, padx=2)

    # --- 8. VISUALIZAÇÃO DO JOGO (CANVAS) ---
    canvas = tk.Canvas(conteudo, width=400, height=600, bg="#111111", highlightthickness=2, highlightbackground="#444")
    canvas.pack(side="left", padx=20)

# --- FUNÇÕES DE LÓGICA ---

def validar_e_testar(valor, canvas, label, lista, editor):
    """ Verifica se a cor digitada é válida e segura para o jogo. """
    cor = valor.strip().lower() 
    
    if cor in lista:
        canvas.configure(bg=cor) 
        label.configure(text=f"🤩 Incrível! O mundo agora é {cor}!", fg="#4CAF50")
        editor.configure(highlightbackground="#4CAF50") 
        return True
    elif cor in ["white", "red", "yellow"]:
        label.configure(text="⚠️ Essa cor esconde os itens do jogo! Tente outra.", fg="#FF9800")
        editor.configure(highlightbackground="#FF9800")
        return False
    else:
        label.configure(text="🤔 Hum, essa cor não está no inventário!", fg="#FF5252")
        editor.configure(highlightbackground="#FF5252") 
        return False

def concluir_missao(valor, canvas, frame_botoes, label, lista, container, root, editor):
    """ Finaliza a missão 1 e envia a cor segura para a Missão 2. """
    if validar_e_testar(valor, canvas, label, lista, editor):
        cor_escolhida = valor.strip().lower() 
        root.unbind('<Return>') 
        
        for widget in frame_botoes.winfo_children():
            widget.destroy()
        
        label.configure(text="✨ VOCÊ É UM ARQUITETO! ✨", fg="#FFD700", font=("Arial", 14, "bold"))
        
        tk.Button(frame_botoes, text="PRÓXIMO PASSO: CRIAR O PADDLE ➡️", bg="#FF9800", fg="white", 
                  font=("Arial", 12, "bold"), pady=15,
                  command=lambda: carregar_missao_2(container, root, cor_escolhida)).pack(fill="x", pady=10)