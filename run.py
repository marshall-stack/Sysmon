from flask import Flask, jsonify, render_template
import psutil

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats')
def stats():
    # Get the system stats
    data = {
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
    }

    # Get the list of running processes sorted by CPU usage
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Sort processes by CPU usage in descending order
    processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)

    # Add top 10 processes to the data
    data["processes"] = processes[:10]

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
