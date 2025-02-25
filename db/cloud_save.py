import pygame
import chess
import chess.engine
import chess.svg
import cairosvg
import pymongo
from dotenv import load_dotenv
import io
import json
import time
import os


load_dotenv()
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

MONGO_URI = os.getenv('MONGO_URI')
# MONGO_URI="mongodb://localhost:27017"
DB_NAME = "chess_games"
COLLECTION_NAME = "games"

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

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

def save_game_data(new_game_data, filename="chess_game_data.json"):
    """Save chess game data to both JSON and MongoDB"""

    # ==== 1️⃣ Save to JSON File ====
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                existing_data = json.load(f)
                if not isinstance(existing_data, list):
                    existing_data = []
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    existing_data.append(new_game_data)

    with open(filename, "w") as f:
        json.dump(existing_data, f, indent=4)

    print("\n✅ Game data saved to JSON file!")

    # ==== 2️⃣ Save to MongoDB ====
    try:
        collection.insert_one(new_game_data)
        print("✅ Game data successfully saved to MongoDB!")
    except Exception as e:
        print(f"❌ MongoDB Insert Error: {e}")

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