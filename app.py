from flask import Flask, render_template, request, jsonify
import json
import os
import sqlite3

app = Flask(__name__)

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
    
    # If no data exists, load from JSON file
    if count == 0:
        data_path = os.path.join(app.root_path, "employment_data.json")
        try:
            with open(data_path, "r") as f:
                data = json.load(f)
            
            # Insert data from JSON
            for entry in data.get('series', []):
                cursor.execute('''
                    INSERT INTO employment_data (year, unemployment_rate, employment_rate)
                    VALUES (?, ?, ?)
                ''', (entry['year'], entry['unemployment_rate'], entry['employment_rate']))
            
            conn.commit()
            print("Database initialized with employment data from JSON")
        except Exception as e:
            print(f"Error initializing employment database: {e}")
    
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
    """
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Query all employment data ordered by year
        cursor.execute('''
            SELECT year, unemployment_rate, employment_rate
            FROM employment_data
            ORDER BY year
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
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
            'source_notes': 'Employment data retrieved from database'
        }
        
        return jsonify(response_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/api/business")
def api_business():
    """
    Returns a simple time series of business openings/closures
    for Staten Island from the database.
    """
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Query all business data ordered by year
        cursor.execute('''
            SELECT year, new_businesses, closed_businesses, net_change
            FROM business_data
            ORDER BY year
        ''')
        
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
    # For production (AWS Lightsail)
    app.run(host='0.0.0.0', port=8000)
    
    # For local development, comment out the line above and uncomment this:
    # app.run(debug=True)

