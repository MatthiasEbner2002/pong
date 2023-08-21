import pygame


class SettingData:

    def __init__(
        self, rect: pygame.Rect, safe, input, text: str,
        input_type: str, upper_limit: int = 0, lower_limit: int = 0
    ):
        self.rect: pygame.Rect = rect
        self.input = input
        self.safe = safe
        self.text: str = text
        self.input_type = input_type
        self.upper_limit: int = upper_limit
        self.lower_limit: int = lower_limit

    def __str__(self) -> str:
        ret: str = ''
        ret += f"rect: {self.rect},"
        ret += f"safe: {self.safe},"
        ret += f"input: {self.input},"
        ret += f"text: {self.text},"
        ret += f"input_type: {self.input_type}"
        return ret
