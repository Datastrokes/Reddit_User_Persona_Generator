#!/usr/bin/env python3
"""
Test script to verify Reddit Persona Generator setup
"""

import sys
import importlib

def test_imports():
    """Test if all required packages can be imported."""
    required_packages = [
        'requests',
        'bs4',
        'ollama',
        'lxml'
    ]
    
    print("Testing package imports...")
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✓ {package} imported successfully")
        except ImportError as e:
            print(f"✗ Failed to import {package}: {e}")
            return False
    return True

def test_ollama_connection():
    """Test if Ollama is running and accessible."""
    try:
        import ollama
        print("\nTesting Ollama connection...")
        
        # Test basic connection
        models = ollama.list()
        print(f"✓ Ollama is running")
        
        # Check available models
        if 'models' in models and models['models']:
            model_names = [model.get('name', '') for model in models['models']]
            print(f"  Available models: {model_names}")
            
            # Check if llama2 is available
            if 'llama2' in model_names:
                print("✓ llama2 model is available")
            else:
                print("⚠ llama2 model not found. You may need to run: ollama pull llama2")
        else:
            print("  No models found. You may need to run: ollama pull llama2")
            
        return True
        
    except Exception as e:
        print(f"✗ Ollama connection failed: {e}")
        print("  Make sure Ollama is installed and running:")
        print("  - Install: https://ollama.ai/")
        print("  - Start: ollama serve")
        return False

def test_reddit_access():
    """Test basic Reddit access."""
    try:
        import requests
        print("\nTesting Reddit access...")
        
        # Test basic Reddit access
        response = requests.get('https://www.reddit.com/user/kojied/.json', 
                              headers={'User-Agent': 'Mozilla/5.0'})
        
        if response.status_code == 200:
            print("✓ Reddit API access successful")
            return True
        else:
            print(f"⚠ Reddit API returned status {response.status_code}")
            return True  # Still usable, just might have rate limiting
            
    except Exception as e:
        print(f"✗ Reddit access test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Reddit Persona Generator - Setup Test")
    print("=" * 40)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test Ollama
    if not test_ollama_connection():
        all_passed = False
    
    # Test Reddit access
    if not test_reddit_access():
        all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("✓ All tests passed! You're ready to use the Reddit Persona Generator.")
        print("\nTry running:")
        print("python reddit_persona_generator.py \"https://www.reddit.com/user/kojied/\"")
    else:
        print("✗ Some tests failed. Please check the setup instructions in README.md")
        sys.exit(1)

if __name__ == "__main__":
    main() 