import pygame  # Importa a biblioteca que sabe tocar música e sons
import os      # Importa o "GPS" do computador para acharmos as pastas de arquivos

class SoundManager:
    def __init__(self):
        # 1. LIGANDO O SOM
        # Inicializa o mixer, que é como se fosse a mesa de som de um DJ
        pygame.mixer.init()
        
        # 2. ENCONTRANDO A PASTA DOS SONS
        # Criamos o caminho até a pasta "assets/sounds" onde os arquivos .wav estão guardados
        self.base_path = os.path.join("assets", "sounds")
        
        # Criamos o endereço completo de cada som (como se fosse o nome da rua e o número da casa)
        self.bounce_path = os.path.join(self.base_path, "bounce.wav")      # Som das paredes
        self.paddle_path = os.path.join(self.base_path, "paddle_hit.wav")  # Som da raquete
        self.block_path = os.path.join(self.base_path, "block_hit.wav")    # Som do bloco quebrando
        
        try:
            # 3. CARREGANDO OS SONS NA MEMÓRIA
            # Tentamos colocar os sons dentro das variáveis para eles ficarem prontos para tocar
            self.bounce_sound = pygame.mixer.Sound(self.bounce_path)
            self.paddle_sound = pygame.mixer.Sound(self.paddle_path)
            self.block_sound = pygame.mixer.Sound(self.block_path)
        except Exception as e:
            # Se a gente esqueceu de colocar o arquivo na pasta, o jogo avisa aqui no terminal
            print(f"Aviso: Arquivos de som não encontrados. Verifique a pasta assets/sounds/")
            self.bounce_sound = None
            self.paddle_sound = None
            self.block_sound = None 

    # 4. FUNÇÕES PARA DAR O "PLAY"
    
    def play_bounce(self):
        # Se o som existir, toca o barulhinho de batida na parede (Boing!)
        if self.bounce_sound:
            self.bounce_sound.play()

    def play_paddle(self):
        # Toca o som quando a bola encosta na raquete do jogador
        if self.paddle_sound:
            self.paddle_sound.play()

    def play_block(self):
        # Toca o som de "CRASH!" quando o bloco é destruído
        if self.block_sound:
            self.block_sound.play()