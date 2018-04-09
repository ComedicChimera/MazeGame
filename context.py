from input import Key
import os
import time
from game import MazeGame
import input


class TextContext:
    def __init__(self, on_close=None, on_switch=None):
        self.close_handler = on_close
        self.switch_handler = on_switch

    @staticmethod
    def render(lines):
        """Print a set of lines with their elements delimited by \n"""

        print('\r' + '\n'.join(lines), end='')

    @staticmethod
    def clear():
        """Clear the stdout"""

        os.system('cls' if os.name == 'nt' else 'clear')

    def update(self, key_state=None, key_str=''):
        pass

    def close(self):
        """Close the text context"""

        self.clear()
        if self.close_handler:
            self.close_handler()

    def switch(self, new_context, **kwargs):
        """Switch text contexts"""

        self.clear()
        if self.switch_handler:
            self.switch_handler(new_context, **kwargs)


class MenuContext(TextContext):
    def __init__(self, on_close=None, on_switch=None):
        super().__init__(on_close, on_switch)

        self.menu = {
            'Start': [True, lambda: self.switch(GameContext)],
            'How To Play': [False, lambda: self.switch(TutorialContext)],
            'Leaderboard': [False, lambda: self.switch(LeaderBoardContext)],
            'Exit': [False, self.close]
        }
        self.clear()

    def update(self, key_state=None, key_str=''):
        if key_state:
            if key_state == Key.RIGHT:
                self.slide(False)
            elif key_state == Key.LEFT:
                self.slide(True)
            elif key_state == Key.ENTER:
                for _, v in self.menu.items():
                    if v[0]:
                        v[1]()
        line = []
        for k, v in self.menu.items():
            if v[0]:
                line.append('[%s]' % k)
            else:
                line.append(' %s ' % k)
        self.render(['\t'.join(line)])

    def slide(self, reverse):
        men = reversed(list(self.menu.keys())) if reverse else self.menu
        set_next = False
        for k in men:
            if set_next:
                self.menu[k][0] = True
                set_next = False
            elif self.menu[k][0]:
                self.menu[k][0] = False
                set_next = True
        if set_next:
            self.menu['Exit' if reverse else 'Start'][0] = True


class GameContext(TextContext):
    def __init__(self, on_close=None, on_switch=None):
        super().__init__(on_close, on_switch)
        self._start_time = time.time()
        self.game = MazeGame()

    def update(self, key_state=None, key_str=''):
        if key_state:
            if key_state == Key.LEFT:
                self.game.shift_x(-1)
            elif key_state == Key.RIGHT:
                self.game.shift_x(1)
            elif key_state == Key.UP:
                self.game.shift_y(-1)
            elif key_state == Key.DOWN:
                self.game.shift_y(1)
            elif key_state == Key.ENTER:
                if self.game.check_door():
                    self.switch(SaveContext, score=self.game.score, time=time.time() - self._start_time)

        dif_time = time.time() - self._start_time
        l_time = time.localtime(dif_time)
        border_y = '  +%s+' % ('-' * self.game.fov[0])
        window = [border_y] + ['  |' + x + '|' for x in self.game.get_window()] + [border_y]
        self.render([time.strftime('%M:%S', l_time) + ' ' + 'Score: %d' % self.game.score] + [''] + window)
        time.sleep(0.02)
        self.clear()


class TutorialContext(TextContext):
    def __init__(self, on_close=None, on_switch=None):
        super().__init__(on_close, on_switch)
        self.rendered = False

    def update(self, key_state=None, key_str=''):
        if key_state:
            if key_state == Key.ENTER:
                self.switch(MenuContext)
        if not self.rendered:
            self.clear()
            with open('tutorial.txt', 'r', encoding='utf8') as file:
                self.render([file.read()])
            self.rendered = True


class SaveContext(TextContext):
    def __init__(self, on_close=None, on_switch=None, **kwargs):
        super().__init__(on_close, on_switch)
        self.score = kwargs['score']
        self.time = kwargs['time']
        self.menu = {
            'Save': [True, self._save],
            'Back to Menu': [False, lambda: self.switch(MenuContext)],
        }
        self._message = [
            'Congratulations! You won.',
            '',
            'Time: %s Score: %s' % (time.strftime('%M:%S', time.localtime(self.time)), self.score),
            '',
            'Would you like to save your score?'
        ]
        self._collect_name = False
        self._name = ''

    def update(self, key_state=None, key_str=''):
        if self._collect_name:
            if key_state == Key.ENTER:
                with open('leaderboard.txt', 'a+') as file:
                    file.write('%s %s %s\n' % (self._name, self.score, self.time))
                self.switch(LeaderBoardContext)
            else:
                if key_str.isalnum():
                    if len(key_str) == 1:
                        self._name += key_str
                    elif key_str == 'backspace':
                        self.clear()
                        self._name = self._name[:-1]
                elif key_str == '_':
                    self._name += '_'
            self.render(['Name: %s' % self._name])
            return
        if key_state:
            if key_state in (Key.LEFT, Key.RIGHT):
                self._swap_menu()
            elif key_state == Key.ENTER:
                for _, v in self.menu.items():
                    if v[0]:
                        v[1]()
        menu_line = []
        for k, v in self.menu.items():
            if v[0]:
                menu_line.append('[%s]' % k)
            else:
                menu_line.append(' %s ' % k)
        self.render(self._message + ['\t'.join(menu_line)])
        time.sleep(0.02)
        self.clear()

    def _swap_menu(self):
        for k in self.menu:
            self.menu[k][0] = not self.menu[k][0]

    def _save(self):
        self.clear()
        self._collect_name = True


class LeaderBoardContext(TextContext):
    def __init__(self, on_close=None, on_switch=None):
        super().__init__(on_close, on_switch)
        self.lb = []
        with open('leaderboard.txt', 'r+') as file:
            data = file.read().split('\n')
            data.pop()
            org_data = {}
            for item in data:
                split_item = item.split(' ')
                score, player_time = int(split_item[1]), float(split_item[2])
                if score == 0:
                    org_data[player_time] = split_item
                elif score * 10 - player_time < 0:
                    org_data[abs(score * 10 - player_time)] = split_item
                else:
                    org_data[score * 10 - player_time] = split_item
            keys = list(org_data.keys())
            keys.sort()
            for i, k in enumerate(keys):
                items = org_data[k]
                self.lb.append('%d | %s %s %s' % (i + 1, items[0], items[1], time.strftime('%M:%S', time.localtime(round(float(items[2]))))))
        self.rendered = False

    def update(self, key_state=None, key_str=''):
        if not self.rendered:
            self.clear()
            self.render(self.lb + ['', '[ Back to Menu ]'])
            self.rendered = True
        if key_state:
            if key_state == Key.ENTER:
                self.switch(MenuContext)
