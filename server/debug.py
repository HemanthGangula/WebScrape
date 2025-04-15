import os
import sys

print("=== Python Path Debug ===")
print(f"Current working directory: {os.getcwd()}")
print(f"Directory of this file: {os.path.dirname(os.path.abspath(__file__))}")
print(f"Parent directory: {os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}")

print("\n=== Directory Structure ===")
print(f"Contents of current directory: {os.listdir('.')}")
print(f"Contents of parent directory: {os.listdir('..')}")

try:
    print("\n=== Checking for scraper.js ===")
    potential_paths = [
        os.path.join(os.getcwd(), 'scraper', 'scrape.js'),
        os.path.join(os.getcwd(), '..', 'scraper', 'scrape.js'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scraper', 'scrape.js'),
        '/app/scraper/scrape.js'
    ]
    
    for path in potential_paths:
        exists = os.path.exists(path)
        print(f"Path {path}: {'EXISTS' if exists else 'NOT FOUND'}")
        
except Exception as e:
    print(f"Error during path check: {str(e)}")
