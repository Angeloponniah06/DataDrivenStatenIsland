import sqlite3
import requests

# Check database contents
print("=" * 60)
print("CHECKING DATABASE...")
print("=" * 60)

try:
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    # Check employment data
    cursor.execute('SELECT COUNT(*) FROM employment_data')
    emp_count = cursor.fetchone()[0]
    print(f"\n✓ Employment records in database: {emp_count}")
    
    if emp_count > 0:
        cursor.execute('SELECT * FROM employment_data ORDER BY year LIMIT 5')
        print("\nSample employment data:")
        for row in cursor.fetchall():
            print(f"  Year: {row[1]}, Unemployment: {row[2]}%, Employment: {row[3]}%")
    else:
        print("⚠ No employment data found in database!")
    
    # Check business data
    cursor.execute('SELECT COUNT(*) FROM business_data')
    biz_count = cursor.fetchone()[0]
    print(f"\n✓ Business records in database: {biz_count}")
    
    if biz_count > 0:
        cursor.execute('SELECT * FROM business_data ORDER BY year LIMIT 5')
        print("\nSample business data:")
        for row in cursor.fetchall():
            print(f"  Year: {row[1]}, New: {row[2]}, Closed: {row[3]}, Net: {row[4]}")
    else:
        print("⚠ No business data found in database!")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Error checking database: {e}")

print("\n" + "=" * 60)
print("TESTING API ENDPOINTS...")
print("=" * 60)

# Test if Flask is running
try:
    response = requests.get('http://localhost:8000/api/employment?start_year=2019&end_year=2024', timeout=3)
    if response.status_code == 200:
        data = response.json()
        print(f"\n✓ Employment API returned {len(data.get('series', []))} records")
        if data.get('series'):
            print(f"  Sample: {data['series'][0]}")
    else:
        print(f"❌ Employment API returned status code: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("❌ Flask server not running on localhost:8000")
except Exception as e:
    print(f"❌ Error testing API: {e}")

print("\n" + "=" * 60)
