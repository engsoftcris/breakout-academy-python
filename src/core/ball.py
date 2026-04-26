class Ball:
    # Ajustado para receber o 'engine' no final
    def __init__(self, canvas, paddle, sound_manager, bricks, engine):
        self.canvas = canvas
        self.paddle = paddle
        self.sound_manager = sound_manager 
        self.bricks = bricks
        self.engine = engine 
        
        self.id = canvas.create_oval(10, 10, 25, 25, fill="green")
        self.canvas.move(self.id, 190, 250)
        self.x = 3
        self.y = -3
        
    def desenhar(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        self.checar_colisao_blocos(pos)
        
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

        # 3. Lógica do Fundo (O "Chão") - AQUI ACRESCENTAMOS A PERDA DE VIDA
        if pos[3] >= 600:
            self.y = -3
            print("A bola tocou o chão!")
            # Acrescentado: avisa o engine para reduzir a vida
            self.engine.reduzir_vida() 
            # Acrescentado: reposiciona a bola para não perder todas as vidas de uma vez
            self.canvas.coords(self.id, 190, 250, 205, 265)
    
    def bater_na_raquete(self, pos_bola):
        pos_raquete = self.canvas.coords(self.paddle.id)
        if pos_bola[2] >= pos_raquete[0] and pos_bola[0] <= pos_raquete[2]:
            if pos_bola[3] >= pos_raquete[1] and pos_bola[3] <= pos_raquete[3]:
                return True
        return False
    
    def checar_colisao_blocos(self, pos_bola):
        for bloco in self.bricks:
            if bloco.active:
                pos_bloco = self.canvas.coords(bloco.id)
                
                if (pos_bola[2] >= pos_bloco[0] and pos_bola[0] <= pos_bloco[2] and
                    pos_bola[3] >= pos_bloco[1] and pos_bola[1] <= pos_bloco[3]):
                    
                    bloco.destruir()    
                    self.y *= -1        
                    self.sound_manager.play_block() 
                    
                    # 1. Soma os pontos
                    self.engine.adicionar_pontos() 
                    
                    # 2. ACRESCENTADO: Verifica se era o último bloco
                    self.engine.verificar_vitoria() 
                    
                    return