from .paddle import Paddle
from .ball import Ball
from .sound_manager import SoundManager
from .brick import Brick

class GameEngine:
    def __init__(self, canvas):
        self.canvas = canvas
        self.WIDTH = 400
        self.HEIGHT = 600

        # Inicializa o gerenciador de som
        self.sound_manager = SoundManager()
        self.bricks = []
        self.paddle = Paddle(self.canvas)
        # Criamos a bola passando o canvas e a raquete (para futuras colisões)
        self.ball = Ball(self.canvas, self.paddle, self.sound_manager, self.bricks)
       
        self.criar_grade_de_blocos()
        
        self.configurar_controles()
        # Iniciamos o ciclo de animação
        self.atualizar()

    def configurar_controles(self):
        self.canvas.focus_set()
        self.canvas.bind_all("<Left>", self.paddle.mover_esquerda)
        self.canvas.bind_all("<Right>", self.paddle.mover_direita)

    def atualizar(self):
        # Move a bola
        self.ball.desenhar()
        
        # Agenda a próxima atualização (aprox. 60 FPS)
        # 16 milissegundos é o tempo ideal para um movimento fluido
        self.canvas.after(16, self.atualizar)

    def configurar_mundo(self):
        print("Bola em jogo!")

    def criar_grade_de_blocos(self):
        cores = ["#FF5722", "#FFC107", "#4CAF50", "#2196F3"] # Cores vibrantes
        for linha in range(4): # 4 fileiras
            for coluna in range(6): # 6 blocos por fileira
                # Cálculo de posicionamento:
                x1 = coluna * 65 + 5 # largura de 60px + 5px de margem
                y1 = linha * 25 + 50 # altura de 20px + 5px de margem, começando 50px do topo
                x2 = x1 + 60
                y2 = y1 + 20
                
                bloco = Brick(self.canvas, x1, y1, x2, y2, cores[linha])
                self.bricks.append(bloco)