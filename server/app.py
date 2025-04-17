from flask import Flask, Response
import json
import os
import subprocess
import time

app = Flask(__name__)

cached_data = None
last_scrape_time = 0
CACHE_LIFETIME = 3600  

def get_scraped_data():
    global cached_data, last_scrape_time
    current_time = time.time()
    
    if cached_data is None or current_time - last_scrape_time > CACHE_LIFETIME:
        try:
            json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scraped_data.json')
            
            if os.path.exists(json_path):
                with open(json_path, 'r') as f:
                    cached_data = json.load(f)
                    last_scrape_time = current_time
            else:
                run_scraper()
                
        except Exception as e:
            print(f"Error reading cached data: {e}")
            run_scraper()
    
    return cached_data or {"error": "No data available"}

def run_scraper():
    global cached_data, last_scrape_time
    
    url = os.environ.get('SCRAPE_URL', 'https://example.com')
    
    try:
        scraper_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scraper', 'scrape.js'))
        working_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        process = subprocess.run(
            ['node', scraper_path], 
            env=dict(os.environ, SCRAPE_URL=url),
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            cwd=working_dir,
            text=True
        )
        
        if process.returncode != 0:
            return {"error": "Scraper failed", "message": process.stderr}
            
        json_path = os.path.join(working_dir, 'scraped_data.json')
        
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                cached_data = json.load(f)
                last_scrape_time = time.time()
                return cached_data
        
        parsed_path = os.path.join(working_dir, 'parsed_data.txt')
        if os.path.exists(parsed_path):
            with open(parsed_path, 'r') as f:
                content = f.read()
                if "JSON_START" in content and "JSON_END" in content:
                    json_text = content.split("JSON_START")[1].split("JSON_END")[0].strip()
                    try:
                        cached_data = json.loads(json_text)
                        last_scrape_time = time.time()
                        return cached_data
                    except:
                        pass
                
        return {"error": "Could not retrieve scraped data"}
        
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def index():
    data = get_scraped_data()
    return Response(
        json.dumps(data, indent=2),
        mimetype='application/json'
    )

@app.route('/api/data')
def get_data():
    data = get_scraped_data()
    return Response(
        json.dumps(data, indent=2),
        mimetype='application/json'
    )

@app.route('/refresh')
def refresh_data():
    data = run_scraper()
    return Response(
        json.dumps(data, indent=2),
        mimetype='application/json'
    )

if __name__ == '__main__':
    get_scraped_data()
    app.run(host='0.0.0.0', port=5000)
