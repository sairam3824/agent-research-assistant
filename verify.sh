#!/bin/bash

echo "🔍 Verifying Agent Research Assistant Setup..."
echo ""

# Check Python
echo "1. Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "   ✅ $PYTHON_VERSION"
else
    echo "   ❌ Python 3 not found"
    exit 1
fi

# Check Node
echo "2. Checking Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "   ✅ Node $NODE_VERSION"
else
    echo "   ❌ Node.js not found"
    exit 1
fi

# Check npm
echo "3. Checking npm..."
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo "   ✅ npm $NPM_VERSION"
else
    echo "   ❌ npm not found"
    exit 1
fi

# Check backend files
echo "4. Checking backend files..."
BACKEND_FILES=(
    "backend/api.py"
    "backend/config.py"
    "backend/requirements.txt"
    "backend/.env.example"
)

for file in "${BACKEND_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file missing"
    fi
done

# Check frontend files
echo "5. Checking frontend files..."
FRONTEND_FILES=(
    "frontend/package.json"
    "frontend/app/page.tsx"
    "frontend/components/ReportView.tsx"
    "frontend/components/ProgressFeed.tsx"
)

for file in "${FRONTEND_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file missing"
    fi
done

# Check if backend venv exists
echo "6. Checking backend virtual environment..."
if [ -d "backend/venv" ]; then
    echo "   ✅ Virtual environment exists"
else
    echo "   ⚠️  Virtual environment not created yet"
    echo "      Run: cd backend && python3 -m venv venv"
fi

# Check if frontend node_modules exists
echo "7. Checking frontend dependencies..."
if [ -d "frontend/node_modules" ]; then
    echo "   ✅ Dependencies installed"
else
    echo "   ⚠️  Dependencies not installed yet"
    echo "      Run: cd frontend && npm install"
    echo "      👉 This will fix all the TypeScript errors!"
fi

# Check .env file
echo "8. Checking environment variables..."
if [ -f "backend/.env" ]; then
    echo "   ✅ .env file exists"
    
    # Check for API keys (without showing them)
    if grep -q "OPENAI_API_KEY=sk-" backend/.env 2>/dev/null; then
        echo "   ✅ OpenAI API key configured"
    else
        echo "   ⚠️  OpenAI API key not set"
    fi
    
    if grep -q "TAVILY_API_KEY=tvly-" backend/.env 2>/dev/null; then
        echo "   ✅ Tavily API key configured"
    else
        echo "   ⚠️  Tavily API key not set"
    fi
else
    echo "   ⚠️  .env file not created yet"
    echo "      Run: cp backend/.env.example backend/.env"
    echo "      Then add your API keys"
fi

echo ""
echo "📋 Summary:"
echo ""

if [ ! -d "frontend/node_modules" ]; then
    echo "⚠️  TO FIX TYPESCRIPT ERRORS:"
    echo "   cd frontend"
    echo "   npm install"
    echo ""
fi

if [ ! -f "backend/.env" ]; then
    echo "⚠️  TO ADD API KEYS:"
    echo "   cp backend/.env.example backend/.env"
    echo "   Edit backend/.env and add your keys"
    echo ""
fi

if [ ! -d "backend/venv" ]; then
    echo "⚠️  TO SETUP BACKEND:"
    echo "   cd backend"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    echo ""
fi

echo "✅ Verification complete!"
echo ""
echo "📖 Next steps: See QUICKSTART.md"
