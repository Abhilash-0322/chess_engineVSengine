import pygame
import chess
import chess.engine
import chess.svg
import groq
import cairosvg
import io

# Groq API Key
GROQ_API_KEY = ""

# Initialize Groq client
client = groq.Client(api_key=GROQ_API_KEY)

# Path to Stockfish engine
STOCKFISH_PATH = "D:/codespace/stockfish/stockfish-windows-x86-64-avx2.exe"

# Initialize Stockfish
stockfish = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

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
pygame.display.set_caption("LLM vs Stockfish")

def render_board():
    """Convert the board into an image and display it using pygame."""
    svg_board = chess.svg.board(board=board, size=WIDTH, colors=custom_colors)
    png_bytes = cairosvg.svg2png(bytestring=svg_board.encode('utf-8'))
    image = pygame.image.load(io.BytesIO(png_bytes))
    screen.blit(image, (0, 0))
    pygame.display.flip()

def get_llm_move(fen):
    """Get the best chess move from Groq's LLM based on the given FEN position."""
    prompt = f"Given this chess position in FEN: {fen}, suggest the best move in UCI format (e.g., e2e4). Only return the move, nothing else."

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )

        # Extract move
        move = response.choices[0].message.content.strip()
        move_obj = chess.Move.from_uci(move)

        # Validate move legality
        if move_obj in board.legal_moves:
            return move
        else:
            print(f"❌ Invalid move received: {move}. Choosing a random legal move.")
            return str(board.legal_moves.__iter__().__next__())  # Pick first legal move

    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return str(board.legal_moves.__iter__().__next__())  # Safe fallback move

# Game loop
running = True
render_board()

while running and not board.is_game_over():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # LLM Move
    print("\nLLM is thinking...")
    llm_move = get_llm_move(board.fen())

    # Ensure the move is applied correctly
    move_obj = chess.Move.from_uci(llm_move)
    if move_obj in board.legal_moves:
        board.push(move_obj)
        render_board()
    else:
        print(f"⚠️ Skipping invalid LLM move: {llm_move}")

    if board.is_game_over():
        break

    # Stockfish Move
    print("\nStockfish is thinking...")
    stockfish_move = stockfish.play(board, chess.engine.Limit(time=1.0))
    board.push(stockfish_move.move)
    render_board()

print("\nGame Over!")
print(f"Result: {board.result()}")

# Cleanup
stockfish.quit()
pygame.quit()