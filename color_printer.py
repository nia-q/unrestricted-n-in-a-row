class ColorPrinter:
    def __init__(self):
        """Initialize ColorPrinter with rainbow colors and cycling state."""
        # ANSI color codes for rainbow colors (ROYGBIV)
        self.COLORS = [
            '\033[91m',  # Red
            '\033[38;5;208m',  # Orange (true orange color)
            '\033[93m',  # Yellow (bright yellow)
            '\033[32m',  # Green  
            '\033[94m',  # Blue
            '\033[95m',  # Indigo (magenta as substitute)
            '\033[96m',  # Violet (cyan as substitute)
        ]
        self.RESET = '\033[0m'  # Reset to default color
        self.color_index = 0  # Track current color position in rainbow cycle
    
    def print_colored(self, message: str = "") -> None:
        """
        Print a message in the next rainbow color, then advance to next color.
        
        Args:
            message: The text to print (can be empty for blank lines)
        """
        color = self.COLORS[self.color_index]
        print(f"{color}{message}{self.RESET}")
        
        # Advance to next color (cycle back to 0 after last color)
        self.color_index = (self.color_index + 1) % len(self.COLORS)
    
    def reset_colors(self) -> None:
        """Reset color cycling back to the beginning (Red)."""
        self.color_index = 0 