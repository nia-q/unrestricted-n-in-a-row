# N-Row Game - Technical Documentation

## Project Structure

```
n-row/
├── main.py         # Entry point with exception handling
├── game.py         # Game class + GameExit exception
├── board.py        # Board class with game logic
├── player.py       # Player class for player data
├── README.md       # User-facing documentation
└── DEVELOPMENT.md  # This technical reference
```

## Detailed Class Documentation

### `Player` Class (`player.py`)
**Responsibility**: Store player identity and symbol

#### Attributes
```python
name: str          # Player's display name
symbol: str        # Game piece symbol ('X' or 'O')
```

#### Methods
```python
__init__(name: str, symbol: str) -> None
    # Initialize player with name and symbol
get_name() -> str
    # Returns player's name
get_symbol() -> str
    # Returns player's symbol
```

---

### `Board` Class (`board.py`)
**Responsibility**: Game state management, move validation, win detection, rendering

#### Attributes
```python
state: dict[tuple[int, int], str]    # Maps (x,y) coordinates to symbols
min_x: int                           # Left boundary of placed pieces
max_x: int                           # Right boundary of placed pieces  
min_y: int                           # Top boundary of placed pieces
max_y: int                           # Bottom boundary of placed pieces
```

#### Methods

##### Piece Placement
```python
place_piece(x: int, y: int, symbol: str) -> None
    # Add piece to board state
    # Update coordinate boundaries for rendering
    # Algorithm: min/max boundary expansion
```

##### Move Validation
```python
is_valid_move(x: int, y: int) -> bool
    # Check if move is legal
    # Rules:
    #   1. Position not occupied
    #   2. First move: anywhere allowed
    #   3. Subsequent moves: within Manhattan distance ≤ 3 of existing piece
    # Algorithm: Manhattan distance calculation |x1-x2| + |y1-y2|
```

##### Win Detection
```python
check_win(x: int, y: int, symbol: str) -> bool
    # Check if placement creates 5-in-a-row
    # Directions checked: horizontal, vertical, both diagonals
    # Algorithm: Bidirectional line counting from placed piece
    #   - For each direction (dx, dy):
    #     - Count pieces in positive direction
    #     - Count pieces in negative direction  
    #     - Total = 1 (current) + positive + negative
    #     - Win if total ≥ 5
```

**Win Detection Implementation Details**:
- **Directions**: `[(1,0), (0,1), (1,1), (1,-1)]` for horizontal, vertical, and diagonals
- **Step Values**: `(1, -1)` to check both directions along each line
- **Nested Loop Structure**:
  1. **Outer**: For each direction
  2. **Middle**: For each step direction (positive/negative)
  3. **Inner**: Count consecutive pieces until gap/opponent

##### Rendering System
```python
get_bounds(pad: int = 3) -> tuple[int, int, int, int]
    # Calculate rendering boundaries with padding
    # Returns: (min_x-pad, max_x+pad, min_y-pad, max_y+pad)

render(pad: int = 3) -> None
    # Display board to console
    # Algorithm:
    #   1. Calculate bounds with padding
    #   2. Print column headers (x-coordinates)
    #   3. Print each row with y-coordinate and content
    #   4. Use 3-character formatting for alignment
```

**Rendering Implementation**:
- **Column Headers**: `"   " + "".join(f"{x:>3}" for x in range(min_x, max_x + 1))`
  - 3 spaces for alignment with row numbers
  - Each x-coordinate formatted as 3-char wide, right-aligned
  - Empty string join (no separator) because spacing is built into formatting
- **Row Content**: `f"{y:>3}" + "".join(f"{self.state.get((x, y), '.'):>3}" for x in range(...))`
  - Row number right-aligned in 3 characters
  - Each position shows piece symbol or '.' if empty
  - Same 3-character formatting for perfect alignment

---

### `Game` Class (`game.py`)
**Responsibility**: Game orchestration, turn management, input handling

#### Attributes
```python
players: List[Player]              # List of 2 players [X, O]
board: Board                       # Game board instance
current_player: Player             # Currently active player
_current_player_index: int         # Index for turn switching (0 or 1)
```

#### Methods

##### Game Management
```python
__init__(player1_name: str, player2_name: str) -> None
    # Initialize game with 2 players
    # Create board, set first player

switch_turns() -> None
    # Alternate between players
    # Algorithm: index = (index + 1) % 2
```

