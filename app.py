from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from backend import fcfs, sjf, priority_scheduling, round_robin

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('frontend.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    num_cores = data['num_cores']
    processes = data['processes']
    quantum = data.get('quantum', 1)
    selected_algorithms = data['selected_algorithms']

    results = []

    if 'fcfs' in selected_algorithms:
        avg_waiting_time, avg_turnaround_time, order_of_execution = fcfs(processes)
        results.append(("First Come First Serve", avg_waiting_time, avg_turnaround_time, order_of_execution))

    if 'sjf' in selected_algorithms:
        avg_waiting_time, avg_turnaround_time, order_of_execution = sjf(processes)
        results.append(("Shortest Job First", avg_waiting_time, avg_turnaround_time, order_of_execution))

    if 'priority' in selected_algorithms:
        avg_waiting_time, avg_turnaround_time, order_of_execution = priority_scheduling(processes)
        results.append(("Priority Scheduling", avg_waiting_time, avg_turnaround_time, order_of_execution))

    if 'rr' in selected_algorithms:
        avg_waiting_time, avg_turnaround_time, order_of_execution = round_robin(processes, quantum)
        results.append(("Round Robin", avg_waiting_time, avg_turnaround_time, order_of_execution))

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)