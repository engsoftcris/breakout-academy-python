import pygame
import os

class SoundManager:
    def __init__(self):
        # Inicializa o mixer do pygame
        pygame.mixer.init()
        
        self.base_path = os.path.join("assets", "sounds")
        
        # Agora usando os nomes padronizados
        self.bounce_path = os.path.join(self.base_path, "bounce.wav")
        self.paddle_path = os.path.join(self.base_path, "paddle_hit.wav")
        
        try:
            self.bounce_sound = pygame.mixer.Sound(self.bounce_path)
            self.paddle_sound = pygame.mixer.Sound(self.paddle_path)
        except Exception as e:
            print(f"Aviso: Arquivos de som não encontrados. Verifique a pasta assets/sounds/")
            self.bounce_sound = None
            self.paddle_sound = None

    def play_bounce(self):
        if self.bounce_sound:
            self.bounce_sound.play()

    def play_paddle(self):
        if self.paddle_sound:
            self.paddle_sound.play()