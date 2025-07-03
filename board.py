class Board:
    def __init__(self) -> None:
        # Dictionary mapping (x, y) coordinates to player symbols
        self.state: dict[tuple[int, int], str] = {}
        # Track the minimum and maximum coordinates for rendering bounds
        self.min_x: int = 0
        self.max_x: int = 0
        self.min_y: int = 0
        self.max_y: int = 0

    def place_piece(self, x: int, y: int, symbol: str) -> None:
        """
        Place a game piece at the specified coordinates.
        
        Args:
            x: The x-coordinate where to place the piece
            y: The y-coordinate where to place the piece
            symbol: The player's symbol (e.g., 'X' or 'O')
        """
        # Add the piece to the board state
        self.state[(x, y)] = symbol
        # Update the board bounds to include this new piece
        self.min_x = min(self.min_x, x)  # Expand left boundary if needed
        self.max_x = max(self.max_x, x)  # Expand right boundary if needed
        self.min_y = min(self.min_y, y)  # Expand bottom boundary if needed
        self.max_y = max(self.max_y, y)  # Expand top boundary if needed

    def is_valid_move(self, x: int, y: int) -> bool:
        """
        Check if a move at the given coordinates is valid.

        A move is valid if:
        1. The position is not already occupied
        2. It's the first move (anywhere is allowed), OR
        3. It's within 3 non-diagonal moves (Manhattan distance) of an existing piece

        Args:
            x: The x-coordinate to check
            y: The y-coordinate to check

        Returns:
            True if the move is valid, False otherwise
        """
        # Check if the position is already occupied
        if (x, y) in self.state:
            return False
        # Check if it's the first move
        if not self.state:
            return True

        # Check if the move is within 3 non-diagonal moves of an existing piece
        #for coordinate pair in occupied spaces
        for (px, py) in self.state:
            #if input coordinate pair can be reached in 3 moves return true 
            if abs(px - x) + abs(py - y) <= 3:
                return True

        return False

    def check_win(self, x: int, y: int, symbol: str) -> bool:
        """
        Check if placing a piece at (x, y) creates a winning condition.

        A win occurs when 5 or more pieces of the same symbol are aligned
        horizontally, vertically, or diagonally.

        Args:
            x: The x-coordinate of the newly placed piece
            y: The y-coordinate of the newly placed piece
            symbol: The symbol to check for winning condition

        Returns:
            True if this move creates a win, False otherwise
        """
        # Define the four possible directions to check for 5-in-a-row:
        # (1, 0) = horizontal (left-right)
        # (0, 1) = vertical (up-down) 
        # (1, 1) = diagonal (bottom-left to top-right)
        # (1, -1) = diagonal (top-left to bottom-right)
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        # Check each of the four directions for a potential win
        for dx, dy in directions:
            # Start counting with the newly placed piece (count = 1)
            count = 1  # Start with the current piece
            
            # For each direction, we need to check BOTH ways along the line
            # step = 1 means go in positive direction (dx, dy)
            # step = -1 means go in negative direction (-dx, -dy)
            for step in (1, -1):  # Check both directions along the line
                # Start from the newly placed piece position
                nx, ny = x, y
                
                # Keep moving in this direction until we hit an empty space or opponent piece
                while True:
                    # Move one step further in the current direction
                    # If step=1: move by (dx, dy), if step=-1: move by (-dx, -dy)
                    nx += dx * step
                    ny += dy * step

                    # Check if this position contains the same symbol as ours
                    if self.state.get((nx, ny)) == symbol:
                        # Found another piece of our symbol, increment count
                        count += 1
                    else:
                        # Hit an empty space or opponent's piece, stop checking this direction
                        break

            # After checking both directions along this line, see if we have 5+ in a row
            if count >= 5:
                return True  # Winning condition met

        # If we've checked all four directions and none had 5+ in a row
        return False  # No 5 in a row found

    def get_bounds(self, pad: int = 3) -> tuple[int, int, int, int]:
        """
        Get the rendering bounds of the board with optional padding.
        
        Args:
            pad: Number of empty spaces to add around the board for rendering
            
        Returns:
            Tuple of (min_x, max_x, min_y, max_y) coordinates for rendering
        """
        return (
            self.min_x - pad,  # Left boundary with padding
            self.max_x + pad,  # Right boundary with padding
            self.min_y - pad,  # Bottom boundary with padding
            self.max_y + pad   # Top boundary with padding
        )

    def render(self, printer, pad: int = 3) -> None:
        """
        Display the current board state to the console using colored output.
        
        Args:
            printer: ColorPrinter instance for colored output
            pad: Number of empty spaces to show around the board edges
        """
        min_x, max_x, min_y, max_y = self.get_bounds(pad)
        
        # Print column headers: "   " (3 spaces for alignment) + "".join() (no separator) 
        # + f"{x:>3}" (each x-coordinate formatted as 3-char wide, right-aligned string)
        header = "   " + "".join(f"{x:>3}" for x in range(min_x, max_x + 1))
        printer.print_colored(header)
        
        # Print each row with row number and content
        for y in range(min_y, max_y + 1):  # Loop through each y-coordinate (row) from top to bottom
            # Build the content for this row: get piece at each (x,y) or '.' if empty,
            # format each as 3-char wide right-aligned, then join with no separator
            row_content = "".join(f"{self.state.get((x, y), '.'):>3}" for x in range(min_x, max_x + 1))
            # Print row: f"{y:>3}" (row number right-aligned in 3 chars) + row content
            printer.print_colored(f"{y:>3}" + row_content)
