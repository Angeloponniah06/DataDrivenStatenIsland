from flask import Flask, render_template, request, jsonify
import json
import os
import sqlite3
import requests
from datetime import datetime

app = Flask(__name__)

# FRED API Configuration
FRED_API_KEY = '3cddf79d5604a832019162f50334e76a'
FRED_BASE_URL = 'https://api.stlouisfed.org/fred/series/observations'

# Database configuration
DATABASE = 'data.db'

def get_db():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

def init_db():
    """Initialize the database with business and employment data"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Create business_data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS business_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER NOT NULL,
            new_businesses INTEGER NOT NULL,
            closed_businesses INTEGER NOT NULL,
            net_change INTEGER NOT NULL
        )
    ''')
    
    # Create employment_data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employment_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER NOT NULL,
            unemployment_rate REAL NOT NULL,
            employment_rate REAL NOT NULL
        )
    ''')
    
    # Check if business data already exists
    cursor.execute('SELECT COUNT(*) FROM business_data')
    count = cursor.fetchone()[0]
    
    # If no data exists, load from JSON file
    if count == 0:
        data_path = os.path.join(app.root_path, "business_data.json")
        try:
            with open(data_path, "r") as f:
                data = json.load(f)
            
            # Insert data from JSON
            for entry in data.get('series', []):
                cursor.execute('''
                    INSERT INTO business_data (year, new_businesses, closed_businesses, net_change)
                    VALUES (?, ?, ?, ?)
                ''', (entry['year'], entry['new_businesses'], entry['closed_businesses'], entry['net_change']))
            
            conn.commit()
            print("Database initialized with business data from JSON")
        except Exception as e:
            print(f"Error initializing business database: {e}")
    
    # Check if employment data already exists
    cursor.execute('SELECT COUNT(*) FROM employment_data')
    count = cursor.fetchone()[0]
    
    # If no data exists, fetch from FRED API
    if count == 0:
        try:
            # Fetch unemployment rate data from FRED API
            params = {
                'series_id': 'NYRICH5URN',
                'api_key': FRED_API_KEY,
                'file_type': 'json',
                'observation_start': '2014-01-01',
                'observation_end': '2025-12-31'
            }
            
            response = requests.get(FRED_BASE_URL, params=params)
            response.raise_for_status()
            fred_data = response.json()
            
            # Process FRED data: aggregate by year (take annual average)
            yearly_data = {}
            for observation in fred_data.get('observations', []):
                if observation['value'] != '.':  # Skip missing values
                    date = datetime.strptime(observation['date'], '%Y-%m-%d')
                    year = date.year
                    unemployment_rate = float(observation['value'])
                    
                    if year not in yearly_data:
                        yearly_data[year] = []
                    yearly_data[year].append(unemployment_rate)
            
            # Calculate annual averages and insert into database
            for year in sorted(yearly_data.keys()):
                avg_unemployment = round(sum(yearly_data[year]) / len(yearly_data[year]), 1)
                avg_employment = round(100 - avg_unemployment, 1)
                
                cursor.execute('''
                    INSERT INTO employment_data (year, unemployment_rate, employment_rate)
                    VALUES (?, ?, ?)
                ''', (year, avg_unemployment, avg_employment))
            
            conn.commit()
            print(f"Database initialized with employment data from FRED API for {len(yearly_data)} years")
        except Exception as e:
            print(f"Error fetching data from FRED API: {e}")
            print("Falling back to JSON file...")
            # Fallback to JSON file if API fails
            data_path = os.path.join(app.root_path, "employment_data.json")
            try:
                with open(data_path, "r") as f:
                    data = json.load(f)
                
                for entry in data.get('series', []):
                    cursor.execute('''
                        INSERT INTO employment_data (year, unemployment_rate, employment_rate)
                        VALUES (?, ?, ?)
                    ''', (entry['year'], entry['unemployment_rate'], entry['employment_rate']))
                
                conn.commit()
                print("Database initialized with employment data from JSON fallback")
            except Exception as json_error:
                print(f"Error loading JSON fallback: {json_error}")
    
    conn.close()

# Initialize database on startup
init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/resources")
def resources():
    return render_template("resources.html")

@app.route("/apply")
def apply():
    job_id = request.args.get("job", "")
    return render_template("apply.html", job_id=job_id)
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/api/employment")
def api_employment():
    """
    Returns a simple time series of employment/unemployment rates
    for Staten Island from the database.
    Supports optional query parameters: start_year, end_year
    """
    try:
        # Get optional date range parameters
        start_year = request.args.get('start_year', type=int)
        end_year = request.args.get('end_year', type=int)
        
        print(f"DEBUG: start_year={start_year}, end_year={end_year}")  # Debug
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Build query with optional date filtering
        query = 'SELECT year, unemployment_rate, employment_rate FROM employment_data WHERE 1=1'
        params = []
        
        if start_year:
            query += ' AND year >= ?'
            params.append(start_year)
        if end_year:
            query += ' AND year <= ?'
            params.append(end_year)
        
        query += ' ORDER BY year'
        
        print(f"DEBUG: SQL query={query}, params={params}")  # Debug
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        print(f"DEBUG: Rows returned={len(rows)}")  # Debug
        
        # Convert rows to list of dictionaries
        series = []
        for row in rows:
            series.append({
                'year': row['year'],
                'unemployment_rate': row['unemployment_rate'],
                'employment_rate': row['employment_rate']
            })
        
        # Build response similar to original JSON structure
        response_data = {
            'area': 'Staten Island (Richmond County, NY)',
            'series': series,
            'source_notes': 'Unemployment rates for Richmond County (Staten Island) from FRED API (NYRICH5URN). Employment rate calculated as 100 minus unemployment rate.'
        }
        
        return jsonify(response_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/api/business")
def api_business():
    """
    Returns a simple time series of business openings/closures
    for Staten Island from the database.
    Supports optional query parameters: start_year, end_year
    """
    try:
        # Get optional date range parameters
        start_year = request.args.get('start_year', type=int)
        end_year = request.args.get('end_year', type=int)
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Build query with optional date filtering
        query = 'SELECT year, new_businesses, closed_businesses, net_change FROM business_data WHERE 1=1'
        params = []
        
        if start_year:
            query += ' AND year >= ?'
            params.append(start_year)
        if end_year:
            query += ' AND year <= ?'
            params.append(end_year)
        
        query += ' ORDER BY year'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        # Convert rows to list of dictionaries
        series = []
        for row in rows:
            series.append({
                'year': row['year'],
                'new_businesses': row['new_businesses'],
                'closed_businesses': row['closed_businesses'],
                'net_change': row['net_change']
            })
        
        # Build response similar to original JSON structure
        response_data = {
            'area': 'Staten Island (Richmond County, NY)',
            'series': series,
            'source_notes': 'Business data retrieved from database'
        }
        
        return jsonify(response_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # For local development
    app.run(host='0.0.0.0', port=8000, debug=True)
    
    # For production (AWS Lightsail), use:
    # app.run(host='0.0.0.0', port=8000)

