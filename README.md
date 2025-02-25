# Stockfish vs Lc0 - Chess AI Battle

## 🏆 Chess Engine GUI using Pygame

A fully functional **Chess AI GUI** where **Stockfish** and **Lc0** battle it out, with move tracking and **graph visualization in Neo4j**! This project lets you watch AI engines play chess in real-time and analyze their decisions.

---

## 📌 Features

✅ **Engine vs Engine Matches** (Stockfish vs Lc0) ✅ **Real-time Move Visualization** using **Pygame** ✅ **Graph-based Move Tracking** using **Neo4j** ✅ **Evaluation Scores** for AI decision-making ✅ **Move History Display** ✅ **FEN-based Board State Storage** ✅ **Fast, Smooth Rendering**

---

## 🛠️ Tech Stack

| Technology                 | Purpose                                            |
| -------------------------- | -------------------------------------------------- |
| **Python**                 | Core logic, engine integration                     |
| **Pygame**                 | GUI for real-time chess board visualization        |
| **Chess.py**               | Chess rules, move generation, and legality checks  |
| **Stockfish**              | Traditional chess AI engine                        |
| **Lc0 (Leela Chess Zero)** | Neural-network-based chess AI engine               |
| **Neo4j**                  | Graph database to visualize and analyze moves      |
| **Cairosvg**               | Converts chess board SVG to PNG for Pygame display |

---

## 🔧 Setup

1. **Download Chess Engines**

   - [Stockfish](https://stockfishchess.org/download/)
   - [Lc0](https://lczero.org/)

---
Lco Might Require CUDA Setup as Well Follow The Documentation.

---

2. **Clone this Repository**

   ```bash
   git clone https://github.com/Abhilash-0322/chess-engine-gui.git
   cd chess-engine-gui
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Update Paths in the Script** Edit the `STOCKFISH_PATH` and `LCO_PATH` variables in the script to point to your local chess engine executables or use Cloud Engines.

5. **Start the Chess Match**

   ```bash
   cd engine_vs_engine
   python engine_vs_engine.py
   ```

---

## 🎥 How It Works

1. **Engines Play Automatically**: The script lets Stockfish and Lc0 take turns making moves.
2. **Real-time Rendering**: The chessboard updates live in **Pygame**.
3. **Move Tracking in Neo4j**: Each move is stored in **Neo4j** as a graph relationship between board states.
4. **Evaluation Scores**: Engine analysis is shown for each move.
5. **Move History**: Displays moves along with time taken and evaluations.

---

## 📊 Visualization with Neo4j

The project **stores and visualizes chess moves as a graph**:

- **Nodes** represent **board positions** (FEN strings)
- **Edges** represent **moves made by engines** (Stockfish/Lc0)
- You can query the graph to analyze **patterns, openings, and decision-making**

---

## 🎥 Demo

🔹 **Video of Chess AI Battle** 🔹 [Attach your video here]

🔹 **Graph Visualization of Moves in Neo4j** 🔹 [Attach graph screenshots]

---

## 📌 Future Improvements

🚀 Adding **interactive move suggestions** 🚀 Integrating **user vs engine mode** 🚀 Implementing **more AI engines** 🚀 Enhancing **graph analytics for move analysis**

---

## 📢 Contribute

Found a bug or have a feature request? Feel free to open an issue or submit a PR!

👨‍💻 **Made by [Abhilash-0322](https://github.com/Abhilash-0322)** 🚀