import pygame
import chess
import chess.engine
import chess.svg
import cairosvg
import pymongo
from dotenv import load_dotenv
import io
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

# MongoDB Setup
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "chess_games"
COLLECTION_NAME = "games"

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Create a new game document in MongoDB
game_doc = {
    "moves": [],
    "result": None,
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
}
game_id = collection.insert_one(game_doc).inserted_id  # Get the document ID

def render_board():
    """Convert the board into an image and display it using pygame."""
    svg_board = chess.svg.board(board=board, size=WIDTH, colors=custom_colors)
    png_bytes = cairosvg.svg2png(bytestring=svg_board.encode("utf-8"))
    image = pygame.image.load(io.BytesIO(png_bytes))
    screen.blit(image, (0, 0))
    pygame.display.flip()

def update_game_in_db(engine_name, move, eval_score, time_taken, fen):
    """Push each move into MongoDB in real-time."""
    move_data = {
        "engine": engine_name,
        "move": move.uci(),
        "evaluation": eval_score,
        "time_taken": round(time_taken, 3),
        "fen": fen,
    }

    collection.update_one({"_id": game_id}, {"$push": {"moves": move_data}})
    print(f"✅ Move saved to MongoDB: {move_data}")

# Game loop
running = True
render_board()

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

    update_game_in_db("Lc0", lc0_result.move, lc0_result.info.get("score", None), end_time - start_time, board.fen())

    if board.is_game_over():
        break

    # Stockfish plays next
    print("\nStockfish is thinking...")
    start_time = time.time()
    stockfish_result = stockfish.play(board, chess.engine.Limit(time=0.01))
    end_time = time.time()
    
    board.push(stockfish_result.move)
    render_board()

    update_game_in_db("Stockfish", stockfish_result.move, stockfish_result.info.get("score", None), end_time - start_time, board.fen())

# Store the final game result
game_result = board.result()
collection.update_one({"_id": game_id}, {"$set": {"result": game_result}})
print("\nGame Over!")
print(f"Result: {game_result}")

# Cleanup
stockfish.quit()
lc0.quit()
pygame.quit()