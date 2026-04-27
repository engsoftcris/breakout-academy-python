class Paddle:
    def __init__(self, canvas):
        self.canvas = canvas
        
        # 1. CRIANDO O NOSSO "ESCUDO" (A RAQUETE)
        # O comando create_rectangle desenha um retângulo.
        # Os números dizem onde ele começa e onde termina (x1, y1, x2, y2).
        # Escolhemos uma cor azul brilhante (#00adb5) para ela se destacar!
        self.id = canvas.create_rectangle(150, 550, 250, 565, fill="#00adb5")
        
        # Definimos que, toda vez que apertarmos uma tecla, ela vai pular 20 pixels
        self.velocidade = 20

    def mover_esquerda(self, event):
        # Primeiro, perguntamos ao computador: "Onde a raquete está agora?"
        pos = self.canvas.coords(self.id)
        
        # pos[0] é o lado esquerdo da raquete. 
        # Se ele for maior que 0, significa que ainda não bateu na parede da esquerda!
        if pos[0] > 0: 
            # Mandamos a raquete "dar um passo" para a esquerda (número negativo)
            self.canvas.move(self.id, -self.velocidade, 0)

    def mover_direita(self, event):
        # Perguntamos de novo: "Onde a raquete está?"
        pos = self.canvas.coords(self.id)
        
        # pos[2] é o lado direito da raquete.
        # Como nossa tela tem 400 pixels de largura, ela só pode andar se pos[2] for menor que 400.
        if pos[2] < 400: 
            # Mandamos a raquete "dar um passo" para a direita (número positivo)
            self.canvas.move(self.id, self.velocidade, 0)