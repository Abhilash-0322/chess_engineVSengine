import groq
import chess

# Groq API Key
GROQ_API_KEY = "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"

# Initialize Groq client
client = groq.Client(api_key=GROQ_API_KEY)

def get_llm_move(fen):
    """Get the best chess move from Groq's LLM based on the given FEN position."""
    prompt = f"Given this chess position in FEN: {fen}, suggest the best move in UCI format (e.g., e2e4). Only return the move, nothing else."

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        # Extract the move from the response
        move = response.choices[0].message.content.strip()
        if chess.Move.from_uci(move) in chess.Board(fen).legal_moves:
            return move
        else:
            print(f"Invalid move received: {move}. Defaulting to e2e4.")
            return "e2e4"

    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return "e2e4"  # Safe fallback move

# Example usage
fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
llm_move = get_llm_move(fen)
print(f"LLM Move: {llm_move}")