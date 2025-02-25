import pygame
import chess
import chess.engine
import chess.svg
import cairosvg
import io
import json
import time
import os

# Path to your engines
STOCKFISH_PATH = "D:/codespace/stockfish/stockfish-windows-x86-64-avx2.exe"
LCO_PATH = "D:/codespace/lco Engine/lc0.exe"

# Initialize engines
stockfish = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
lc0 = chess.engine.SimpleEngine.popen_uci(LCO_PATH)

# Define board colors
custom_colors = {
    "square light": "#EEEED2",
    "square dark": "#769656",
    "square light lastmove": "#A9A9A9",
    "square dark lastmove": "#696969",
}

# Initialize board
board = chess.Board()

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Engine vs Engine")

# Data collection
game_data = {
    "moves": [],
    "result": None,
    "timestamps": [],
}

def render_board():
    """Convert the board into an image and display it using pygame."""
    svg_board = chess.svg.board(board=board, size=WIDTH, colors=custom_colors)
    png_bytes = cairosvg.svg2png(bytestring=svg_board.encode("utf-8"))
    image = pygame.image.load(io.BytesIO(png_bytes))
    screen.blit(image, (0, 0))
    pygame.display.flip()

# Game loop
running = True
render_board()

# Function to save game data into a single JSON file with multiple games
def save_game_data(new_game_data, filename="chess_game_data.json"):
    # Check if file exists
    if os.path.exists(filename):
        # Read existing data
        with open(filename, "r") as f:
            try:
                existing_data = json.load(f)  # Load existing JSON data
                if not isinstance(existing_data, list):  # Ensure it's a list
                    existing_data = []
            except json.JSONDecodeError:
                existing_data = []  # Handle case where JSON is corrupt or empty
    else:
        existing_data = []

    # Append new game data
    existing_data.append(new_game_data)

    # Write updated list back to file
    with open(filename, "w") as f:
        json.dump(existing_data, f, indent=4)

    print("\nGame data successfully saved to", filename, "✅")

while running and not board.is_game_over():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Lc0 plays first
    print("\nLc0 is thinking...")
    start_time = time.time()
    lc0_result = lc0.play(board, chess.engine.Limit(time=0.1))
    end_time = time.time()
    
    board.push(lc0_result.move)
    render_board()

    # Record move and evaluation
    game_data["moves"].append({
        "engine": "Lc0",
        "move": lc0_result.move.uci(),
        "evaluation": lc0_result.info.get("score", None),
        "time_taken": round(end_time - start_time, 3),
        "fen": board.fen(),
    })

    if board.is_game_over():
        break

    # Stockfish plays next
    print("\nStockfish is thinking...")
    start_time = time.time()
    stockfish_result = stockfish.play(board, chess.engine.Limit(time=0.01))
    end_time = time.time()
    
    board.push(stockfish_result.move)
    render_board()

    # Record move and evaluation
    game_data["moves"].append({
        "engine": "Stockfish",
        "move": stockfish_result.move.uci(),
        "evaluation": stockfish_result.info.get("score", None),
        "time_taken": round(end_time - start_time, 3),
        "fen": board.fen(),
    })

print("\nGame Over!")
game_data["result"] = board.result()
print(f"Result: {board.result()}")

save_game_data(game_data)

# Cleanup
stockfish.quit()
lc0.quit()
pygame.quit()