"""
RCA Report Generator
Generates formal Root Cause Analysis reports and stores in Azure Blob Storage
ENTERPRISE ENHANCED: Dual output (Executive + Technical JSON)
"""

import os
import json
from datetime import datetime
from typing import Dict, List
import logging
from azure.storage.blob import BlobServiceClient, ContentSettings

class RCAGenerator:
    def __init__(self):
        self.connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        self.container_name = os.getenv("BLOB_CONTAINER_NAME", "rca-reports")
        
        if self.connection_string:
            try:
                self.blob_service_client = BlobServiceClient.from_connection_string(
                    self.connection_string
                )
                self._ensure_container_exists()
            except Exception as e:
                logging.warning(f"Blob storage not configured: {str(e)}")
                self.blob_service_client = None
        else:
            logging.warning("Azure Storage connection string not configured")
            self.blob_service_client = None
    
    def _ensure_container_exists(self):
        """Create container if it doesn't exist"""
        try:
            container_client = self.blob_service_client.get_container_client(
                self.container_name
            )
            if not container_client.exists():
                container_client.create_container()
                logging.info(f"Created blob container: {self.container_name}")
        except Exception as e:
            logging.error(f"Error creating container: {str(e)}")
    
    def generate_report(self, target: str, diagnostics: List[Dict], 
                       ai_analysis: Dict, incident_context: Dict = None,
                       recent_changes: Dict = None) -> str:
        """
        Generate formal RCA report in text format
        ENTERPRISE ENHANCED: Includes incident context and change awareness
        """
        timestamp = datetime.utcnow()
        
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("ROOT CAUSE ANALYSIS REPORT")
        report_lines.append("=" * 80)
        report_lines.append("")
        
        # Header
        report_lines.append(f"Target:           {target}")
        report_lines.append(f"Analysis Date:    {timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        report_lines.append(f"Severity:         {ai_analysis.get('severity', 'UNKNOWN')}")
        report_lines.append(f"Category:         {ai_analysis.get('category', 'UNKNOWN')}")
        report_lines.append("")
        
        # Executive Summary
        report_lines.append("-" * 80)
        report_lines.append("EXECUTIVE SUMMARY")
        report_lines.append("-" * 80)
        report_lines.append("")
        report_lines.append(f"Root Cause: {ai_analysis.get('root_cause', 'Unknown')}")
        report_lines.append(f"Confidence: {ai_analysis.get('confidence_percentage', 0)}%")
        report_lines.append("")
        
        # Diagnostic Results
        report_lines.append("-" * 80)
        report_lines.append("DIAGNOSTIC TEST RESULTS")
        report_lines.append("-" * 80)
        report_lines.append("")
        
        for test in diagnostics:
            status_symbol = "✓" if test["status"] == "PASS" else "✗"
            report_lines.append(f"{status_symbol} {test['test_name']}")
            report_lines.append(f"  Status:       {test['status']}")
            report_lines.append(f"  Latency:      {test['latency_ms']} ms")
            
            if test.get('failure_reason'):
                report_lines.append(f"  Failure:      {test['failure_reason']}")
            
            if test.get('details'):
                report_lines.append(f"  Details:      {json.dumps(test['details'])}")
            
            report_lines.append("")
        
        # Analysis & Reasoning
        report_lines.append("-" * 80)
        report_lines.append("ANALYSIS & REASONING")
        report_lines.append("-" * 80)
        report_lines.append("")
        report_lines.append(ai_analysis.get('reasoning', 'No reasoning provided'))
        report_lines.append("")
        
        # Evidence
        report_lines.append("-" * 80)
        report_lines.append("SUPPORTING EVIDENCE")
        report_lines.append("-" * 80)
        report_lines.append("")
        
        evidence = ai_analysis.get('evidence', [])
        for i, item in enumerate(evidence, 1):
            report_lines.append(f"{i}. {item}")
        
        if not evidence:
            report_lines.append("No specific evidence provided")
        
        report_lines.append("")
        
        # Remediation Steps
        report_lines.append("-" * 80)
        report_lines.append("RECOMMENDED REMEDIATION STEPS")
        report_lines.append("-" * 80)
        report_lines.append("")
        
        steps = ai_analysis.get('remediation_steps', [])
        for i, step in enumerate(steps, 1):
            report_lines.append(f"{i}. {step}")
        
        if not steps:
            report_lines.append("No remediation steps available")
        
        report_lines.append("")
        
        # Footer
        report_lines.append("=" * 80)
        report_lines.append("END OF REPORT")
        report_lines.append("=" * 80)
        report_lines.append("")
        report_lines.append("Generated by AI-Powered Network RCA Platform")
        report_lines.append("Powered by Azure Functions + Azure OpenAI")
        report_lines.append("")
        
        return "\n".join(report_lines)
    
    def generate_executive_report(self, target: str, diagnostics: List[Dict],
                                  ai_analysis: Dict, incident_context: Dict = None,
                                  recent_changes: Dict = None) -> str:
        """
        ENTERPRISE FEATURE 3: Generate Executive RCA (Human-Readable, Non-Technical)
        Suitable for managers and executives
        """
        timestamp = datetime.utcnow()
        
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("EXECUTIVE INCIDENT SUMMARY")
        report_lines.append("=" * 80)
        report_lines.append("")
        
        # Incident Overview
        report_lines.append(f"Service Affected:     {target}")
        report_lines.append(f"Report Generated:     {timestamp.strftime('%B %d, %Y at %H:%M UTC')}")
        
        if incident_context:
            if incident_context.get('incident_start_time'):
                report_lines.append(f"Incident Start Time:  {incident_context['incident_start_time']}")
            report_lines.append(f"Detection Method:     {incident_context.get('incident_detection_type', 'User-Reported')}")
            report_lines.append(f"Users Impacted:       {incident_context.get('affected_users_count', 'Unknown')}")
            report_lines.append(f"Business Priority:    {incident_context.get('business_criticality', 'Medium')}")
        
        report_lines.append("")
        
        # What Happened (Plain English)
        report_lines.append("-" * 80)
        report_lines.append("WHAT HAPPENED")
        report_lines.append("-" * 80)
        report_lines.append("")
        
        # Translate technical root cause to business language
        root_cause = ai_analysis.get('root_cause', 'Unknown issue')
        severity = ai_analysis.get('severity', 'MEDIUM')
        
        if severity in ['CRITICAL', 'HIGH']:
            impact_statement = "This is a high-priority issue requiring immediate attention."
        elif severity == 'MEDIUM':
            impact_statement = "This issue requires timely resolution to prevent service degradation."
        else:
            impact_statement = "This is a low-impact issue that should be addressed during regular maintenance."
        
        report_lines.append(f"The service '{target}' experienced an outage or degradation.")
        report_lines.append(f"Root Cause: {root_cause}")
        report_lines.append(f"Impact Level: {severity}")
        report_lines.append(impact_statement)
        report_lines.append("")
        
        # Why It Happened
        report_lines.append("-" * 80)
        report_lines.append("WHY IT HAPPENED")
        report_lines.append("-" * 80)
        report_lines.append("")
        
        # Simplify technical reasoning
        reasoning = ai_analysis.get('reasoning', '')
        report_lines.append(reasoning)
        report_lines.append("")
        
        # Recent Changes (if any)
        if recent_changes:
            changes_made = []
            if recent_changes.get('recent_firewall_change'):
                changes_made.append("Network firewall configuration")
            if recent_changes.get('recent_dns_change'):
                changes_made.append("DNS settings")
            if recent_changes.get('recent_deployment'):
                changes_made.append("Application deployment")
            
            if changes_made:
                report_lines.append("Recent Changes That May Be Related:")
                for change in changes_made:
                    report_lines.append(f"  • {change}")
                
                if ai_analysis.get('change_correlation'):
                    report_lines.append("")
                    report_lines.append(f"Analysis: {ai_analysis['change_correlation']}")
                
                report_lines.append("")
        
        # Who Is Responsible
        report_lines.append("-" * 80)
        report_lines.append("WHO SHOULD FIX THIS")
        report_lines.append("-" * 80)
        report_lines.append("")
        
        responsible_team = ai_analysis.get('responsible_team', 'Technical Team')
        root_cause_category = ai_analysis.get('root_cause_category', 'Network Issue')
        
        report_lines.append(f"Responsible Team:     {responsible_team}")
        report_lines.append(f"Issue Category:       {root_cause_category}")
        report_lines.append(f"Reason:               {ai_analysis.get('responsibility_reason', 'Based on diagnostic analysis')}")
        report_lines.append("")
        
        # Next Steps (Simplified)
        report_lines.append("-" * 80)
        report_lines.append("RECOMMENDED NEXT STEPS")
        report_lines.append("-" * 80)
        report_lines.append("")
        
        steps = ai_analysis.get('remediation_steps', [])
        if steps:
            report_lines.append("The technical team recommends:")
            for i, step in enumerate(steps[:3], 1):  # Top 3 steps only for executives
                report_lines.append(f"{i}. {step}")
        else:
            report_lines.append("Technical team to investigate and provide action plan.")
        
        report_lines.append("")
        
        # Confidence
        confidence = ai_analysis.get('confidence_percentage', 0)
        report_lines.append(f"Analysis Confidence:  {confidence}%")
        if confidence >= 80:
            report_lines.append("(High confidence - recommended to proceed with remediation)")
        elif confidence >= 60:
            report_lines.append("(Moderate confidence - may require additional investigation)")
        else:
            report_lines.append("(Low confidence - recommend manual investigation)")
        
        report_lines.append("")
        
        # Footer
        report_lines.append("=" * 80)
        report_lines.append("END OF EXECUTIVE SUMMARY")
        report_lines.append("=" * 80)
        report_lines.append("")
        report_lines.append("For technical details, refer to the Technical RCA Report.")
        report_lines.append("")
        
        return "\n".join(report_lines)
    
    def generate_technical_report(self, target: str, diagnostics: List[Dict],
                                  ai_analysis: Dict, incident_context: Dict = None,
                                  recent_changes: Dict = None) -> Dict:
        """
        ENTERPRISE FEATURE 3: Generate Technical RCA (Machine-Readable JSON)
        Structured format for automation and integration
        """
        return {
            "report_version": "1.0",
            "report_type": "technical_rca",
            "generated_at": datetime.utcnow().isoformat(),
            
            # Incident Metadata
            "incident": {
                "target": target,
                "incident_context": incident_context or {},
                "recent_changes": recent_changes or {}
            },
            
            # Diagnostic Results
            "diagnostics": {
                "tests_run": len(diagnostics),
                "tests_passed": sum(1 for t in diagnostics if t["status"] == "PASS"),
                "tests_failed": sum(1 for t in diagnostics if t["status"] in ["FAIL", "INFERRED_FAIL"]),
                "results": diagnostics
            },
            
            # Root Cause Analysis
            "root_cause_analysis": {
                "root_cause": ai_analysis.get('root_cause', 'Unknown'),
                "confidence_percentage": ai_analysis.get('confidence_percentage', 0),
                "severity": ai_analysis.get('severity', 'UNKNOWN'),
                "category": ai_analysis.get('category', 'UNKNOWN'),
                
                # ENTERPRISE FEATURE 4: Responsibility Classification
                "root_cause_category": ai_analysis.get('root_cause_category', 'Network Issue'),
                "responsible_team": ai_analysis.get('responsible_team', 'Network Operations'),
                "responsibility_reason": ai_analysis.get('responsibility_reason', ''),
                
                # Change Correlation
                "change_correlation": ai_analysis.get('change_correlation'),
                
                # Analysis Details
                "reasoning": ai_analysis.get('reasoning', ''),
                "evidence": ai_analysis.get('evidence', []),
                "remediation_steps": ai_analysis.get('remediation_steps', [])
            },
            
            # Metadata
            "metadata": {
                "analysis_engine": "Azure OpenAI",
                "platform": "AI-Powered Network RCA",
                "version": "2.0-enterprise"
            }
        }
    
    def save_to_blob(self, report_content: str, target: str, suffix: str = "") -> str:
        """
        Save report to Azure Blob Storage
        ENTERPRISE ENHANCED: Supports multiple report types via suffix
        Returns URL to the report or None if storage not configured
        """
        if not self.blob_service_client:
            logging.warning("Blob storage not configured, skipping upload")
            return None
        
        try:
            # Generate blob name
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            safe_target = target.replace('/', '_').replace(':', '_')
            blob_name = f"rca_{safe_target}_{timestamp}{suffix}.txt"
            
            # Upload to blob
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )
            
            blob_client.upload_blob(
                report_content,
                overwrite=True,
                content_settings=ContentSettings(content_type='text/plain')
            )
            
            # Generate URL
            url = blob_client.url
            logging.info(f"Report saved to blob storage: {blob_name}")
            
            return url
        
        except Exception as e:
            logging.error(f"Failed to save report to blob: {str(e)}")
            return None
    
    def save_technical_json_to_blob(self, technical_report: Dict, target: str) -> str:
        """
        Save technical JSON report to Azure Blob Storage
        """
        if not self.blob_service_client:
            logging.warning("Blob storage not configured, skipping upload")
            return None
        
        try:
            # Generate blob name
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            safe_target = target.replace('/', '_').replace(':', '_')
            blob_name = f"rca_{safe_target}_{timestamp}_technical.json"
            
            # Upload to blob
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )
            
            blob_client.upload_blob(
                json.dumps(technical_report, indent=2),
                overwrite=True,
                content_settings=ContentSettings(content_type='application/json')
            )
            
            # Generate URL
            url = blob_client.url
            logging.info(f"Technical JSON report saved to blob storage: {blob_name}")
            
            return url
        
        except Exception as e:
            logging.error(f"Failed to save technical JSON to blob: {str(e)}")
            return None
    
    def generate_json_report(self, target: str, diagnostics: List[Dict], 
                            ai_analysis: Dict) -> Dict:
        """
        Generate RCA report in JSON format (for API responses)
        LEGACY METHOD - Kept for backward compatibility
        """
        return {
            "target": target,
            "timestamp": datetime.utcnow().isoformat(),
            "severity": ai_analysis.get('severity', 'UNKNOWN'),
            "category": ai_analysis.get('category', 'UNKNOWN'),
            "summary": {
                "root_cause": ai_analysis.get('root_cause', 'Unknown'),
                "confidence_percentage": ai_analysis.get('confidence_percentage', 0)
            },
            "diagnostics": diagnostics,
            "analysis": {
                "reasoning": ai_analysis.get('reasoning', ''),
                "evidence": ai_analysis.get('evidence', []),
                "remediation_steps": ai_analysis.get('remediation_steps', [])
            }
        }
