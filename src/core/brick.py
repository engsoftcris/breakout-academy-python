class Brick:
    # O "Nascimento" do bloco: ele precisa saber onde vai morar (x1, y1, x2, y2) e qual sua cor
    def __init__(self, canvas, x1, y1, x2, y2, color):
        self.canvas = canvas
        
        # 1. CONSTRUINDO O TIJOLO
        # Desenhamos o retângulo com a cor que o motor (engine) escolheu.
        # Guardamos o "RG" dele no self.id para podermos escondê-lo depois.
        self.id = canvas.create_rectangle(
            x1, y1, x2, y2, 
            fill=color, 
            outline=color  # Usamos a mesma cor na borda para ficar um bloco sólido e bonito
        )
        
        # O bloco começa o jogo "Vivo" (True)
        self.active = True

    def destruir(self):
        # 2. O BLOCO FOI ATINGIDO!
        # Em vez de jogar o bloco no lixo (delete), nós apenas dizemos que ele não vale mais
        self.active = False
        
        # MÁGICA: O comando state='hidden' faz o bloco ficar invisível!
        # Ele ainda existe lá no código, mas o jogador não o vê e a bola não bate mais nele.
        # Isso é ótimo porque, se quisermos reiniciar o jogo, é só "desesconder".
        self.canvas.itemconfig(self.id, state='hidden')