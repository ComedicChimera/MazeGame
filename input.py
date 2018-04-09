import keyboard


class Key:
    UP = 72
    DOWN = 80
    LEFT = 75
    RIGHT = 77
    ENTER = 28


class InputHandler:
    def __init__(self):
        """Initialize event handler"""

        self._update_state = False

        def emit(symbol):
            self._update_state = symbol

        # add all the hotkeys
        keyboard.on_press(emit)

    def collect(self):
        """Collect latest input state.
        If state has not changed, nothing is returned"""

        if self._update_state:
            key = self._update_state
            self._update_state = False
            return key
