from typing import List
from player import Player
from board import Board
from color_printer import ColorPrinter


class GameExit(Exception):
    pass


class Game:
    def __init__(self, player1_name: str, player2_name: str) -> None:
        """
        Initialize a new game with two players.
        
        Args:
            player1_name: Name of the first player (will use 'X' symbol)
            player2_name: Name of the second player (will use 'O' symbol)
        """
        # Create two players with their respective symbols
        self.players: List[Player] = [
            Player(player1_name, 'X'),  # First player gets X symbol
            Player(player2_name, 'O')   # Second player gets O symbol
        ]
        
        # Initialize an empty game board
        self.board: Board = Board()
        
        # Set the first player (index 0) as the starting player
        self.current_player: Player = self.players[0]
        
        # Track current player index for easy switching
        self._current_player_index: int = 0
        
        # Initialize color printer for rainbow output
        self.printer: ColorPrinter = ColorPrinter()
    
    def switch_turns(self) -> None:
        """
        Switch to the next player's turn.
        
        Alternates between player 0 and player 1 by toggling the index.
        """
        # Toggle between player at index 0 and player at index 1 using modulo operation
        self._current_player_index = (self._current_player_index + 1) % 2
        
        # Update current_player reference to point to the new active player
        self.current_player = self.players[self._current_player_index]
    
    def get_player_move(self) -> tuple[int, int]:
        """
        Get a valid move from the current player via console input.
        
        Continuously prompts the player until they enter a valid move.
        Handles input validation and move legality checking.
        Accepts coordinates as "x,y" or "x y" format.
        
        Returns:
            Tuple of (x, y) coordinates for the player's move
        """
        while True:
            try:
                # Display whose turn it is
                player_name = self.current_player.get_name()
                player_symbol = self.current_player.get_symbol()
                self.printer.print_colored(f"\n{player_name}'s turn ({player_symbol})")
                
                # Get coordinate pair input from player
                self.printer.print_colored("Enter coordinates (x,y): ")
                coords_input = input().strip()
                
                # Check for exit commands
                if coords_input in {"exit", "quit"}:
                    raise GameExit()
                
                # Parse the input - handle both comma and space separated formats
                if ',' in coords_input:
                    # Handle "x,y" format
                    x_str, y_str = coords_input.split(',', 1)
                else:
                    # Handle "x y" format (space separated)
                    parts = coords_input.split()
                    if len(parts) != 2:
                        raise ValueError("Need exactly 2 coordinates")
                    x_str, y_str = parts
                
                # Convert to integers, stripping any extra whitespace
                x = int(x_str.strip())
                y = int(y_str.strip())
                
                # Check if the move is valid according to game rules
                if self.board.is_valid_move(x, y):
                    return (x, y)  # Valid move, return coordinates
                else:
                    # Invalid move, explain the rules and ask again
                    self.printer.print_colored("Invalid move! Remember:")
                    self.printer.print_colored("- Can't place on occupied space")
                    self.printer.print_colored("- Must be within 3 moves of existing piece (except first move)")
                    
            except ValueError:
                # Handle parsing errors gracefully
                self.printer.print_colored("Please enter coordinates as 'x,y' or 'x y' (e.g., '3,4' or '3 4')")
            except KeyboardInterrupt:
                # Handle Ctrl+C gracefully
                self.printer.print_colored("\nGame interrupted by user.")
                exit(0)
    
    def play(self) -> None:
        """
        Main game loop that runs the entire game from start to finish.
        
        Handles the complete game flow:
        1. Display initial board
        2. Get player moves
        3. Place pieces
        4. Check for wins
        5. Switch turns
        6. Repeat until someone wins
        """
        self.printer.print_colored("Welcome to N-Row Game!")
        self.printer.print_colored("Get 5 in a row (horizontal, vertical, or diagonal) to win!")
        self.printer.print_colored("=" * 50)
        
        # Display the initial empty board
        self.printer.print_colored("\nInitial board:")
        self.board.render(self.printer)
        
        # Main game loop - continues until someone wins
        while True:
            # Get a valid move from the current player
            x, y = self.get_player_move()
            
            # Place the current player's piece on the board
            player_symbol = self.current_player.get_symbol()
            self.board.place_piece(x, y, player_symbol)
            
            # Display the updated board state
            self.printer.print_colored(f"\nBoard after {self.current_player.get_name()}'s move:")
            self.board.render(self.printer)
            
            # Check if this move created a winning condition
            if self.board.check_win(x, y, player_symbol):
                # Game over - current player wins!
                winner_name = self.current_player.get_name()
                self.printer.print_colored(f"\n🎉 Congratulations! {winner_name} wins! 🎉")
                self.printer.print_colored("Thanks for playing!")
                break  # Exit the game loop
            
            # No winner yet, switch to the other player's turn
            self.switch_turns()
            
            # Optional: Add a small separator for readability
            self.printer.print_colored("-" * 30)
