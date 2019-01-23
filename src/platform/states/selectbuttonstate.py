from platform.states.state import State


class SelectButtonState(State):
    name = 'select button'
    button = None
    parent_state = None

    def __init__(self, parent_state):
        self.parent_state = parent_state

    def on_enter(self, protocol, player):
        return S_SELECT_BUTTON

    def on_exit(self, protocol, player):
        self.parent_state.button = self.button
        player.previous_button = self.button or player.previous_button
        if player.states.top() is self.parent_state:
            player.states.pop()
        elif self.button:
            return S_BUTTON_SELECTED.format(label = self.button.label)