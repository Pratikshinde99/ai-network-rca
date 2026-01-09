"""
Simple Flask API for local testing
Run this instead of Azure Functions for local development
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from diagnostics import NetworkDiagnostics
from ai_analyzer import AIAnalyzer
from rca_generator import RCAGenerator

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/diagnose', methods=['POST'])
def diagnose():
    try:
        data = request.get_json()
        target = data.get('target')
        service_type = data.get('service_type', 'web')
        
        # Get optional enterprise context
        incident_context = data.get('incident_context')
        recent_changes = data.get('recent_changes')
        
        print(f"Running diagnostics for: {target}")
        
        # Run diagnostics
        diag = NetworkDiagnostics(target, service_type)
        diagnostics = diag.run_all_diagnostics()
        
        # AI Analysis
        analyzer = AIAnalyzer()
        ai_analysis = analyzer.analyze_diagnostics(target, diagnostics, incident_context, recent_changes)
        
        # Generate reports
        generator = RCAGenerator()
        reports = generator.generate_all_reports(target, diagnostics, ai_analysis, incident_context, recent_changes)
        
        # Build response
        response = {
            "target": target,
            "timestamp": diagnostics[0].get('timestamp', ''),
            "diagnostics": diagnostics,
            "ai_analysis": ai_analysis,
            "technical_report": reports['technical'],
            "executive_report": reports['executive'],
            "json_report": reports['json']
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Flask API on http://localhost:7071")
    print("📡 API endpoint: http://localhost:7071/api/diagnose")
    print("Press Ctrl+C to stop")
    app.run(host='0.0.0.0', port=7071, debug=True)
