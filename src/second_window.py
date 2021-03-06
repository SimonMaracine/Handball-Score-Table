import pyglet
from pyglet.window import key

import src.table as table
import src.config as config
from src.config import WIDTH, HEIGHT, icon1, icon2, background

second_window = None


def start():
    global second_window
    second_window = pyglet.window.Window(WIDTH, HEIGHT, "Handball Score Table [2]", vsync=True, visible=False)

    @second_window.event
    def on_draw():
        second_window.clear()
        background.blit(0, 0)
        table.tab.team1.render()
        table.tab.team2.render()
        table.tab.show_timers()
        table.tab.show_round()
        table.Table.show_players(table.tab.get_players("left"), False)
        table.Table.show_players(table.tab.get_players("right"), False)
        table.Table.show_suspended_players(table.tab.get_players("left"))
        table.Table.show_suspended_players(table.tab.get_players("right"))

    @second_window.event
    def on_key_release(symbol, modifiers):
        global fullscreen
        if symbol == key.F:
            if len(monitors) >= 2:
                if not fullscreen:
                    second_window.set_fullscreen(True, monitors[1], width=WIDTH, height=HEIGHT)
                    fullscreen = True
                else:
                    second_window.set_fullscreen(False, monitors[1], width=WIDTH, height=HEIGHT)
                    fullscreen = False

    @second_window.event
    def on_close():
        config.num_second_windows -= 1

    display = pyglet.window.get_platform().get_default_display()
    monitors = display.get_screens()

    second_window.set_icon(icon1, icon2)
    if len(monitors) >= 2:
        second_window.set_location(monitors[0].width + monitors[1].width // 2 - second_window.width // 2, 200)
        # second_window.set_fullscreen(True, monitors[1], width=WIDTH, height=HEIGHT)
    second_window.set_visible(True)

    fullscreen = False
    config.num_second_windows += 1
