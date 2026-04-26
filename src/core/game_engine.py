import tkinter as tk

class GameEngine:
    def __init__(self, canvas):
        self.canvas = canvas
        self.WIDTH = 400
        self.HEIGHT = 600
        
    def configurar_mundo(self):
        # Por enquanto apenas confirma que o motor iniciou
        print("Motor do jogo iniciado...")