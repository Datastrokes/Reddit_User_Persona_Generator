#!/usr/bin/env python3
"""
Reddit User Persona Generator
Scrapes a Reddit user's posts and comments to generate a detailed persona.
"""

import argparse
import re
import json
import os
import sys
from datetime import datetime
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import ollama

class RedditPersonaGenerator:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def extract_username_from_url(self, url):
        """Extract username from Reddit profile URL."""
        # Handle various Reddit URL formats
        patterns = [
            r'reddit\.com/user/([^/]+)',
            r'reddit\.com/u/([^/]+)',
            r'reddit\.com/user/([^/]+)/',
            r'reddit\.com/u/([^/]+)/'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        raise ValueError(f"Could not extract username from URL: {url}")
    
    def scrape_user_data(self, username):
        """Scrape user's posts and comments from Reddit."""
        print(f"Scraping data for user: {username}")
        
        # Reddit JSON endpoints
        user_url = f"https://www.reddit.com/user/{username}/"
        posts_url = f"https://www.reddit.com/user/{username}/submitted/.json"
        comments_url = f"https://www.reddit.com/user/{username}/comments/.json"
        
        user_data = {
            'username': username,
            'posts': [],
            'comments': [],
            'profile_info': {}
        }
        
        try:
            # Get user profile info
            response = self.session.get(user_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract basic profile info
                user_data['profile_info'] = {
                    'karma': self._extract_karma(soup),
                    'account_age': self._extract_account_age(soup),
                    'trophies': self._extract_trophies(soup)
                }
            
            # Get posts
            posts_response = self.session.get(posts_url)
            if posts_response.status_code == 200:
                posts_data = posts_response.json()
                user_data['posts'] = self._extract_posts(posts_data)
            
            # Get comments
            comments_response = self.session.get(comments_url)
            if comments_response.status_code == 200:
                comments_data = comments_response.json()
                user_data['comments'] = self._extract_comments(comments_data)
            
            print(f"Found {len(user_data['posts'])} posts and {len(user_data['comments'])} comments")
            return user_data
            
        except Exception as e:
            print(f"Error scraping data: {e}")
            return user_data
    
    def _extract_karma(self, soup):
        """Extract karma from profile page."""
        try:
            karma_elem = soup.find('span', {'class': 'karma'})
            if karma_elem:
                return karma_elem.text.strip()
        except:
            pass
        return "Unknown"
    
    def _extract_account_age(self, soup):
        """Extract account age from profile page."""
        try:
            # Look for account age information
            age_elem = soup.find('span', string=re.compile(r'redditor for'))
            if age_elem:
                return age_elem.text.strip()
        except:
            pass
        return "Unknown"
    
    def _extract_trophies(self, soup):
        """Extract trophies from profile page."""
        try:
            trophy_elems = soup.find_all('span', {'class': 'trophy'})
            return [trophy.text.strip() for trophy in trophy_elems]
        except:
            pass
        return []
    
    def _extract_posts(self, data):
        """Extract posts from Reddit JSON response."""
        posts = []
        if 'data' in data and 'children' in data['data']:
            for child in data['data']['children']:
                if 'data' in child:
                    post_data = child['data']
                    posts.append({
                        'title': post_data.get('title', ''),
                        'content': post_data.get('selftext', ''),
                        'subreddit': post_data.get('subreddit', ''),
                        'score': post_data.get('score', 0),
                        'created_utc': post_data.get('created_utc', 0),
                        'url': f"https://reddit.com{post_data.get('permalink', '')}",
                        'type': 'post'
                    })
        return posts
    
    def _extract_comments(self, data):
        """Extract comments from Reddit JSON response."""
        comments = []
        if 'data' in data and 'children' in data['data']:
            for child in data['data']['children']:
                if 'data' in child:
                    comment_data = child['data']
                    comments.append({
                        'content': comment_data.get('body', ''),
                        'subreddit': comment_data.get('subreddit', ''),
                        'score': comment_data.get('score', 0),
                        'created_utc': comment_data.get('created_utc', 0),
                        'url': f"https://reddit.com{comment_data.get('permalink', '')}",
                        'type': 'comment'
                    })
        return comments
    
    def generate_persona(self, user_data, model='llama3.2'):
        """Generate user persona using Ollama/Llama."""
        print(f"Generating persona using Llama model ({model})...")
        
        # Prepare data for LLM
        username = user_data['username']
        posts = user_data['posts'][:20]  # Limit to recent posts
        comments = user_data['comments'][:30]  # Limit to recent comments
        profile_info = user_data['profile_info']
        
        # Create context for LLM
        context = f"""
            Reddit User: {username}
            Profile Info: {json.dumps(profile_info, indent=2)}

            Recent Posts ({len(posts)}):
            """
        for i, post in enumerate(posts, 1):
            context += f"""
            {i}. Title: {post['title']}
            Subreddit: r/{post['subreddit']}
            Content: {post['content'][:500]}{'...' if len(post['content']) > 500 else ''}
            Score: {post['score']}
            URL: {post['url']}
            """

        context += f"""
            Recent Comments ({len(comments)}):
            """
        for i, comment in enumerate(comments, 1):
            context += f"""
            {i}. Subreddit: r/{comment['subreddit']}
            Content: {comment['content'][:300]}{'...' if len(comment['content']) > 300 else ''}
            Score: {comment['score']}
            URL: {comment['url']}
            """

        # LLM prompt
        prompt = f"""
            Based on the following Reddit user data, create a detailed user persona. 
            Analyze their posts, comments, subreddits they frequent, writing style, interests, and behavior patterns.

            {context}

            Please create a comprehensive user persona that includes:

            1. **Demographics & Background**: Age range, likely location, profession hints
            2. **Interests & Hobbies**: Main topics they discuss, subreddits they frequent
            3. **Personality Traits**: Communication style, attitude, values
            4. **Technical Knowledge**: Level of expertise in various topics
            5. **Online Behavior**: How they interact, posting frequency, engagement style
            6. **Values & Beliefs**: Political views, ethical stances, priorities
            7. **Communication Style**: Writing tone, vocabulary, formality level

            For each characteristic, provide specific citations from their posts/comments (use the numbered references above).

            Format the output as a structured persona with clear sections and citations.
            """

        try:
            # Use Ollama to generate persona
            response = ollama.chat(model=model, messages=[
                {
                    'role': 'user',
                    'content': prompt
                }
            ])
            
            return response['message']['content']
            
        except Exception as e:
            print(f"Error generating persona with Ollama: {e}")
            return f"Error generating persona: {e}"
    
    def save_persona(self, username, persona_content):
        """Save persona to a text file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{username}_persona.txt"
        
        # Create sample_outputs directory if it doesn't exist
        os.makedirs('sample_outputs', exist_ok=True)
        
        filepath = os.path.join('sample_outputs', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Reddit User Persona Analysis\n")
            f.write(f"Username: {username}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*50}\n\n")
            f.write(persona_content)
        
        print(f"Persona saved to: {filepath}")
        return filepath

def main():
    parser = argparse.ArgumentParser(description='Generate Reddit user persona')
    parser.add_argument('url', help='Reddit user profile URL')
    parser.add_argument('--model', default='llama3.2', help='Ollama model to use (default: llama3.2)')
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = RedditPersonaGenerator()
    
    try:
        # Extract username from URL
        username = generator.extract_username_from_url(args.url)
        print(f"Processing user: {username}")
        
        # Scrape user data
        user_data = generator.scrape_user_data(username)
        
        if not user_data['posts'] and not user_data['comments']:
            print("No posts or comments found. The user might be private or have no activity.")
            return
        
        # Generate persona
        persona_content = generator.generate_persona(user_data, model=args.model)
        
        # Save persona
        output_file = generator.save_persona(username, persona_content)
        
        print(f"\nPersona generation complete!")
        print(f"Output file: {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 