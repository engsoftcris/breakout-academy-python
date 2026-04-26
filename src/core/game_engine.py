from .paddle import Paddle

class GameEngine:
    def __init__(self, canvas):
        self.canvas = canvas
        self.WIDTH = 400
        self.HEIGHT = 600
        
        # Criamos a raquete dentro do motor
        self.paddle = Paddle(self.canvas)
        
        # Ativamos os controles de teclado
        self.configurar_controles()

    def configurar_controles(self):
        # Dá foco ao canvas para ele capturar as teclas
        self.canvas.focus_set()
        # Vincula as setas esquerda e direita
        self.canvas.bind_all("<Left>", self.paddle.mover_esquerda)
        self.canvas.bind_all("<Right>", self.paddle.mover_direita)

    def configurar_mundo(self):
        print("Mundo configurado e Raquete pronta para o combate!")