import chess
import chess.engine

# Path to Stockfish engine (update this path if necessary)
STOCKFISH_PATH = "D:\codespace\stockfish\stockfish-windows-x86-64-avx2.exe"  # Change this if the path is different
LCO_PATH="D:\codespace\lco Engine\lc0.exe"
# Load Stockfish engine
engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

engine2=chess.engine.SimpleEngine.popen_uci(LCO_PATH)

# Initialize board
board = chess.Board()

print("Welcome to Chess! You will play as White.")
print(board)

while not board.is_game_over():
    # Get user's move
    # user_move = input("\nEnter your move (e.g., e2e4): ").strip()
    
    # # Validate move
    # if user_move not in [move.uci() for move in board.legal_moves]:
    #     print("Invalid move. Try again.")
    #     continue
    
    # Apply user's move
    # board.push_uci(user_move)
    # print("\nYour move:")
    print("\n Lc0 is thinking...")
    result2=engine2.play(board,chess.engine.Limit(time=1.0))
    board.push(result2.move)


    print("\n Lc0's move:")
    print(board)

    if board.is_game_over():
        break

    # Get engine's move
    print("\nStockfish is thinking...")
    result = engine.play(board, chess.engine.Limit(time=1.0))  # Adjust time for difficulty
    board.push(result.move)

    # Display board after engine move
    print("\nStockfish's move:")
    print(board)

# Display final result
print("\nGame Over!")
print(f"Result: {board.result()}")

# Close the engine
engine.quit()