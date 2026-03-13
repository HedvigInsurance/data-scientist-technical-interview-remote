# Data Scientist Technical Interview - Setup

## Prerequisites

- Python 3.10 or higher
- Git

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd data-scientist-technical-interview-remote
```

### 2. Create a Python Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Verify Setup

Run the verification script to ensure everything is configured correctly:

```bash
python verify_setup.py
```

If the script reports that everything is working correctly, you're ready for the interview!

## Troubleshooting

If you encounter any issues during setup, please ensure:
- You're using Python 3.10 or higher (`python --version`)
- Your virtual environment is activated
- All dependencies installed successfully without errors