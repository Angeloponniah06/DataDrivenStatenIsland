# AWS Lightsail Deployment Guide

## Quick Deploy Steps

### 1. Create Lightsail Instance
- Choose **Ubuntu 24.04 LTS**
- Select **$3.50/month** plan (sufficient for this app)
- Create the instance

### 2. Upload Your Files

First, download your SSH key from Lightsail console and note your instance's public IP.

**Option A: Using FileZilla or WinSCP (Easiest - GUI)**

**FileZilla** (cross-platform):
1. Download [FileZilla](https://filezilla-project.org/)
2. Go to Edit → Settings → SFTP → Add key file (select your `.pem` file)
3. Connect: Host: `sftp://YOUR_LIGHTSAIL_IP`, Username: `ubuntu`, Port: 22
4. Navigate to `/home/ubuntu/` and create folder `myapp`
5. Drag and drop all files from left (local) to right (server)

**WinSCP** (Windows only):
1. Download [WinSCP](https://winscp.net/)
2. Connect using: Protocol: SFTP, Host: Your Lightsail IP, Username: `ubuntu`, Private key: Your `.pem` file
3. Navigate to `/home/ubuntu/` and create folder `myapp`
4. Drag and drop all files into `myapp`

Files to upload:
- `app.py`
- `requirements.txt`
- `business_data.json`
- `employment_data.json`
- `templates/` folder (entire folder with all HTML files)

**Option B: Using SCP from Command Line**
```bash
# From your local machine (in PowerShell/CMD)
cd C:\code\data_driven_staten_island

# Create the directory on server first
ssh -i path\to\your-key.pem ubuntu@YOUR_LIGHTSAIL_IP "mkdir -p /home/ubuntu/myapp"

# Upload files
scp -i path\to\your-key.pem app.py requirements.txt *.json ubuntu@YOUR_LIGHTSAIL_IP:/home/ubuntu/myapp/
scp -i path\to\your-key.pem -r templates ubuntu@YOUR_LIGHTSAIL_IP:/home/ubuntu/myapp/
```

**Option C: Clone from Git (if you have a repo)**
```bash
# SSH into your instance first
ssh -i path\to\your-key.pem ubuntu@YOUR_LIGHTSAIL_IP

# Then clone
cd /home/ubuntu
git clone https://github.com/yourusername/yourrepo.git myapp
cd myapp
```

### 3. Install Dependencies
```bash
sudo apt update
sudo apt install -y python3-pip python3-venv

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Open Firewall Ports

Before running the app, configure Lightsail firewall:

1. Go to your Lightsail instance page
2. Click the **Networking** tab
3. Scroll down to **IPv4 Firewall**
4. Click **+ Add rule**
5. Configure:
   - **Application**: Custom
   - **Protocol**: TCP
   - **Port**: 8000 (or 80 for production)
   - Click **Create**

Default rules already allow SSH (22) and HTTP (80). Add custom port 8000 only for testing.

### 5. Run the Application

**Option A: Quick test (port 8000)**
```bash
source venv/bin/activate
gunicorn --bind 0.0.0.0:8000 --workers 2 app:app
```
Visit: `http://YOUR_LIGHTSAIL_IP:8000/`

**Option B: Production (port 80)**
```bash
chmod +x start.sh
sudo venv/bin/gunicorn --bind 0.0.0.0:80 --workers 2 app:app
```
Visit: `http://YOUR_LIGHTSAIL_IP/` (no port needed)

**Note:** Port 80 requires sudo. Make sure:
- Port 80 is open in Lightsail firewall (usually open by default)
- You see "Listening at: http://0.0.0.0:80" in the output
- No errors appear in the terminal

### 5. Keep It Running (Optional)
To keep the app running after you disconnect, use systemd:

Create `/etc/systemd/system/myapp.service`:
```ini
[Unit]
Description=Data Driven Staten Island
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/myapp
Environment="PATH=/home/ubuntu/myapp/venv/bin"
ExecStart=/home/ubuntu/myapp/venv/bin/gunicorn --bind 0.0.0.0:80 --workers 2 app:app

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable myapp
sudo systemctl start myapp
```

### 6. Access Your App
Visit: `http://YOUR_LIGHTSAIL_IP/`

---

## Local Development
To test locally, edit `app.py`:
- Comment out: `app.run(host='0.0.0.0', port=8000)`
- Uncomment: `app.run(debug=True)`

Then run: `python app.py`
