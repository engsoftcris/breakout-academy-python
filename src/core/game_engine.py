from .paddle import Paddle
from .ball import Ball
from .sound_manager import SoundManager

class GameEngine:
    def __init__(self, canvas):
        self.canvas = canvas
        self.WIDTH = 400
        self.HEIGHT = 600

        # Inicializa o gerenciador de som
        self.sound_manager = SoundManager()
        
        self.paddle = Paddle(self.canvas)
        # Criamos a bola passando o canvas e a raquete (para futuras colisões)
        self.ball = Ball(self.canvas, self.paddle, self.sound_manager)
        
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