# N-Row Game

A console-based 5-in-a-row strategy game where players compete on an infinite coordinate plane.

## Game Overview

Players take turns placing their pieces (X or O) on an unlimited grid. The first player to get 5 pieces in a row—horizontally, vertically, or diagonally—wins the game.

### Key Features
- **Infinite Board**: Play on an unlimited coordinate system
- **Proximity Rules**: New pieces must be placed within 3 moves of existing pieces
- **Real-time Win Detection**: Instant victory checking after each move
- **Dynamic Board Display**: View only the relevant game area with padding
- **Rainbow Color Output**: All game text displays in cycling rainbow colors (ROYGBIV)

## Game Rules

1. **First Move**: Can be placed anywhere on the board
2. **Subsequent Moves**: Must be within 3 Manhattan distance of any existing piece
3. **Winning**: Get 5 pieces in a row (any direction)
4. **Exit**: Type "quit" or "exit" during your turn, or use Ctrl+C

## Architecture Overview

### Core Classes
- **Player**: Stores player identity and game symbol
- **Board**: Manages game state, validates moves, detects wins, handles rendering
- **Game**: Orchestrates gameplay, manages turns, processes user input
- **ColorPrinter**: Handles rainbow color cycling for all console output
- **GameExit**: Custom exception for clean game termination

### Data Structures
- **Sparse Board Representation**: `dict[(x,y) → symbol]` - Only stores occupied positions
- **Boundary Tracking**: Min/max coordinates for efficient rendering
- **Player List**: Fixed array of 2 players with index-based turn switching

### Performance Characteristics

| Operation | Time Complexity | Notes |
|-----------|----------------|-------|
| Move Validation | O(n) | n = number of placed pieces |
| Win Detection | O(1) | Bounded search in 4 directions |
| Board Rendering | O(area) | area = displayed rectangle size |
| Memory Usage | O(n) | n = number of placed pieces |

### Optimization Opportunities

**Current Implementation**:
- Move validation checks all existing pieces for proximity
- Win detection is already optimized with bidirectional counting

**Future Enhancements**:
- **Valid Move Caching**: Pre-compute set of valid positions to reduce validation to O(1)
- **Spatial Indexing**: Use grid-based lookup for faster proximity checks
- **Move History**: Track recent moves for undo/redo functionality
- **Win Pattern Caching**: Cache partial win patterns to speed up repeated checks

## Technical Notes

- **Coordinate System**: (0,0) at center, infinite in all directions
- **Input Format**: "x,y" or "x y" coordinate pairs
- **Error Handling**: Graceful handling of invalid input and interruptions
- **Memory Efficient**: Sparse representation means unused board space costs nothing

## Getting Started

Run the game with:
```bash
python main.py
```

Enter player names when prompted, then take turns entering coordinates in "x,y" format. # unrestricted-n-in-a-row
