from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Ensure data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

DATA_FILE = 'data/agents.json'

def load_agents():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_agents(agents):
    with open(DATA_FILE, 'w') as f:
        json.dump(agents, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/save-agent', methods=['POST'])
def save_agent():
    try:
        agent_data = request.json
        agent_data['timestamp'] = datetime.now().isoformat()
        
        agents = load_agents()
        agents.append(agent_data)
        save_agents(agents)
        
        return jsonify({"status": "success", "message": "Agent data saved successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/agents', methods=['GET'])
def get_agents():
    try:
        agents = load_agents()
        return jsonify(agents)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
