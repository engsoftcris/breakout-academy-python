class Ball:
    # O "RG" da bola: ela precisa conhecer o campo, a raquete, os sons, os blocos e o juiz (engine)
    def __init__(self, canvas, paddle, sound_manager, bricks, engine):
        self.canvas = canvas
        self.paddle = paddle
        self.sound_manager = sound_manager 
        self.bricks = bricks
        self.engine = engine # O motor do jogo que cuida das vidas e pontos
        
        # Criamos a nossa bolinha verde redondinha (create_oval)
        self.id = canvas.create_oval(10, 10, 25, 25, fill="green")
        
        # Colocamos ela no meio do campo para começar
        self.canvas.move(self.id, 190, 250)
        
        # A velocidade dela: x é para os lados, y é para cima e para baixo
        self.x = 3
        self.y = -3
        
    def desenhar(self):
        # 1. FAZENDO A BOLA SE MEXER
        self.canvas.move(self.id, self.x, self.y)
        
        # Perguntamos ao computador: "Onde a bolinha está agora?"
        pos = self.canvas.coords(self.id)
        
        # Verificamos se ela bateu em algum bloco de tijolo
        self.checar_colisao_blocos(pos)
        
        # 2. BATENDO NAS PAREDES (BOUNCE)
        # pos[0] = esquerda, pos[2] = direita, pos[1] = topo
        if pos[0] <= 0 or pos[2] >= 400 or pos[1] <= 0:
            self.sound_manager.play_bounce() # Toca o som de batida na parede
            
            # Se bater na esquerda, ela volta para a direita
            if pos[0] <= 0: self.x = 3
            # Se bater na direita, ela volta para a esquerda
            if pos[2] >= 400: self.x = -3
            # Se bater no teto, ela começa a cair
            if pos[1] <= 0: self.y = 3

        # 3. BATENDO NA RAQUETE
        if self.bater_na_raquete(pos):
            self.y = -3 # Manda a bola para cima de novo
            self.sound_manager.play_paddle() # Toca o som de batida na raquete

        # 4. O PERIGO: TOCOU O CHÃO!
        # pos[3] é a parte de baixo da bolinha. O chão fica em 600.
        if pos[3] >= 600:
            self.y = -3 # Prepara ela para subir no próximo reinício
            print("A bola tocou o chão!")
            
            # Avisamos ao juiz (engine) para tirar uma vida do jogador
            self.engine.reduzir_vida() 
            
            # Teletransportamos a bola de volta para o centro para recomeçar
            self.canvas.coords(self.id, 190, 250, 205, 265)
    
    def bater_na_raquete(self, pos_bola):
        # Descobrimos onde a raquete está no momento
        pos_raquete = self.canvas.coords(self.paddle.id)
        
        # Verificamos se a posição da bola "cruza" com a posição da raquete
        if pos_bola[2] >= pos_raquete[0] and pos_bola[0] <= pos_raquete[2]:
            if pos_bola[3] >= pos_raquete[1] and pos_bola[3] <= pos_raquete[3]:
                return True # Sim, ela bateu!
        return False # Não, ela errou.
    
    def checar_colisao_blocos(self, pos_bola):
        # Olhamos cada bloco dentro da nossa lista de blocos
        for bloco in self.bricks:
            # Só conferimos os blocos que ainda não foram quebrados (ativos)
            if bloco.active:
                pos_bloco = self.canvas.coords(bloco.id)
                
                # Se o bloco por algum motivo sumiu, pulamos para o próximo
                if not pos_bloco:
                    continue
                
                # MATEMÁTICA DA COLISÃO: A bola entrou no espaço do retângulo do bloco?
                if (pos_bola[2] >= pos_bloco[0] and pos_bola[0] <= pos_bloco[2] and
                    pos_bola[3] >= pos_bloco[1] and pos_bola[1] <= pos_bloco[3]):
                    
                    bloco.destruir()    # O bloco "some" da tela
                    self.y *= -1        # A bola rebate e muda de direção (sobe vira desce, desce vira sobe)
                    self.sound_manager.play_block() # Toca o som de explosão do bloco
                    self.engine.adicionar_pontos() # Avisa o juiz para dar pontos ao jogador
                    self.engine.verificar_vitoria() # Pergunta se esse era o último bloco
                    
                    return # Para a função aqui porque já bateu em um bloco