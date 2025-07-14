# Reddit User Persona Generator

A Python script that scrapes Reddit user profiles and generates detailed user personas using local LLM models via Ollama.

## Features

- **Reddit Data Scraping**: Extracts posts, comments, and profile information from Reddit users
- **LLM-Powered Analysis**: Uses Ollama with Llama models to generate comprehensive user personas
- **Citation System**: Each persona characteristic includes citations from the user's actual posts/comments
- **Structured Output**: Generates well-formatted text files with detailed persona analysis

## Prerequisites

### 1. Python Setup
- Python 3.8 or higher
- pip (Python package installer)

### 2. Ollama Installation

#### Windows:
```bash
# Download and install Ollama from https://ollama.ai/
# Or use winget:
winget install Ollama.Ollama
```

#### macOS:
```bash
# Using Homebrew
brew install ollama

# Or download from https://ollama.ai/
```

#### Linux:
```bash
# Using curl
curl -fsSL https://ollama.ai/install.sh | sh
```

