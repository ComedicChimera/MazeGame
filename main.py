import context
import input as inp


class Game:
    def __init__(self):
        self._input_handler = inp.InputHandler()

        self._text_context = context.MenuContext(on_close=exit, on_switch=self.switch_context)

        self.update()

    def update(self):
        while True:
            symbol = self._input_handler.collect()
            if symbol:
                self._text_context.update(key_state=symbol.scan_code, key_str=symbol.name)
            else:
                self._text_context.update()

    def switch_context(self, new_context, **kwargs):
        if 'time' in kwargs:
            self._text_context = new_context(on_close=exit, on_switch=self.switch_context, **kwargs)
        else:
            self._text_context = new_context(on_close=exit, on_switch=self.switch_context, **kwargs)


Game()
