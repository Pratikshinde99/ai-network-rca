"""
Azure Function App - Network RCA Platform
Main entry point for HTTP-triggered diagnostics
"""

import azure.functions as func
import logging
import json
import os
from datetime import datetime

from diagnostics import NetworkDiagnostics
from ai_analyzer import AIAnalyzer
from rca_generator import RCAGenerator

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="diagnose", methods=["POST"])
def diagnose(req: func.HttpRequest) -> func.HttpResponse:
    """
    Main diagnostic endpoint
    Accepts: { "target": "domain.com", "service_type": "web" }
    Returns: Full diagnostic results + AI RCA
    """
    logging.info('Network RCA diagnostic request received')
    
    try:
        # Parse request
        req_body = req.get_json()
        target = req_body.get('target')
        service_type = req_body.get('service_type', 'web')
        
        # ENTERPRISE FEATURE 1: Incident Context Awareness
        incident_context = {
            'incident_start_time': req_body.get('incident_start_time'),
            'incident_detection_type': req_body.get('incident_detection_type', 'User-Reported'),
            'affected_users_count': req_body.get('affected_users_count', 0),
            'business_criticality': req_body.get('business_criticality', 'Medium')
        }
        
        # ENTERPRISE FEATURE 2: Change Awareness
        recent_changes = {
            'recent_firewall_change': req_body.get('recent_firewall_change', False),
            'recent_dns_change': req_body.get('recent_dns_change', False),
            'recent_deployment': req_body.get('recent_deployment', False)
        }
        
        if not target:
            return func.HttpResponse(
                json.dumps({"error": "Missing 'target' parameter"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Clean target (remove protocol if present)
        target = target.replace('http://', '').replace('https://', '').strip()
        
        logging.info(f'Running diagnostics for target: {target}')
        logging.info(f'Incident context: {incident_context}')
        logging.info(f'Recent changes: {recent_changes}')
        
        # Step 1: Run network diagnostics
        diagnostics = NetworkDiagnostics(target, service_type)
        diagnostic_results = diagnostics.run_all_diagnostics()
        
        # Step 2: AI Root Cause Analysis (with enterprise context)
        ai_analyzer = AIAnalyzer()
        ai_analysis = ai_analyzer.analyze_diagnostics(
            target, 
            diagnostic_results,
            incident_context=incident_context,
            recent_changes=recent_changes
        )
        
        # Step 3: Generate RCA Report (dual output)
        rca_generator = RCAGenerator()
        
        # Generate both human and machine-readable reports
        executive_report = rca_generator.generate_executive_report(
            target=target,
            diagnostics=diagnostic_results,
            ai_analysis=ai_analysis,
            incident_context=incident_context,
            recent_changes=recent_changes
        )
        
        technical_report_json = rca_generator.generate_technical_report(
            target=target,
            diagnostics=diagnostic_results,
            ai_analysis=ai_analysis,
            incident_context=incident_context,
            recent_changes=recent_changes
        )
        
        # Legacy text report (for backward compatibility)
        rca_report = rca_generator.generate_report(
            target=target,
            diagnostics=diagnostic_results,
            ai_analysis=ai_analysis,
            incident_context=incident_context,
            recent_changes=recent_changes
        )
        
        # Step 4: Store reports in Blob Storage
        report_url = rca_generator.save_to_blob(rca_report, target)
        executive_url = rca_generator.save_to_blob(executive_report, target, suffix='_executive')
        technical_url = rca_generator.save_technical_json_to_blob(technical_report_json, target)
        
        # Prepare response
        response = {
            "target": target,
            "timestamp": datetime.utcnow().isoformat(),
            "diagnostics": diagnostic_results,
            "ai_analysis": ai_analysis,
            "incident_context": incident_context,
            "recent_changes": recent_changes,
            "rca_report": rca_report,
            "executive_report": executive_report,
            "technical_report": technical_report_json,
            "report_urls": {
                "technical_text": report_url,
                "executive_summary": executive_url,
                "machine_readable_json": technical_url
            },
            "status": "success"
        }
        
        logging.info(f'Diagnostics completed successfully for {target}')
        
        return func.HttpResponse(
            json.dumps(response, indent=2),
            status_code=200,
            mimetype="application/json",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            }
        )
        
    except ValueError as e:
        logging.error(f'Validation error: {str(e)}')
        return func.HttpResponse(
            json.dumps({"error": str(e), "status": "validation_error"}),
            status_code=400,
            mimetype="application/json"
        )
    
    except Exception as e:
        logging.error(f'Unexpected error: {str(e)}', exc_info=True)
        return func.HttpResponse(
            json.dumps({
                "error": "Internal server error",
                "details": str(e),
                "status": "error"
            }),
            status_code=500,
            mimetype="application/json"
        )


@app.route(route="health", methods=["GET"])
def health_check(req: func.HttpRequest) -> func.HttpResponse:
    """Health check endpoint"""
    return func.HttpResponse(
        json.dumps({
            "status": "healthy",
            "service": "Network RCA Platform",
            "timestamp": datetime.utcnow().isoformat()
        }),
        status_code=200,
        mimetype="application/json"
    )
