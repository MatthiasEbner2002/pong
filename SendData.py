

class SendData():
    def __init__(self, player_position, game_state, ball_x, ball_y, server_score, client_score):
        self.player_position = player_position
        self.game_state = game_state
        self.ball_x = ball_x
        self.ball_y = ball_y
        self.server_score = server_score
        self.client_score = client_score
        
    def __getstate__(self):
        return (
            self.player_position,
            self.game_state,
            self.ball_x,
            self.ball_y,
            self.server_score,
            self.client_score
        )

    def __setstate__(self, state):
        (
            self.player_position,
            self.game_state,
            self.ball_x,
            self.ball_y,
            self.server_score,
            self.client_score
        ) = state