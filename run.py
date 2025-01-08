from flask import Flask, jsonify, render_template
import psutil

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats')
def stats():
    # Get CPU temperatures
    try:
        temps = psutil.sensors_temperatures()
        cpu_temp = temps['coretemp'][0].current if 'coretemp' in temps else None
    except AttributeError:
        cpu_temp = None

    # Get fan speeds
    try:
        fans = psutil.sensors_fans()
        fan_speed = fans['fan'][0].current if 'fan' in fans else None
    except AttributeError:
        fan_speed = None

    data = {
        "cpu": psutil.cpu_percent(interval=1, percpu=True),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "cpu_temp": cpu_temp,
        "fan_speed": fan_speed,
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

