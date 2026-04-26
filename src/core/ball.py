class Ball:
    def __init__(self, canvas, paddle, sound_manager):
        self.canvas = canvas
        self.paddle = paddle
        self.sound_manager = sound_manager # Recebe o gerente de som
        self.id = canvas.create_oval(10, 10, 25, 25, fill="red")
        self.canvas.move(self.id, 190, 250)
        self.x = 3
        self.y = -3
        
    def desenhar(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        
        # 1. Colisão com laterais e topo (Bounce normal)
        if pos[0] <= 0 or pos[2] >= 400 or pos[1] <= 0:
            self.sound_manager.play_bounce()
            if pos[0] <= 0: self.x = 3
            if pos[2] >= 400: self.x = -3
            if pos[1] <= 0: self.y = 3

        # 2. Colisão com a raquete (Paddle Hit)
        if self.bater_na_raquete(pos):
            self.y = -3
            self.sound_manager.play_paddle()

        # 3. Lógica do Fundo (O "Chão")
        if pos[3] >= 600:
            # PARA O TUTORIAL: Vamos fazer ela quicar, mas poderíamos disparar um som de erro
            self.y = -3
            # self.sound_manager.play_fail() # Futuro som de vida perdida
            print("A bola tocou o chão!")
    
    def bater_na_raquete(self, pos_bola):
        pos_raquete = self.canvas.coords(self.paddle.id)
        # Verifica se a bola está dentro da área horizontal e vertical da raquete
        if pos_bola[2] >= pos_raquete[0] and pos_bola[0] <= pos_raquete[2]:
            if pos_bola[3] >= pos_raquete[1] and pos_bola[3] <= pos_raquete[3]:
                return True
        return False