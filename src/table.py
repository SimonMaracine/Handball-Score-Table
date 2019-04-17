import pyglet

import countdown
import team
from player import Player
from button import Button
from player_panel import PlayerPanel

WIDTH = 800
HEIGHT = 600


class Table:
    def __init__(self):
        self.timer = countdown.Timer(WIDTH // 2 - 92, HEIGHT // 2 + 180, 60, 60 * 20)  # main timer
        self.time_out_timer = None  # time-out timer
        self.game_round = 1
        self.round_text = pyglet.text.Label(str(self.game_round), font_name="Calibri", font_size=90, x=334, y=304)
        self.player_panel = None

        self.players1 = [Player("Simon", 1, "left"), Player("Teodor", 2, "left"), Player("player3", 3, "left")]
        self.players2 = [Player("player1", 4, "right"), Player("player2", 5, "right"), Player("player3", 6, "right"),
                         Player("player4", 7, "right")]
        self.team1 = team.Team("Home", self.players1, 30, HEIGHT - 130, 110, 362)
        self.team2 = team.Team("Guest", self.players2, 565, HEIGHT - 130, 590, 362)

        self.button1 = Button(360, 60, "first button", 14)
        self.buttons = ()
        self.init_player_buttons()

    def update(self, dt):
        if self.time_out_timer is not None and self.time_out_timer.finished:
            self.time_out_timer = None
            self.timer.start()
            __class__.update_players_timers("start", self.get_players())
        if self.timer.finished:
            __class__.update_players_timers("release", self.get_players())
        self.team1.update()
        self.team2.update()

    def show_round(self):
        self.round_text.text = str(self.game_round)
        self.round_text.draw()

    @staticmethod
    def show_players(players):
        for i, player in enumerate(players):
            player.render((-i + 13) * 23)

    @staticmethod
    def show_suspended_players(players):
        suspended_players = list(filter(lambda player: player.suspended, players))
        for i, player in enumerate(suspended_players):
            player.render_suspended((-len(suspended_players) + i + 12) * 23)

    def show_buttons(self):
        for button in self.buttons:
            button.render()

    def show_timers(self):
        if self.time_out_timer is None:
            self.timer.render()
        if self.time_out_timer is not None:
            self.time_out_timer.render()

    def get_players(self, mode="all") -> list:  # Returns all players.
        if mode == "all":
            players = self.players1 + self.players2
        elif mode == "left":
            players = self.players1
        elif mode == "right":
            players = self.players2
        else:
            players = list(filter(lambda player: not player.disqualified, self.players1 + self.players2))
        return players

    def update_player_functionality(self, x, y):
        players = self.get_players("remained")
        player_buttons = list(map(lambda player: player.get_button(), players))

        if self.player_panel is not None:
            if self.player_panel.update(x, y, self.timer):
                return  # to not check for other buttons bellow the panel

        for i, btn in enumerate(player_buttons):
            if btn.pressed(x, y):
                # print("player {}".format(i + 1))
                if players[i].select() == "selected":  # select the clicked player
                    self.player_panel = PlayerPanel(x, y, players[i], (self.team1, self.team2))
                    if len(list(filter(lambda player: player.selected, players))) == 2:
                        Player.de_select(players, i)  # de-select previous clicked player
                else:
                    self.player_panel = None
                break
        else:
            Player.de_select(players)
            self.player_panel = None

    def init_player_buttons(self):
        for i, player in enumerate(self.get_players("left")):
            player.update_button(32, (-i + 13) * 23)
        for i, player in enumerate(self.get_players("right")):
            player.update_button(WIDTH - 238, (-i + 13) * 23)

    @staticmethod
    def update_players_timers(func: str, players):
        suspended_players = filter(lambda player: player.suspended, players)
        if func == "start":
            for player_timer in map(lambda player: player.suspend_timer, suspended_players):
                player_timer.start()
        elif func == "pause":
            for player_timer in map(lambda player: player.suspend_timer, suspended_players):
                player_timer.pause()
        else:
            for player in suspended_players:
                player.release()

    def advance_round(self, x: int):
        if x == -1 and self.game_round <= 1:
            return
        self.game_round += x


table = Table()