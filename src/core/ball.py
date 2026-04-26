class Ball:
    def __init__(self, canvas, paddle):
        self.canvas = canvas
        self.paddle = paddle
        # Cria a bola (um círculo)
        # Coordenadas: x1, y1, x2, y2
        self.id = canvas.create_oval(10, 10, 25, 25, fill="red")
        
        # Define a posição inicial (meio da tela)
        self.canvas.move(self.id, 190, 250)
        
        # Velocidade inicial
        self.x = 3
        self.y = -3
        
    def desenhar(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        
        # Quicar no topo
        if pos[1] <= 0:
            self.y = 3
            
        # Quicar no fundo (por enquanto, para não perdermos a bola)
        if pos[3] >= 600:
            self.y = -3
            
        # Quicar nas laterais
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= 400:
            self.x = -3
        # Colisão com a Raquete
        if self.bater_na_raquete(pos):
            self.y = -3 # Manda a bola para cima
    
    def bater_na_raquete(self, pos_bola):
        pos_raquete = self.canvas.coords(self.paddle.id)
        # Verifica se a bola está dentro da área horizontal e vertical da raquete
        if pos_bola[2] >= pos_raquete[0] and pos_bola[0] <= pos_raquete[2]:
            if pos_bola[3] >= pos_raquete[1] and pos_bola[3] <= pos_raquete[3]:
                return True
        return False