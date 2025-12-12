"""
Flask web application for the Data Communication simulation.
Serves a modern UI and provides API endpoint for running simulations.
"""
from flask import Flask, render_template, request, jsonify
from core_simulation import run_simulation

app = Flask(__name__)


@app.route('/')
def index():
    """Serve the main UI page."""
    return render_template('index.html')


@app.route('/run-simulation', methods=['POST'])
def run_simulation_endpoint():
    """
    API endpoint to run a simulation.
    
    Expected JSON payload:
        {"message": "your message here"}
    
    Returns JSON with simulation results.
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Missing 'message' field in request"}), 400
        
        message = data['message']
        
        if not isinstance(message, str):
            return jsonify({"error": "Message must be a string"}), 400
        
        # Run the simulation
        result = run_simulation(message)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("Starting Data Communication Simulation Web App...")
    print("Open your browser and navigate to: http://127.0.0.1:8080")
    app.run(host='127.0.0.1', port=8080, debug=True)

