import pygame

class SettingData:
    
    def __init__(self, rect: pygame.Rect, safe, input,  text: str, input_type: str, upper_limit: int = 0, lower_limit: int = 0):
        self.rect: pygame.Rect = rect
        self.input = input
        self.safe = safe
        self.text: str = text
        self.input_type = input_type
        self.upper_limit: int = upper_limit
        self.lower_limit: int = lower_limit
        
    def __str__(self) -> str:
        return f"rect: {self.rect}, safe: {self.safe}, input: {self.input}, text: {self.text}, input_type: {self.input_type}"