# import chess
# import chess.engine

# # Path to Stockfish engine (update this path if necessary)
# STOCKFISH_PATH = "D:\codespace\stockfish\stockfish-windows-x86-64-avx2.exe"  # Change this if the path is different
# LCO_PATH="D:\codespace\lco Engine\lc0.exe"
# # Load Stockfish engine
# engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

# engine2=chess.engine.SimpleEngine.popen_uci(LCO_PATH)

# # Initialize board
# board = chess.Board()

# print("Welcome to Chess! You will play as White.")
# print(board)

# while not board.is_game_over():
#     # Get user's move
#     # user_move = input("\nEnter your move (e.g., e2e4): ").strip()
    
#     # # Validate move
#     # if user_move not in [move.uci() for move in board.legal_moves]:
#     #     print("Invalid move. Try again.")
#     #     continue
    
#     # Apply user's move
#     # board.push_uci(user_move)
#     # print("\nYour move:")
#     print("\n Lc0 is thinking...")
#     result2=engine2.play(board,chess.engine.Limit(time=1.0))
#     board.push(result2.move)


#     print("\n Lc0's move:")
#     print(board)

#     if board.is_game_over():
#         break

#     # Get engine's move
#     print("\nStockfish is thinking...")
#     result = engine.play(board, chess.engine.Limit(time=1.0))  # Adjust time for difficulty
#     board.push(result.move)

#     # Display board after engine move
#     print("\nStockfish's move:")
#     print(board)

# # Display final result
# print("\nGame Over!")
# print(f"Result: {board.result()}")

# # Close the engine
# engine.quit()


import pygame
import chess
import chess.engine
import chess.svg
import cairosvg
import io

# Path to your engines
STOCKFISH_PATH = "D:/codespace/stockfish/stockfish-windows-x86-64-avx2.exe"
LCO_PATH = "D:/codespace/lco Engine/lc0.exe"

# Initialize engines
stockfish = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
lc0 = chess.engine.SimpleEngine.popen_uci(LCO_PATH)

# Define board colors
custom_colors = {
    "square light": "#EEEED2",  # Light squares
    "square dark": "#769656",   # Dark squares
    "square light lastmove": "#A9A9A9",  # Highlight last move on light square
    "square dark lastmove": "#696969",   # Highlight last move on dark square
}

# Initialize board
board = chess.Board()

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Engine vs Engine")

def render_board():
    """Convert the board into an image and display it using pygame."""
    svg_board = chess.svg.board(board=board, size=WIDTH,colors=custom_colors)
    png_bytes = cairosvg.svg2png(bytestring=svg_board.encode('utf-8'))
    image = pygame.image.load(io.BytesIO(png_bytes))
    screen.blit(image, (0, 0))
    pygame.display.flip()

# Game loop
running = True
while running and not board.is_game_over():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Lc0 plays first
    print("\nLc0 is thinking...")
    lc0_move = lc0.play(board, chess.engine.Limit(time=1.0))
    board.push(lc0_move.move)
    render_board()
    
    if board.is_game_over():
        break

    # Stockfish plays next
    print("\nStockfish is thinking...")
    stockfish_move = stockfish.play(board, chess.engine.Limit(time=1.0))
    board.push(stockfish_move.move)
    render_board()

print("\nGame Over!")
print(f"Result: {board.result()}")

# Cleanup
stockfish.quit()
lc0.quit()
pygame.quit()