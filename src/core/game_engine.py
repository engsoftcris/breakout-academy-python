# Importamos as outras peças do nosso brinquedo: a Raquete, a Bola, os Sons e os Blocos
from .paddle import Paddle
from .ball import Ball
from .sound_manager import SoundManager
from .brick import Brick

class GameEngine:
    def __init__(self, canvas):
        self.canvas = canvas
        # Definimos o tamanho do nosso campo de jogo (400 de largura por 600 de altura)
        self.WIDTH = 400
        self.HEIGHT = 600
        # O jogo começa "Dormindo" (False), esperando o jogador apertar Espaço
        self.jogando = False  
        
        # Criamos o letreiro principal que dá instruções ao jogador no meio da tela
        self.tela_mensagem = self.canvas.create_text(
            200, 300, 
            text="Pressione ESPAÇO para Iniciar", 
            fill="white", 
            font=("Arial", 16, "bold")
        )

        # --- NOSSO PLACAR (HUD) ---
        self.score = 0  # Começamos com zero pontos
        self.lives = 3  # O jogador ganha 3 chances (vidas)
        
        # Desenhamos o texto dos Pontos lá no cantinho esquerdo (50, 20)
        self.score_text = self.canvas.create_text(
            50, 20, text=f"Pontos: {self.score}", fill="white", font=("Arial", 12, "bold")
        )
        # Desenhamos o texto das Vidas lá no cantinho direito (350, 20)
        self.lives_text = self.canvas.create_text(
            350, 20, text=f"Vidas: {self.lives}", fill="white", font=("Arial", 12, "bold")
        )
        # -----------------------

        # Ligamos a caixinha de som do jogo
        self.sound_manager = SoundManager()
        # Criamos uma mochila (lista) vazia para guardar os blocos
        self.bricks = []
        
        # Chamamos o mestre de obras para construir a parede de tijolos
        self.criar_grade_de_blocos()
        
        # Colocamos a Raquete (Paddle) no campo
        self.paddle = Paddle(self.canvas)
        
        # Colocamos a Bola e damos a ela o mapa de onde estão a raquete, os sons e os blocos
        # Também passamos "self" para a bola poder avisar ao motor quando ganhar pontos
        self.ball = Ball(self.canvas, self.paddle, self.sound_manager, self.bricks, self)
       
        # Preparamos o teclado para obedecer aos nossos comandos
        self.configurar_controles()
        # Ligamos o coração do jogo para ele começar a bater (atualizar)
        self.atualizar()

    # --- FUNÇÕES PARA CUIDAR DOS PONTOS E VIDAS ---
    
    def adicionar_pontos(self):
        # Ganhou 10 pontos! Aumentamos o número e atualizamos o texto na tela
        self.score += 10
        self.canvas.itemconfig(self.score_text, text=f"Pontos: {self.score}")

    def reduzir_vida(self):
        # Que pena! A bola caiu. Tiramos uma vida e atualizamos na tela
        self.lives -= 1
        self.canvas.itemconfig(self.lives_text, text=f"Vidas: {self.lives}")
        # Se as vidas chegarem a zero, o Juiz apita o fim do jogo
        if self.lives <= 0:
            self.finalizar_jogo()

    def finalizar_jogo(self):
        # O jogo para de rodar e mostra a mensagem de derrota em vermelho
        self.jogando = False
        self.canvas.itemconfig(
            self.tela_mensagem, 
            text="GAME OVER\n\nAperte ESPAÇO para reiniciar", 
            fill="red"
        )
        # Fazemos a bola parar de se mexer
        self.ball.x = 0
        self.ball.y = 0
    # --------------------------------

    def configurar_controles(self):
        # Dizemos para a janela prestar atenção nas teclas que vamos apertar
        self.canvas.focus_set()
        # Seta para Esquerda, Direta e a tecla Espaço
        self.canvas.bind_all("<Left>", self.paddle.mover_esquerda)
        self.canvas.bind_all("<Right>", self.paddle.mover_direita)
        self.canvas.bind_all("<space>", self.alternar_estado)

    def atualizar(self):
        # Se o jogo estiver valendo (True), mandamos a bola se desenhar/mover
        if self.jogando:
            self.ball.desenhar()
        
        # O relógio do jogo: ele espera 16 milissegundos e chama essa função de novo (60 vezes por segundo!)
        self.canvas.after(16, self.atualizar)

    def configurar_mundo(self):
        # Um aviso no terminal só para sabermos que tudo começou bem
        print("Bola em jogo!")

    def criar_grade_de_blocos(self):
        # Definimos as cores das linhas de blocos
        cores = ["#FF5722", "#FFC107", "#4CAF50", "#2196F3"]
        largura_bloco = 60  
        espacamento = 6   
        margem_esquerda = 5 
        
        # Criamos 4 linhas de blocos
        for linha in range(4):
            # Em cada linha, colocamos 6 blocos um do lado do outro
            for coluna in range(6):
                # Calculamos onde cada bloco vai ficar para não ficarem um em cima do outro
                x1 = (coluna * (largura_bloco + espacamento)) + margem_esquerda
                y1 = linha * 30 + 50 
                
                x2 = x1 + largura_bloco
                y2 = y1 + 20
                
                # Criamos o bloco e guardamos na nossa lista "mochila"
                bloco = Brick(self.canvas, x1, y1, x2, y2, cores[linha])
                self.bricks.append(bloco)

    def verificar_vitoria(self):
        # Perguntamos: "Ainda tem algum bloco sobrando?"
        blocos_restantes = any(bloco.active for bloco in self.bricks)
        
        # Se não tiver mais nenhum bloco, o jogador venceu!
        if not blocos_restantes:
            self.vencer_jogo()

    def vencer_jogo(self):
        # Para o jogo e mostra a mensagem de vitória em Verde Neon
        self.jogando = False
        self.canvas.itemconfig(
            self.tela_mensagem, 
            text="VOCÊ VENCEU!\n\nAperte ESPAÇO para reiniciar", 
            fill="#00FF00" 
        )
        # Guardamos a bola num lugar seguro no centro
        self.canvas.coords(self.ball.id, 190, 350, 205, 365)
        self.ball.x = 0
        self.ball.y = 0

    def alternar_estado(self, event):
        # Esta função decide o que acontece quando apertamos ESPAÇO
        
        # 1. Se o jogo já acabou, o Espaço serve para REINICIAR tudo do zero
        blocos_ativos = any(bloco.active for bloco in self.bricks)
        if self.lives <= 0 or not blocos_ativos:
            self.reiniciar_jogo_completo()
            return

        # 2. Se o jogo estava parado no início, o Espaço serve para dar o START
        if not self.jogando:
            self.jogando = True
            # Limpa o texto da tela para podermos ver o jogo
            self.canvas.itemconfig(self.tela_mensagem, text="")

    def reiniciar_jogo_completo(self):
        # Resetamos os pontos e as vidas como se fosse um novo dia
        self.score = 0
        self.lives = 3
        self.canvas.itemconfig(self.score_text, text=f"Points: {self.score}")
        self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.lives}")
        
        # Fazemos todos os blocos "nascerem" de novo e ficarem visíveis
        for bloco in self.bricks:
            bloco.active = True
            self.canvas.itemconfig(bloco.id, state='normal')
            
        # Apagamos as mensagens e colocamos a bola na posição inicial de lançamento
        self.canvas.itemconfig(self.tela_mensagem, text="", fill="white")
        self.ball.x = 3
        self.ball.y = -3
        self.canvas.coords(self.ball.id, 190, 250, 205, 265)
        # E o jogo começa a rodar imediatamente!
        self.jogando = True