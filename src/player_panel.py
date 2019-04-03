from button import Button
import draw


class PlayerPanel:
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.player = player
        self.suspend_button = Button(x + 15, y + 30, "Suspend player", 16, (255, 16, 16, 255), True)
        self.release_button = Button(x + 15, y + 30 - 25, "Release player", 16, (255, 16, 16, 255), True)
        self.width = 160
        self.height = 50

    def render(self):
        draw.rect(self.x + 14, self.y, self.width, self.height)
        self.suspend_button.render()
        self.release_button.render()

    def update(self, x, y):
        if self.suspend_button.pressed(x, y):
            self.player.suspend()
        elif self.release_button.pressed(x, y):
            self.player.release()
