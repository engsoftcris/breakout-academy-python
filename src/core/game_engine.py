from .paddle import Paddle
from .ball import Ball
from .sound_manager import SoundManager
from .brick import Brick

class GameEngine:
    def __init__(self, canvas):
        self.canvas = canvas
        self.WIDTH = 400
        self.HEIGHT = 600

        # --- NOVOS ATRIBUTOS ---
        self.score = 0
        self.lives = 3
        
        # Elementos visuais (HUD)
        self.score_text = self.canvas.create_text(
            50, 20, text=f"Pontos: {self.score}", fill="white", font=("Arial", 12, "bold")
        )
        self.lives_text = self.canvas.create_text(
            350, 20, text=f"Vidas: {self.lives}", fill="white", font=("Arial", 12, "bold")
        )
        # -----------------------

        self.sound_manager = SoundManager()
        self.bricks = []
        
        # Primeiro criamos a grade para a lista bricks não estar vazia
        self.criar_grade_de_blocos()
        
        self.paddle = Paddle(self.canvas)
        
        # Agora passamos 'self' (o próprio engine) para a bola avisar sobre pontos/vidas
        self.ball = Ball(self.canvas, self.paddle, self.sound_manager, self.bricks, self)
       
        self.configurar_controles()
        self.atualizar()

    # --- NOVOS MÉTODOS DE CONTROLE ---
    def adicionar_pontos(self):
        self.score += 10
        self.canvas.itemconfig(self.score_text, text=f"Pontos: {self.score}")

    def reduzir_vida(self):
        self.lives -= 1
        self.canvas.itemconfig(self.lives_text, text=f"Vidas: {self.lives}")
        if self.lives <= 0:
            self.finalizar_jogo()

    def finalizar_jogo(self):
        self.canvas.create_text(
            200, 300, text="GAME OVER", fill="red", font=("Arial", 25, "bold")
        )
        self.ball.x = 0
        self.ball.y = 0
    # --------------------------------

    def configurar_controles(self):
        self.canvas.focus_set()
        self.canvas.bind_all("<Left>", self.paddle.mover_esquerda)
        self.canvas.bind_all("<Right>", self.paddle.mover_direita)

    def atualizar(self):
        self.ball.desenhar()
        self.canvas.after(16, self.atualizar)

    def configurar_mundo(self):
        print("Bola em jogo!")

    def criar_grade_de_blocos(self):
        # Aqui usei as suas 10 colunas que você mencionou anteriormente
        cores = ["#FF5722", "#FFC107", "#4CAF50", "#2196F3"]
        for linha in range(4):
            for coluna in range(10): # Ajustado para 10 como você preferiu
                x1 = coluna * 40
                y1 = linha * 25 + 50
                x2 = x1 + 38
                y2 = y1 + 20
                bloco = Brick(self.canvas, x1, y1, x2, y2, cores[linha])
                self.bricks.append(bloco)

    def verificar_vitoria(self):
        # O any() verifica se existe pelo menos UM bloco ativo
        blocos_restantes = any(bloco.active for bloco in self.bricks)
        
        if not blocos_restantes:
            self.vencer_jogo()

    def vencer_jogo(self):
        # 1. Criar a mensagem de vitória bem no centro
        self.canvas.create_text(
            200, 300, text="VOCÊ VENCEU!", fill="#4CAF50", font=("Arial", 30, "bold")
        )
        
        # 2. Reposicionar a bola no "centro de descanso"
        # Isso evita que ela fique flutuando em cima de onde ficavam os blocos
        self.canvas.coords(self.ball.id, 190, 350, 205, 365)
        
        # 3. Parar o movimento
        self.ball.x = 0
        self.ball.y = 0