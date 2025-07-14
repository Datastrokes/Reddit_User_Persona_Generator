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
### 3. Download Llama Model
After installing Ollama, download the Llama model:
```bash
ollama pull llama2
```

## Installation

1. **Clone or download this repository**
2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
## Usage

### Basic Usage
```bash
python reddit_persona_generator.py "https://www.reddit.com/user/kojied/"
```

### Advanced Usage
```bash
# Use a different model
python reddit_persona_generator.py "https://www.reddit.com/user/Hungry-Move-6603/" --model llama2:13b
```

### Supported URL Formats
- `https://www.reddit.com/user/username/`
- `https://www.reddit.com/u/username/`
- `https://reddit.com/user/username`

## Output

The script generates a text file in the `sample_outputs/` directory with the following structure:

```
Reddit User Persona Analysis
Username: kojied
Generated: 2024-01-15 14:30:25
==================================================

[Detailed persona analysis with citations]
```
### Persona Sections Include:
1. **Demographics & Background**: Age range, location hints, profession
2. **Interests & Hobbies**: Main topics, frequented subreddits
3. **Personality Traits**: Communication style, attitude, values
4. **Technical Knowledge**: Expertise levels in various topics
5. **Online Behavior**: Interaction patterns, posting frequency
6. **Values & Beliefs**: Political views, ethical stances
7. **Communication Style**: Writing tone, vocabulary, formality

## Example Outputs

The `sample_outputs/` directory contains example persona files for:
- `kojied_persona.txt` - Analysis of user "kojied"
- `Hungry-Move-6603_persona.txt` - Analysis of user "Hungry-Move-6603"

## Troubleshooting

### Common Issues

1. **Ollama not running**:
   ```bash
   # Start Ollama service
   ollama serve
   ```

2. **Model not found**:
   ```bash
   # List available models
   ollama list
   
   # Pull the required model
   ollama pull llama2
   ```

3. **Reddit rate limiting**:
   - The script includes delays and proper headers
   - If issues persist, try running later

4. **No data found**:
   - User might have private profile
   - User might have no posts/comments
   - Check if the username is correct

### Error Messages

- `"Could not extract username from URL"`: Invalid Reddit URL format
- `"Error scraping data"`: Network or Reddit API issues
- `"Error generating persona with Ollama"`: Ollama service or model issues

## Technical Details

### Data Collection
- Uses Reddit's JSON endpoints for efficient data retrieval
- Scrapes user profile pages for additional information
- Handles various Reddit URL formats

### LLM Integration
- Uses Ollama Python client for local model inference
- Configurable model selection (llama2, llama2:13b, etc.)
- Structured prompts for consistent persona generation

### Privacy & Ethics
- Only accesses publicly available Reddit data
- Respects Reddit's terms of service
- No personal information is stored beyond the analysis


## Contributing

Feel free to submit issues or pull requests to improve the script.

## License

This project is for educational purposes. Please respect Reddit's terms of service and user privacy.


