from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

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
    for Staten Island from a local JSON file.
    """
    data_path = os.path.join(app.root_path, "employment_data.json")
    try:
        with open(data_path, "r") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/api/business")
def api_business():
    """
    Returns a simple time series of business openings/closures
    for Staten Island from a local JSON file.
    """
    data_path = os.path.join(app.root_path, "business_data.json")
    try:
        with open(data_path, "r") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # For production (AWS Lightsail)
    app.run(host='0.0.0.0', port=8000)
    
    # For local development, comment out the line above and uncomment this:
    # app.run(debug=True)

