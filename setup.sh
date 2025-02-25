echo "♟️ Setting up the environment..."

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 is not installed. Please install it and try again."
    exit 1
fi

# Create a virtual environment (optional but recommended)
echo "🔹 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate  # Activate virtual environment

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run the script
echo "🚀 Starting Chess Engine Battle..."
python save_move_db.py