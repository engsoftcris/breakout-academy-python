class Brick:
    def __init__(self, canvas, x1, y1, x2, y2, color):
        self.canvas = canvas
        # Desenha o retângulo do bloco
        self.id = canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="white")
        self.active = True

    def destruir(self):
        # Remove o desenho do canvas e marca como inativo
        self.canvas.delete(self.id)
        self.active = False