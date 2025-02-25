echo "♟️ Setting up the environment..."

if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 is not installed. Please install it and try again."
    exit 1
fi

# Create a virtual environment (optional but recommended)
echo "🔹 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate


echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt


echo "🚀 Starting Chess Engine Battle..."
python save_move_db.py