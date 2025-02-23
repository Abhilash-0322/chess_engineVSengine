import pygame
import chess
import chess.engine
import chess.svg
import cairosvg
import io
import time
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase  # Neo4j driver

load_dotenv()

# Paths to engines
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

# Neo4j Setup
NEO4J_URI = os.getenv('NEO_URI')
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = os.getenv('NEO_PSWD')

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def execute_query(query, params=None):
    """Helper function to run Cypher queries."""
    with driver.session() as session:
        session.run(query, params or {})

# Create a game node
game_id = str(int(time.time()))  # Unique game ID
execute_query("CREATE (:Game {id: $game_id, timestamp: $timestamp})", 
              {"game_id": game_id, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")})

def render_board():
    """Convert the board into an image and display it using pygame."""
    svg_board = chess.svg.board(board=board, size=WIDTH, colors=custom_colors)
    png_bytes = cairosvg.svg2png(bytestring=svg_board.encode("utf-8"))
    image = pygame.image.load(io.BytesIO(png_bytes))
    screen.blit(image, (0, 0))
    pygame.display.flip()

def save_move(engine_name, move, eval_score, time_taken, fen_before, fen_after):
    """Save each move to Neo4j as a relationship between board positions."""
    
    query = """
    MERGE (before:Position {fen: $fen_before})
    MERGE (after:Position {fen: $fen_after})
    MERGE (before)-[:MADE_MOVE {game_id: $game_id, engine: $engine, move: $move, 
            evaluation: $eval, time_taken: $time}]->(after)
    """
    
    execute_query(query, {
        "fen_before": fen_before,
        "fen_after": fen_after,
        "game_id": game_id,
        "engine": engine_name,
        "move": move.uci(),
        "eval": eval_score if eval_score else "N/A",
        "time": round(time_taken, 3)
    })
    print(f"✅ Move saved to Neo4j: {move.uci()} by {engine_name}")

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
    
    fen_before = board.fen()
    board.push(lc0_result.move)
    fen_after = board.fen()
    
    render_board()
    save_move("Lc0", lc0_result.move, lc0_result.info.get("score", None), end_time - start_time, fen_before, fen_after)

    if board.is_game_over():
        break

    # Stockfish plays next
    print("\nStockfish is thinking...")
    start_time = time.time()
    stockfish_result = stockfish.play(board, chess.engine.Limit(time=0.01))
    end_time = time.time()
    
    fen_before = board.fen()
    board.push(stockfish_result.move)
    fen_after = board.fen()
    
    render_board()
    save_move("Stockfish", stockfish_result.move, stockfish_result.info.get("score", None), end_time - start_time, fen_before, fen_after)

# Store the final result in Neo4j
game_result = board.result()
execute_query("MATCH (g:Game {id: $game_id}) SET g.result = $result", 
              {"game_id": game_id, "result": game_result})

print("\nGame Over!")
print(f"Result: {game_result}")

# Cleanup
stockfish.quit()
lc0.quit()
pygame.quit()
driver.close()