**Turn Switching Logic**:
- **Current Player 0**: `(0 + 1) % 2 = 1` → Switch to Player 1
- **Current Player 1**: `(1 + 1) % 2 = 0` → Switch to Player 0
- Modulo operation creates wraparound behavior for any number of players

##### Input Processing
```python
get_player_move() -> tuple[int, int]
    # Get and validate player input
    # Formats supported: "x,y" or "x y"
    # Special commands: "quit", "exit"
    # Validation: coordinate parsing, move legality
    # Error handling: invalid input, non-integers
    # Raises: GameExit if player quits
```

##### Game Loop
```python
play() -> None
    # Main game execution
    # Flow:
    #   1. Display welcome and initial board
    #   2. Loop until win or exit:
    #      - Get player move
    #      - Place piece
    #      - Display updated board
    #      - Check win condition
    #      - Switch turns
    #   3. Announce winner
```

---

### `GameExit` Exception (`game.py`)
**Purpose**: Clean game termination without program exit

```python
class GameExit(Exception):
    # Raised when player types "quit" or "exit"
    # Allows return to main menu instead of program termination
```

---

### `main()` Function (`main.py`)
**Responsibility**: Program entry point and exception handling

#### Exception Handling
```python
try:
    # Get player names and start game
except GameExit:
    # Handle mid-game quit gracefully
except KeyboardInterrupt:
    # Handle Ctrl+C interruption
```

## Game Flow Analysis

### Initialization Sequence
1. `main.py` prompts for player names
2. `Game` class instantiated with 2 players (X and O symbols)
3. Empty `Board` created with coordinate tracking
4. Player 1 (X) set as starting player

### Turn Processing Flow
1. Display current player and board state
2. Get coordinate input with validation
3. Check move validity (proximity rules)
4. Place piece and update board bounds
5. Check for win condition
6. Switch turns (if no win)
7. Repeat until win or exit

### Data Flow
**main.py** → **game.py** → **board.py** → **player.py**
- **Input handling**: `game.py`
- **Game logic**: `board.py` 
- **Orchestration**: `game.py`
- **Data storage**: `player.py`

## Algorithm Analysis

### Move Validation Complexity
**Current**: O(n) where n = number of pieces placed
- Iterates through all existing pieces to check Manhattan distance
- Manhattan distance: `abs(px - x) + abs(py - y) <= 3`

**Optimization Opportunity**: O(1) lookup with valid moves set
- Pre-compute and maintain `set[tuple[int, int]]` of valid positions
- Update set when pieces are placed (add neighbors, remove occupied)

### Win Detection Complexity
**Current**: O(1) bounded search
- Checks exactly 4 directions × 2 ways × max 4 steps = 32 position checks
- Efficient bidirectional counting from newly placed piece
- Early termination when gaps found

### Rendering Complexity
**Current**: O(area) where area = (max_x - min_x) × (max_y - min_y)
- Must check every position in rendered rectangle
- Sparse representation means most lookups return empty

## Memory Management

### Space Complexity
- **Board State**: O(n) where n = number of pieces placed
- **Player Data**: O(1) - fixed 2 players
- **Bounds Tracking**: O(1) - 4 integers
- **Total**: O(n) dominated by piece storage

### Memory Efficiency Features
- **Sparse Representation**: Only occupied positions stored
- **Dynamic Bounds**: Rendering area grows only as needed
- **No Board Pre-allocation**: Infinite board costs no upfront memory

## Error Handling Strategy

### Input Validation
- **Format Checking**: Regex or split-based coordinate parsing
- **Range Validation**: Integer conversion with error handling
- **Move Legality**: Proximity and occupation checks

### Exception Types
- **GameExit**: User-initiated quit (graceful)
- **KeyboardInterrupt**: Ctrl+C handling (graceful)
- **ValueError**: Invalid input parsing (recovered)

## Testing Considerations

### Key Test Cases
1. **First Move**: Can be placed anywhere
2. **Proximity Rules**: Valid/invalid distance checks
3. **Win Detection**: All 4 directions + edge cases
4. **Boundary Updates**: Coordinate tracking accuracy
5. **Turn Switching**: Alternation logic
6. **Input Parsing**: Various formats and edge cases

### Performance Testing
- **Large Boards**: Many pieces placed (memory usage)
- **Dense Areas**: Many pieces close together (rendering performance)
- **Win Near Edges**: Edge cases in win detection 