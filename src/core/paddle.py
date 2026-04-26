class Paddle:
    def __init__(self, canvas):
        self.canvas = canvas
        # Desenha a raquete no Canvas
        # Coordenadas: x1, y1 (topo-esquerda), x2, y2 (baixo-direita)
        # Largura: 100px (250-150), Altura: 15px (565-550)
        self.id = canvas.create_rectangle(150, 550, 250, 565, fill="#00adb5")
        self.velocidade = 20

    def mover_esquerda(self, event):
        pos = self.canvas.coords(self.id)
        if pos[0] > 0: # Só move se não encostou na parede esquerda
            self.canvas.move(self.id, -self.velocidade, 0)

    def mover_direita(self, event):
        pos = self.canvas.coords(self.id)
        if pos[2] < 400: # Só move se não encostou na parede direita (WIDTH=400)
            self.canvas.move(self.id, self.velocidade, 0)