"""
AI Analyzer Module
Uses Azure OpenAI to perform root cause analysis
"""

import os
import json
import logging
from openai import AzureOpenAI
from typing import Dict, List

class AIAnalyzer:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4")
        
        if not self.endpoint or not self.api_key:
            raise ValueError("Azure OpenAI credentials not configured")
        
        self.client = AzureOpenAI(
            azure_endpoint=self.endpoint,
            api_key=self.api_key,
            api_version="2024-02-15-preview"
        )
    
    def analyze_diagnostics(self, target: str, diagnostics: List[Dict], 
                           incident_context: Dict = None, recent_changes: Dict = None) -> Dict:
        """
        Analyze diagnostic results using Azure OpenAI
        ENTERPRISE ENHANCED: Includes incident context and change awareness
        Returns structured AI analysis with root cause and recommendations
        """
        logging.info(f"Starting AI analysis for {target}")
        
        # Build prompt with enterprise context
        prompt = self._build_analysis_prompt(target, diagnostics, incident_context, recent_changes)
        
        try:
            # Call Azure OpenAI
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_enterprise_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Low temperature for deterministic output
                max_tokens=2000,  # Increased for enterprise context
                response_format={"type": "json_object"}
            )
            
            # Parse AI response
            ai_response = json.loads(response.choices[0].message.content)
            
            logging.info("AI analysis completed successfully")
            
            return {
                "root_cause": ai_response.get("root_cause", "Unknown"),
                "confidence_percentage": ai_response.get("confidence_percentage", 0),
                "reasoning": ai_response.get("reasoning", ""),
                "evidence": ai_response.get("evidence", []),
                "remediation_steps": ai_response.get("remediation_steps", []),
                "severity": ai_response.get("severity", "MEDIUM"),
                "category": ai_response.get("category", "UNKNOWN"),
                # ENTERPRISE FEATURE 4: Responsibility Classification
                "root_cause_category": ai_response.get("root_cause_category", "Network Issue"),
                "responsibility_reason": ai_response.get("responsibility_reason", ""),
                "responsible_team": ai_response.get("responsible_team", "Network Operations"),
                # Change correlation
                "change_correlation": ai_response.get("change_correlation", None)
            }
        
        except Exception as e:
            logging.error(f"AI analysis failed: {str(e)}", exc_info=True)
            
            # Fallback to rule-based analysis
            return self._fallback_analysis(diagnostics, incident_context, recent_changes)
    
    def _get_system_prompt(self) -> str:
        """System prompt for AI analyzer"""
        return """You are a senior network engineer performing root cause analysis.

Analyze the provided network diagnostic results and provide a structured JSON response with:

1. root_cause: Single most likely root cause (concise, technical)
2. confidence_percentage: Your confidence level (0-100)
3. reasoning: Detailed technical explanation of your analysis
4. evidence: List of specific diagnostic findings supporting your conclusion
5. remediation_steps: Ordered list of actionable fix steps
6. severity: CRITICAL, HIGH, MEDIUM, LOW, or INFO
7. category: DNS, NETWORK, APPLICATION, SSL, FIREWALL, or CONFIGURATION

Rules:
- Base analysis ONLY on provided diagnostic data
- Do not hallucinate or assume information not present
- Be deterministic: same inputs = same outputs
- Prioritize the first failure in the diagnostic chain
- Consider failure propagation (e.g., DNS failure causes downstream failures)
- Provide specific, actionable remediation steps
- Use technical terminology appropriate for network engineers

Output valid JSON only."""
    
    def _get_enterprise_system_prompt(self) -> str:
        """ENTERPRISE ENHANCED: System prompt with context and change awareness"""
        return """You are a senior network engineer and incident commander performing enterprise-grade root cause analysis.

Analyze the provided network diagnostic results, incident context, and recent changes to provide a structured JSON response with:

1. root_cause: Single most likely root cause (concise, technical)
2. confidence_percentage: Your confidence level (0-100) - CALCULATE DYNAMICALLY:
   - Consider number of tests passed vs failed
   - Higher latency = lower confidence
   - More failures = lower confidence
   - Clear single point of failure = higher confidence
   - Ambiguous results = lower confidence
   - All tests pass with good latency (< 100ms) = 90-95%
   - All tests pass with high latency (> 500ms) = 70-80%
   - Single clear failure (e.g., DNS only) = 85-90%
   - Multiple failures = 60-75%
   - Unclear or partial failures = 40-60%
3. reasoning: Detailed technical explanation that EXPLICITLY references:
   - Incident timing and detection method
   - Business criticality and user impact
   - Recent changes (if any) and their correlation to the failure
   - Specific test results (latency, status, failure reasons)
4. evidence: List of specific diagnostic findings supporting your conclusion
5. remediation_steps: Ordered list of actionable fix steps
6. severity: CRITICAL, HIGH, MEDIUM, LOW, or INFO
7. category: DNS, NETWORK, APPLICATION, SSL, FIREWALL, or CONFIGURATION

ENTERPRISE FEATURES (REQUIRED):

8. root_cause_category: Classify into EXACTLY ONE of:
   - "Network Issue" → DNS, ports, firewall, routing, connectivity
   - "Application Issue" → HTTP failures, service not responding, application errors
   - "External Dependency Issue" → ISP, third-party APIs, cloud provider issues

9. responsibility_reason: Explain WHY this category was chosen (1-2 sentences)

10. responsible_team: Suggest which team should own the fix:
    - "Network Operations" → Network issues
    - "Application Team" → Application issues
    - "Platform Engineering" → Infrastructure/cloud issues
    - "External Vendor" → Third-party dependency issues

11. change_correlation: If recent changes were reported, analyze correlation:
    - If firewall change + port blocked → "High correlation: Recent firewall change likely caused port blockage"
    - If DNS change + DNS failure → "High correlation: Recent DNS change likely misconfigured"
    - If deployment + HTTP failure → "High correlation: Recent deployment may have broken the service"
    - If no correlation → null

CRITICAL RULES FOR CONFIDENCE CALCULATION:
- ALWAYS base confidence on the ACTUAL diagnostic results
- NEVER use static confidence values
- Consider latency values: < 50ms = excellent, 50-200ms = good, 200-500ms = degraded, > 500ms = poor
- All tests PASS + low latency → 90-95% confidence
- All tests PASS + high latency → 70-80% confidence (degraded performance)
- Single clear failure → 85-90% confidence
- Multiple failures → 60-75% confidence
- Ambiguous results → 40-60% confidence

CRITICAL RULES:
- ALWAYS reference incident context in your reasoning
- ALWAYS prioritize recent changes when determining root cause
- ALWAYS mention specific latency values in your analysis
- Base confidence on ACTUAL test results, not assumptions
- Be specific about which tests passed/failed
- If all tests pass but latency is high, mention performance degradation

Output valid JSON only.
- ALWAYS explain WHY a change is relevant (or not)
- Base analysis ONLY on provided data - do not hallucinate
- Be deterministic: same inputs = same outputs
- Use technical terminology appropriate for enterprise NOC teams

Example reasoning with context:
"Because the incident was detected immediately after a firewall rule update (recent_firewall_change: true), 
and TCP port 443 is now blocked, the most probable root cause is an incorrect inbound rule configuration. 
The high business criticality (affecting 500+ users) requires immediate escalation to Network Operations."

Output valid JSON only."""
    
    def _build_analysis_prompt(self, target: str, diagnostics: List[Dict],
                               incident_context: Dict = None, recent_changes: Dict = None) -> str:
        """Build user prompt with diagnostic data and enterprise context"""
        
        # Format diagnostics for AI
        diagnostic_summary = []
        for test in diagnostics:
            diagnostic_summary.append({
                "test": test["test_name"],
                "status": test["status"],
                "latency_ms": test["latency_ms"],
                "failure_reason": test.get("failure_reason"),
                "details": test.get("details")
            })
        
        prompt = f"""Perform root cause analysis for network diagnostics.

TARGET: {target}

DIAGNOSTIC RESULTS:
{json.dumps(diagnostic_summary, indent=2)}
"""
        
        # Add enterprise context if provided
        if incident_context:
            prompt += f"""

INCIDENT CONTEXT:
- Start Time: {incident_context.get('incident_start_time', 'Not specified')}
- Detection Type: {incident_context.get('incident_detection_type', 'User-Reported')}
- Affected Users: {incident_context.get('affected_users_count', 0)}
- Business Criticality: {incident_context.get('business_criticality', 'Medium')}
"""
        
        if recent_changes:
            changes_reported = []
            if recent_changes.get('recent_firewall_change'):
                changes_reported.append("Firewall rule update")
            if recent_changes.get('recent_dns_change'):
                changes_reported.append("DNS configuration change")
            if recent_changes.get('recent_deployment'):
                changes_reported.append("Application deployment")
            
            if changes_reported:
                prompt += f"""

RECENT CHANGES REPORTED:
{', '.join(changes_reported)}

IMPORTANT: Analyze correlation between these changes and the observed failures.
"""
            else:
                prompt += """

RECENT CHANGES: None reported
"""
        
        prompt += """

Analyze these results and provide your assessment in JSON format."""
        
        return prompt
    
    def _fallback_analysis(self, diagnostics: List[Dict], 
                           incident_context: Dict = None, recent_changes: Dict = None) -> Dict:
        """
        Rule-based fallback analysis if AI fails
        ENTERPRISE ENHANCED: Includes responsibility categorization
        Provides basic but accurate analysis
        """
        logging.warning("Using fallback rule-based analysis")
        
        # Find first failure
        first_failure = None
        for test in diagnostics:
            if test["status"] in ["FAIL", "INFERRED_FAIL"]:
                first_failure = test
                break
        
        if not first_failure:
            # All tests passed - calculate confidence based on latency
            avg_latency = sum(d.get('latency_ms', 0) for d in diagnostics) / len(diagnostics) if diagnostics else 0
            
            # Dynamic confidence based on latency
            if avg_latency < 100:
                confidence = 95  # Excellent performance
            elif avg_latency < 200:
                confidence = 90  # Good performance
            elif avg_latency < 500:
                confidence = 75  # Degraded performance
            else:
                confidence = 65  # Poor performance
            
            return {
                "root_cause": "No issues detected; all tests passed successfully",
                "confidence_percentage": confidence,
                "reasoning": f"All diagnostic tests (DNS, TCP, HTTP, latency) passed successfully. Average latency: {avg_latency:.0f}ms. The target is reachable and responding normally.",
                "evidence": [
                    "DNS resolution successful",
                    "TCP connectivity established",
                    "HTTP response received",
                    f"Average latency: {avg_latency:.0f}ms"
                ],
                "remediation_steps": ["No action required - system is healthy"],
                "severity": "INFO",
                "category": "HEALTHY",
                "root_cause_category": "Network Issue",
                "responsibility_reason": "All network layers functioning normally - no issues detected",
                "responsible_team": "Network Operations",
                "change_correlation": None
            }
        
        # Analyze based on first failure
        test_name = first_failure["test_name"]
        
        # Check for change correlation
        change_correlation = None
        if recent_changes:
            if recent_changes.get('recent_dns_change') and test_name == "DNS_RESOLUTION":
                change_correlation = "High correlation: Recent DNS change likely caused resolution failure"
            elif recent_changes.get('recent_firewall_change') and test_name == "TCP_CONNECTIVITY":
                change_correlation = "High correlation: Recent firewall change likely blocked the port"
            elif recent_changes.get('recent_deployment') and test_name == "HTTP_STATUS":
                change_correlation = "High correlation: Recent deployment may have broken the service"
        
        if test_name == "DNS_RESOLUTION":
            return {
                "root_cause": "DNS resolution failure",
                "confidence_percentage": 90,
                "reasoning": "The domain name could not be resolved to an IP address. This is the root cause preventing all downstream connectivity.",
                "evidence": [
                    f"DNS lookup failed: {first_failure.get('failure_reason', 'Unknown error')}",
                    "All downstream tests inferred as failed due to DNS failure"
                ],
                "remediation_steps": [
                    "Verify the domain name is correct and exists",
                    "Check DNS server configuration",
                    "Try alternative DNS servers (e.g., 8.8.8.8, 1.1.1.1)",
                    "Verify domain registration and nameserver configuration"
                ],
                "severity": "HIGH",
                "category": "DNS",
                "root_cause_category": "Network Issue",
                "responsibility_reason": "DNS resolution is a network-layer service managed by network operations",
                "responsible_team": "Network Operations",
                "change_correlation": change_correlation
            }
        
        elif test_name == "TCP_CONNECTIVITY":
            return {
                "root_cause": "TCP port connectivity failure",
                "confidence_percentage": 85,
                "reasoning": "DNS resolution succeeded but TCP connection to the target port failed. This suggests a firewall, network ACL, or service availability issue.",
                "evidence": [
                    "DNS resolution successful",
                    f"TCP connection failed: {first_failure.get('failure_reason', 'Port unreachable')}"
                ],
                "remediation_steps": [
                    "Verify the service is running on the target host",
                    "Check firewall rules (host-based and network-based)",
                    "Verify network ACLs and security groups",
                    "Confirm the correct port number",
                    "Check if the service is bound to the correct interface"
                ],
                "severity": "HIGH",
                "category": "FIREWALL",
                "root_cause_category": "Network Issue",
                "responsibility_reason": "Port blocking indicates firewall or network ACL configuration issue",
                "responsible_team": "Network Operations",
                "change_correlation": change_correlation
            }
        
        elif test_name == "HTTP_STATUS":
            return {
                "root_cause": "HTTP/Application layer failure",
                "confidence_percentage": 80,
                "reasoning": "Network connectivity is established but the HTTP request failed. This indicates an application-level issue.",
                "evidence": [
                    "DNS and TCP connectivity successful",
                    f"HTTP request failed: {first_failure.get('failure_reason', 'Unknown error')}"
                ],
                "remediation_steps": [
                    "Check web server logs for errors",
                    "Verify SSL/TLS certificate validity",
                    "Check application configuration",
                    "Verify web server is running and not overloaded",
                    "Review recent application deployments or changes"
                ],
                "severity": "MEDIUM",
                "category": "APPLICATION",
                "root_cause_category": "Application Issue",
                "responsibility_reason": "HTTP layer failure with successful network connectivity indicates application-level problem",
                "responsible_team": "Application Team",
                "change_correlation": change_correlation
            }
        
        else:
            return {
                "root_cause": "Unknown failure",
                "confidence_percentage": 50,
                "reasoning": "A failure was detected but the specific cause could not be determined.",
                "evidence": [f"Test {test_name} failed"],
                "remediation_steps": [
                    "Review detailed diagnostic logs",
                    "Perform manual troubleshooting",
                    "Contact network administrator"
                ],
                "severity": "MEDIUM",
                "category": "UNKNOWN",
                "root_cause_category": "Network Issue",
                "responsibility_reason": "Unable to determine specific category - defaulting to network operations",
                "responsible_team": "Network Operations",
                "change_correlation": change_correlation
            }
