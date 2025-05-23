from flask import Flask, render_template, request, jsonify
from scheduler import fcfs, sjf, priority, round_robin, srtf, multilevel_queue
from recommender import recommend

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    algo = data['algorithm']
    processes = data['processes']
    quantum = data.get('quantum', 2)

    if algo == "FCFS":
        result = fcfs(processes)
    elif algo == "SJF":
        result = sjf(processes)
    elif algo == "SRTF":
        result = srtf(processes)
    elif algo == "Priority":
        result = priority(processes)
    elif algo == "Round Robin":
        result = round_robin(processes, quantum)
    elif algo == "Multilevel Queue":
        result = multilevel_queue(processes, quantum)
    else:
        result = []

    return jsonify(result)

@app.route('/recommend', methods=['POST'])
def suggest():
    data = request.json
    suggestion = recommend(data['processes'])
    return jsonify({'suggested': suggestion})

@app.route('/gantt', methods=['POST'])
def gantt():
    schedule = request.json
    gantt_html = render_template('gantt_chart.html', schedule=schedule)
    return gantt_html

if __name__ == "__main__":
    app.run(debug=True)
