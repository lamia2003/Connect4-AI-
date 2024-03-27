import tkinter as tk

class Connect4:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = [[None for _ in range(cols)] for _ in range(rows)]
        self.current_player = "R"
        self.last_move = None
        self.winning_moves = None

    def drop_piece(self, col):
        for row in reversed(range(self.rows)):
            if self.board[row][col] is None:
                self.board[row][col] = self.current_player
                self.last_move = (row, col)  # Update the last move here
                if self.check_win(row, col):
                    winner = self.current_player
                    self.current_player = "Y" if self.current_player == "R" else "R"
                    return winner
                self.current_player = "Y" if self.current_player == "R" else "R"
                return None
        return None
    
    def check_win(self, row, col):
        # Check horizontal
        for c in range(max(0, col - 3), min(self.cols - 3, col + 1)):
            if all(self.board[row][c + i] == self.board[row][col] for i in range(4)):
                self.winning_moves = [(row, c + i) for i in range(4)]
                return True

        # Check vertical
        for r in range(max(0, row - 3), min(self.rows - 3, row + 1)):
            if all(self.board[r + i][col] == self.board[row][col] for i in range(4)):
                self.winning_moves = [(r + i, col) for i in range(4)]
                return True

        # Check diagonal (\)
        for r, c in zip(range(row - 3, row + 1), range(col - 3, col + 1)):
            if r >= 0 and c >= 0 and r + 3 < self.rows and c + 3 < self.cols:
                if all(self.board[r + i][c + i] == self.board[row][col] for i in range(4)):
                    self.winning_moves = [(r + i, c + i) for i in range(4)]
                    return True

        # Check diagonal (/)
        for r, c in zip(range(row - 3, row + 1), range(col + 3, col - 1, -1)):
            if r >= 0 and c < self.cols and r + 3 < self.rows and c - 3 >= 0:
                if all(self.board[r + i][c - i] == self.board[row][col] for i in range(4)):
                    self.winning_moves = [(r + i, c - i) for i in range(4)]
                    return True

        return False
    
    def check_for_win(self):
    # Check for a win in all directions for all positions on the board
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] is not None and self.check_win(row, col):
                    return True
        return False

    def check_for_draw(self):
        # Check if the board is full
        return all(self.board[0][col] is not None for col in range(self.cols))
        
    def evaluate_board(self):
        score = 0
        # Check for 3-in-a-rows and 2-in-a-rows for both players
        for row in range(self.rows):
            for col in range(self.cols - 3):
                window = [self.board[row][col + i] for i in range(4)]
                score += self.evaluate_window(window, self.current_player)

        for col in range(self.cols):
            for row in range(self.rows - 3):
                window = [self.board[row + i][col] for i in range(4)]
                score += self.evaluate_window(window, self.current_player)

        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                window = [self.board[row + i][col + i] for i in range(4)]
                score += self.evaluate_window(window, self.current_player)

        for row in range(3, self.rows):
            for col in range(self.cols - 3):
                window = [self.board[row - i][col + i] for i in range(4)]
                score += self.evaluate_window(window, self.current_player)

        return score
    
    def minimax(self, depth, alpha, beta, maximizing_player):
        # Base case: check for terminal states (win, draw) or maximum depth
        if depth == 0 or self.check_for_win() or self.check_for_draw():
            return self.evaluate_board()

        if maximizing_player:
            max_eval = float("-inf")
            for col in range(self.cols):
                if self.board[0][col] is None:  # Check if the column is not full
                    # Make a move
                    row = self.find_row_for_col(col)
                    self.board[row][col] = self.current_player
                    eval = self.minimax(depth - 1, alpha, beta, False)
                    # Undo the move
                    self.board[row][col] = None
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break  # Alpha-beta pruning
            return max_eval
        else:
            min_eval = float("inf")
            for col in range(self.cols):
                if self.board[0][col] is None:  # Check if the column is not full
                    # Make a move
                    row = self.find_row_for_col(col)
                    self.board[row][col] = "Y" if self.current_player == "R" else "R"
                    eval = self.minimax(depth - 1, alpha, beta, True)
                    # Undo the move
                    self.board[row][col] = None
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break  # Alpha-beta pruning
            return min_eval
        
    def find_row_for_col(self, col):
        for row in reversed(range(self.rows)):
            if self.board[row][col] is None:
                return row
    
    def ai_move(self):
        # Use minimax to find the best move
        best_score = float("-inf")
        best_col = None
        for col in range(self.cols):
            if self.board[0][col] is None:  # Check if the column is not full
                row = self.find_row_for_col(col)
                self.board[row][col] = self.current_player
                score = self.minimax(4, float("-inf"), float("inf"), False)  # Adjust depth as needed
                self.board[row][col] = None
                if score > best_score:
                    best_score = score
                    best_col = col
        return best_col
    
    def evaluate_window(self, window, player):
        score = 0
        opp_player = "R" if player == "Y" else "Y"

        if window.count(player) == 4:
            score += 100
        elif window.count(player) == 3 and window.count(None) == 1:
            score += 10  # More points for potential win
        elif window.count(player) == 2 and window.count(None) == 2:
            score += 5  # Points for two-in-a-row with space for more

        if window.count(opp_player) == 3 and window.count(None) == 1:
            score -= 50  # High negative score to block opponent's potential win
        elif window.count(opp_player) == 2 and window.count(None) == 2:
            score -= 10  # Negative score to block opponent's two-in-a-row

        # Adding points for a single piece as it could lead to a win
        if window.count(player) == 1 and window.count(None) == 3:
            score += 1

        # Open three-in-a-row is a significant threat/opportunity (e.g., "O_OO" or "OO_O")
        if window.count(player) == 3 and window.count(None) == 1:
            if window.index(None) == 1 or window.index(None) == 2:
                score += 20  # Strong opportunity for next move
        if window.count(opp_player) == 3 and window.count(None) == 1:
            if window.index(None) == 1 or window.index(None) == 2:
                score -= 40  # Strong need to block opponent

        return score



