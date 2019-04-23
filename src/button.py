import pyglet
import draw


class Button:
    def __init__(self, x, y, text, size, color=(255, 255, 255, 255), bold=False, bigger=False, secondary_color=(0, 0, 0, 255), image=None):
        self.x = x
        self.y = y
        self.text = text
        self.size = size
        self.color = color
        self.bold = bold
        self.bigger = bigger
        self.secondary_color = secondary_color
        self.image = image
        self.button_text = pyglet.text.Label(self.text, font_name="Calibri", font_size=self.size,
                                             x=self.x+2, y=self.y+3, color=self.color, bold=self.bold)
        self.width = self.button_text.content_width
        self.height = self.button_text.content_height // 2 + 8
        self.highlight = False

    def render(self, text: bool=True):
        if self.highlight:
            draw.rect(self.x, self.y, self.width + (4 if self.image is None else 0), self.height, self.secondary_color)
        else:
            pass
        if text:
            self.show_text()
        if self.image is not None:
            self.image.blit(self.x, self.y)

    def show_text(self):
        self.button_text.draw()

    def pressed(self, x, y) -> bool:
        if self.x + self.width >= x >= self.x:
            if self.y + self.height - (5 if self.bigger else 0) >= y >= self.y - (5 if self.bigger else 0):
                self.highlight = True
                return True
        self.highlight = False
        return False
