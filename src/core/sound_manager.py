import pygame
import os

class SoundManager:
    def __init__(self):
        # Inicializa o mixer do pygame
        pygame.mixer.init()
        
        self.base_path = os.path.join("assets", "sounds")
        
        self.bounce_path = os.path.join(self.base_path, "bounce.wav")
        self.paddle_path = os.path.join(self.base_path, "paddle_hit.wav")
        self.block_path = os.path.join(self.base_path, "block_hit.wav") # Adicionado
        
        try:
            self.bounce_sound = pygame.mixer.Sound(self.bounce_path)
            self.paddle_sound = pygame.mixer.Sound(self.paddle_path)
            self.block_sound = pygame.mixer.Sound(self.block_path) # Adicionado
        except Exception as e:
            print(f"Aviso: Arquivos de som não encontrados. Verifique a pasta assets/sounds/")
            self.bounce_sound = None
            self.paddle_sound = None
            self.block_sound = None # Adicionado

    def play_bounce(self):
        if self.bounce_sound:
            self.bounce_sound.play()

    def play_paddle(self):
        if self.paddle_sound:
            self.paddle_sound.play()

    # Novo método seguindo EXATAMENTE o seu padrão
    def play_block(self):
        if self.block_sound:
            self.block_sound.play()