class Connect4GUI:
    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("Connect4")
        self.buttons = [tk.Button(self.root, text="Drop", command=lambda c=col: self.drop_piece(c)) for col in range(game.cols)]
        self.grid = [[tk.Label(self.root, width=4, height=2, borderwidth=1, relief="solid") for _ in range(game.cols)] for _ in range(game.rows)]
        self.restart_button = tk.Button(self.root, text="Restart", command=self.restart_game)
        self.restart_button.grid(row=self.game.rows + 2, columnspan=self.game.cols)
        self.win_message = tk.Label(self.root, text="", font=("Arial", 16))
        self.win_message.grid(row=self.game.rows + 1, columnspan=self.game.cols)

        for col, button in enumerate(self.buttons):
            button.grid(row=0, column=col)
        for row in range(game.rows):
            for col in range(game.cols):
                self.grid[row][col].grid(row=row + 1, column=col)

    def drop_piece(self, col):
        result = self.game.drop_piece(col)
        if result:
            self.display_win(result)
            return

        # Update the GUI after a move
        for row in range(self.game.rows):
            for col in range(self.game.cols):
                if self.game.board[row][col] is not None:
                    self.grid[row][col]["bg"] = "red" if self.game.board[row][col] == "R" else "yellow"
        
        # Make the AI move if the game is still ongoing
        if self.game.current_player == "Y":
            self.ai_move()

    def ai_move(self):
        col = self.game.ai_move()
        self.drop_piece(col)

    def display_win(self, winner):
        winner_color = "User" if winner == "R" else "AI"
        self.win_message.config(text=f"{winner_color} wins!")  # Update the win message
        for row, col in self.game.winning_moves:
            self.grid[row][col]["bg"] = "blue"
        for button in self.buttons:
            button["state"] = "disabled"

    def restart_game(self):
        # Reset the game state
        self.game = Connect4()
        # Update the GUI
        for row in range(self.game.rows):
            for col in range(self.game.cols):
                self.grid[row][col]["bg"] = "white"
        for button in self.buttons:
            button["state"] = "normal"
        self.win_message.config(text="")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = Connect4()
    gui = Connect4GUI(game)
    gui.run()
