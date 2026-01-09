import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:7071/api';

function App() {
    const [target, setTarget] = useState('');
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);
    const [error, setError] = useState(null);

    // ENTERPRISE FEATURE 1: Incident Context (OPTIONAL - for NOC teams)
    const [incidentStartTime, setIncidentStartTime] = useState('');
    const [detectionType, setDetectionType] = useState('User-Reported');
    const [affectedUsers, setAffectedUsers] = useState('');
    const [businessCriticality, setBusinessCriticality] = useState('Medium');

    // ENTERPRISE FEATURE 2: Recent Changes
    const [firewallChange, setFirewallChange] = useState(false);
    const [dnsChange, setDnsChange] = useState(false);
    const [deployment, setDeployment] = useState(false);

    // Show/hide enterprise inputs
    const [showEnterpriseInputs, setShowEnterpriseInputs] = useState(false);

    const runDiagnostics = async () => {
        if (!target.trim()) {
            setError('Please enter a domain or IP address');
            return;
        }

        setLoading(true);
        setError(null);
        setResults(null);

        try {
            // Build request with enterprise context
            const requestBody = {
                target: target.trim(),
                service_type: 'web'
            };

            // Add enterprise context if provided
            if (showEnterpriseInputs) {
                if (incidentStartTime) {
                    requestBody.incident_start_time = incidentStartTime;
                }
                requestBody.incident_detection_type = detectionType;
                if (affectedUsers) {
                    requestBody.affected_users_count = parseInt(affectedUsers);
                }
                requestBody.business_criticality = businessCriticality;

                // Recent changes
                requestBody.recent_firewall_change = firewallChange;
                requestBody.recent_dns_change = dnsChange;
                requestBody.recent_deployment = deployment;
            }

            const response = await axios.post(`${API_URL}/diagnose`, requestBody);
            setResults(response.data);
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to run diagnostics. Please try again.');
            console.error('Diagnostic error:', err);
        } finally {
            setLoading(false);
        }
    };

    const downloadReport = (reportType) => {
        if (!results) return;

        let content, filename, mimeType;

        if (reportType === 'technical') {
            content = results.rca_report;
            filename = `rca_technical_${results.target}_${new Date().toISOString().split('T')[0]}.txt`;
            mimeType = 'text/plain';
        } else if (reportType === 'executive') {
            content = results.executive_report;
            filename = `rca_executive_${results.target}_${new Date().toISOString().split('T')[0]}.txt`;
            mimeType = 'text/plain';
        } else if (reportType === 'json') {
            content = JSON.stringify(results.technical_report, null, 2);
            filename = `rca_technical_${results.target}_${new Date().toISOString().split('T')[0]}.json`;
            mimeType = 'application/json';
        }

        const blob = new Blob([content], { type: mimeType });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    };

    const getStatusIcon = (status) => {
        if (status === 'PASS') return '✓';
        if (status === 'FAIL') return '✗';
        return '⚠';
    };

    const getStatusClass = (status) => {
        if (status === 'PASS') return 'status-pass';
        if (status === 'FAIL') return 'status-fail';
        return 'status-warn';
    };

    const getSeverityClass = (severity) => {
        const severityMap = {
            'CRITICAL': 'severity-critical',
            'HIGH': 'severity-high',
            'MEDIUM': 'severity-medium',
            'LOW': 'severity-low',
            'INFO': 'severity-info'
        };
        return severityMap[severity] || 'severity-medium';
    };

    // FIX: Proper confidence level calculation
    const getConfidenceLevel = (percentage) => {
        if (percentage >= 80) return { label: 'HIGH', class: 'confidence-high' };
        if (percentage >= 60) return { label: 'MEDIUM', class: 'confidence-medium' };
        return { label: 'LOW', class: 'confidence-low' };
    };

    return (
        <div className="app">
            <header className="header">
                <div className="header-content">
                    <h1>🔍 AI-Powered Network RCA</h1>
                    <p className="subtitle">Real-time diagnostics with Azure OpenAI intelligence</p>
                    <div className="tech-badges">
                        <span className="badge">Azure Functions</span>
                        <span className="badge">Azure OpenAI</span>
                        <span className="badge">Blob Storage</span>
                        <span className="badge badge-enterprise">Enterprise Features</span>
                    </div>
                </div>
            </header>

            <main className="main-content">
                <div className="input-section card">
                    <h2>Run Network Diagnostics</h2>

                    <div className="input-group">
                        <input
                            type="text"
                            className="target-input"
                            placeholder="Enter domain or IP (e.g., google.com)"
                            value={target}
                            onChange={(e) => setTarget(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && runDiagnostics()}
                            disabled={loading}
                        />
                        <button
                            className="run-button"
                            onClick={runDiagnostics}
                            disabled={loading}
                        >
                            {loading ? (
                                <>
                                    <span className="spinner"></span>
                                    Running...
                                </>
                            ) : (
                                '🚀 Run Diagnostics'
                            )}
                        </button>
                    </div>

                    {/* ENTERPRISE INPUTS TOGGLE - WITH BETTER EXPLANATION */}
                    <div className="enterprise-toggle">
                        <button
                            className="toggle-button"
                            onClick={() => setShowEnterpriseInputs(!showEnterpriseInputs)}
                        >
                            {showEnterpriseInputs ? '▼' : '▶'} Advanced: Add Incident Context (Optional)
                        </button>
                        <p className="toggle-hint">
                            💡 For NOC teams: Add incident metadata to get context-aware AI analysis
                        </p>
                    </div>

                    {/* ENTERPRISE FEATURE 1 & 2: Incident Context and Change Awareness */}
                    {showEnterpriseInputs && (
                        <div className="enterprise-inputs">
                            <div className="enterprise-explanation">
                                <strong>ℹ️ Why provide this information?</strong>
                                <p>This optional metadata helps the AI provide more relevant analysis by understanding:</p>
                                <ul>
                                    <li>When the incident started (for timeline correlation)</li>
                                    <li>How many users are affected (for priority assessment)</li>
                                    <li>Recent infrastructure changes (for change correlation)</li>
                                </ul>
                                <p><em>Skip this section for basic diagnostics.</em></p>
                            </div>

                            <h3>📋 Incident Metadata</h3>
                            <div className="input-row">
                                <div className="input-field">
                                    <label>When did the issue start?</label>
                                    <input
                                        type="datetime-local"
                                        value={incidentStartTime}
                                        onChange={(e) => setIncidentStartTime(e.target.value)}
                                    />
                                </div>
                                <div className="input-field">
                                    <label>How was it detected?</label>
                                    <select value={detectionType} onChange={(e) => setDetectionType(e.target.value)}>
                                        <option value="User-Reported">User-Reported</option>
                                        <option value="System-Detected">System-Detected (Monitoring)</option>
                                    </select>
                                </div>
                            </div>

                            <div className="input-row">
                                <div className="input-field">
                                    <label>How many users are affected?</label>
                                    <input
                                        type="number"
                                        placeholder="e.g., 500"
                                        value={affectedUsers}
                                        onChange={(e) => setAffectedUsers(e.target.value)}
                                    />
                                </div>
                                <div className="input-field">
                                    <label>Business Impact Level</label>
                                    <select value={businessCriticality} onChange={(e) => setBusinessCriticality(e.target.value)}>
                                        <option value="Low">Low - Minor inconvenience</option>
                                        <option value="Medium">Medium - Noticeable impact</option>
                                        <option value="High">High - Critical business impact</option>
                                    </select>
                                </div>
                            </div>

                            <h3>🔄 Recent Infrastructure Changes</h3>
                            <p className="section-hint">Check any changes made in the last 24 hours:</p>
                            <div className="checkbox-group">
                                <label className="checkbox-label">
                                    <input
                                        type="checkbox"
                                        checked={firewallChange}
                                        onChange={(e) => setFirewallChange(e.target.checked)}
                                    />
                                    <span>Firewall rules were modified</span>
                                </label>
                                <label className="checkbox-label">
                                    <input
                                        type="checkbox"
                                        checked={dnsChange}
                                        onChange={(e) => setDnsChange(e.target.checked)}
                                    />
                                    <span>DNS configuration was changed</span>
                                </label>
                                <label className="checkbox-label">
                                    <input
                                        type="checkbox"
                                        checked={deployment}
                                        onChange={(e) => setDeployment(e.target.checked)}
                                    />
                                    <span>New code/application was deployed</span>
                                </label>
                            </div>
                        </div>
                    )}

                    {error && (
                        <div className="error-message">
                            <strong>Error:</strong> {error}
                        </div>
                    )}
                </div>

                {results && (
                    <>
                        {/* ENTERPRISE CONTEXT DISPLAY - Only if provided */}
                        {results.incident_context && (results.incident_context.incident_start_time || results.incident_context.affected_users_count > 0) && (
                            <div className="enterprise-context card">
                                <h2>📊 Incident Context</h2>
                                <div className="context-grid">
                                    {results.incident_context.incident_start_time && (
                                        <div className="context-item">
                                            <span className="context-label">Incident Started:</span>
                                            <span className="context-value">{new Date(results.incident_context.incident_start_time).toLocaleString()}</span>
                                        </div>
                                    )}
                                    <div className="context-item">
                                        <span className="context-label">Detection Method:</span>
                                        <span className="context-value">{results.incident_context.incident_detection_type}</span>
                                    </div>
                                    {results.incident_context.affected_users_count > 0 && (
                                        <div className="context-item">
                                            <span className="context-label">Users Affected:</span>
                                            <span className="context-value highlight">{results.incident_context.affected_users_count.toLocaleString()}</span>
                                        </div>
                                    )}
                                    <div className="context-item">
                                        <span className="context-label">Business Impact:</span>
                                        <span className={`context-value criticality-${results.incident_context.business_criticality.toLowerCase()}`}>
                                            {results.incident_context.business_criticality}
                                        </span>
                                    </div>
                                </div>

                                {/* RECENT CHANGES */}
                                {results.recent_changes && (results.recent_changes.recent_firewall_change || results.recent_changes.recent_dns_change || results.recent_changes.recent_deployment) && (
                                    <div className="recent-changes">
                                        <h3>🔄 Recent Changes Detected:</h3>
                                        <div className="changes-list">
                                            {results.recent_changes.recent_firewall_change && <span className="change-badge">🔥 Firewall Update</span>}
                                            {results.recent_changes.recent_dns_change && <span className="change-badge">🌐 DNS Change</span>}
                                            {results.recent_changes.recent_deployment && <span className="change-badge">🚀 Deployment</span>}
                                        </div>
                                    </div>
                                )}
                            </div>
                        )}

                        {/* Diagnostic Results */}
                        <div className="results-section card">
                            <h2>📊 Diagnostic Test Results</h2>
                            <div className="diagnostics-grid">
                                {results.diagnostics.map((test, index) => (
                                    <div key={index} className={`diagnostic-card ${getStatusClass(test.status)}`}>
                                        <div className="diagnostic-header">
                                            <span className="status-icon">{getStatusIcon(test.status)}</span>
                                            <h3>{test.test_name.replace(/_/g, ' ')}</h3>
                                        </div>
                                        <div className="diagnostic-body">
                                            <div className="diagnostic-stat">
                                                <span className="label">Status:</span>
                                                <span className={`value ${getStatusClass(test.status)}`}>
                                                    {test.status}
                                                </span>
                                            </div>
                                            <div className="diagnostic-stat">
                                                <span className="label">Latency:</span>
                                                <span className="value">{test.latency_ms} ms</span>
                                            </div>
                                            {test.failure_reason && (
                                                <div className="failure-reason">
                                                    <strong>Reason:</strong> {test.failure_reason}
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* AI Analysis with ENTERPRISE FEATURES */}
                        <div className="ai-section card">
                            <h2>🧠 AI Root Cause Analysis</h2>

                            <div className="ai-summary">
                                {/* Only show confidence badge */}
                                <div className="confidence-meter">
                                    {(() => {
                                        const confidenceInfo = getConfidenceLevel(results.ai_analysis.confidence_percentage);
                                        return (
                                            <>
                                                <div className="confidence-header">
                                                    <span className="confidence-label">
                                                        Confidence: {results.ai_analysis.confidence_percentage}%
                                                    </span>
                                                    <span className={`confidence-badge ${confidenceInfo.class}`}>
                                                        {confidenceInfo.label}
                                                    </span>
                                                </div>
                                                <div className="confidence-bar">
                                                    <div
                                                        className="confidence-fill"
                                                        style={{ width: `${results.ai_analysis.confidence_percentage}%` }}
                                                    ></div>
                                                </div>
                                            </>
                                        );
                                    })()}
                                </div>
                            </div>

                            <div className="root-cause">
                                <h3>🎯 Root Cause</h3>
                                <p className="root-cause-text">{results.ai_analysis.root_cause}</p>
                            </div>

                            {/* ENTERPRISE FEATURE 4: Responsibility Classification */}
                            {results.ai_analysis.root_cause_category && (
                                <div className="responsibility-section">
                                    <h3>👥 Responsibility Assignment</h3>
                                    <div className="responsibility-grid">
                                        <div className="responsibility-item">
                                            <span className="resp-label">Issue Category:</span>
                                            <span className="resp-value category-badge">{results.ai_analysis.root_cause_category}</span>
                                        </div>
                                        <div className="responsibility-item">
                                            <span className="resp-label">Responsible Team:</span>
                                            <span className="resp-value team-badge">{results.ai_analysis.responsible_team}</span>
                                        </div>
                                    </div>
                                    {results.ai_analysis.responsibility_reason && (
                                        <div className="responsibility-reason">
                                            <strong>Why this team?</strong> {results.ai_analysis.responsibility_reason}
                                        </div>
                                    )}
                                </div>
                            )}

                            {/* ENTERPRISE FEATURE 2: Change Correlation */}
                            {results.ai_analysis.change_correlation && (
                                <div className="change-correlation">
                                    <h3>🔗 Change Impact Analysis</h3>
                                    <p className="correlation-text">{results.ai_analysis.change_correlation}</p>
                                </div>
                            )}

                            <div className="reasoning">
                                <h3>💡 Detailed Analysis</h3>
                                <p>{results.ai_analysis.reasoning}</p>
                            </div>

                            {results.ai_analysis.evidence && results.ai_analysis.evidence.length > 0 && (
                                <div className="evidence">
                                    <h3>📋 Supporting Evidence</h3>
                                    <ul>
                                        {results.ai_analysis.evidence.map((item, index) => (
                                            <li key={index}>{item}</li>
                                        ))}
                                    </ul>
                                </div>
                            )}

                            {results.ai_analysis.remediation_steps && results.ai_analysis.remediation_steps.length > 0 && (
                                <div className="remediation">
                                    <h3>🔧 Recommended Actions</h3>
                                    <ol>
                                        {results.ai_analysis.remediation_steps.map((step, index) => (
                                            <li key={index}>{step}</li>
                                        ))}
                                    </ol>
                                </div>
                            )}
                        </div>

                        {/* ENTERPRISE FEATURE 3: Dual RCA Output - Download Options */}
                        <div className="download-section card">
                            <h2>📄 Download RCA Reports</h2>
                            <p>Choose the report format that best suits your needs:</p>

                            <div className="download-grid">
                                {/* Technical Text Report */}
                                <div className="download-option">
                                    <div className="download-icon">📄</div>
                                    <h3>Technical Report</h3>
                                    <p>Detailed technical analysis for engineers and NOC teams</p>
                                    <button className="download-button technical" onClick={() => downloadReport('technical')}>
                                        ⬇️ Download Technical (.txt)
                                    </button>
                                </div>

                                {/* Executive Summary */}
                                <div className="download-option">
                                    <div className="download-icon">👔</div>
                                    <h3>Executive Summary</h3>
                                    <p>Plain English summary for managers and stakeholders</p>
                                    <button className="download-button executive" onClick={() => downloadReport('executive')}>
                                        ⬇️ Download Executive (.txt)
                                    </button>
                                </div>

                                {/* Technical JSON */}
                                <div className="download-option">
                                    <div className="download-icon">🤖</div>
                                    <h3>Machine-Readable JSON</h3>
                                    <p>Structured data for automation and integration</p>
                                    <button className="download-button json" onClick={() => downloadReport('json')}>
                                        ⬇️ Download JSON (.json)
                                    </button>
                                </div>
                            </div>

                            {/* REMOVED: Blob Storage URLs (private) */}
                        </div>
                    </>
                )}

                {!results && !loading && (
                    <div className="welcome-card card">
                        <h2>Welcome to AI-Powered Network RCA Platform</h2>
                        <p>Perform comprehensive network diagnostics and get intelligent root cause analysis powered by Azure OpenAI.</p>

                        <div className="features">
                            <div className="feature">
                                <span className="feature-icon">🔍</span>
                                <h3>Real Diagnostics</h3>
                                <p>DNS, TCP, HTTP, and latency tests</p>
                            </div>
                            <div className="feature">
                                <span className="feature-icon">🧠</span>
                                <h3>AI Analysis</h3>
                                <p>GPT-4 powered root cause reasoning</p>
                            </div>
                            <div className="feature">
                                <span className="feature-icon">📊</span>
                                <h3>Context-Aware</h3>
                                <p>Optional incident metadata for better insights</p>
                            </div>
                            <div className="feature">
                                <span className="feature-icon">📄</span>
                                <h3>Multi-Format Reports</h3>
                                <p>Technical, Executive, and JSON formats</p>
                            </div>
                        </div>

                        <div className="demo-examples">
                            <h3>Try these examples:</h3>
                            <div className="example-buttons">
                                <button onClick={() => setTarget('google.com')} className="example-btn">
                                    ✅ google.com (Success)
                                </button>
                                <button onClick={() => setTarget('github.com')} className="example-btn">
                                    ✅ github.com (Success)
                                </button>
                                <button onClick={() => setTarget('nonexistent-domain-xyz.com')} className="example-btn">
                                    ❌ Test DNS Failure
                                </button>
                            </div>
                        </div>
                    </div>
                )}
            </main>

            <footer className="footer">
                <p>Built with Azure Functions, Azure OpenAI, and React | Enterprise-Grade RCA Platform 2026</p>
            </footer>
        </div>
    );
}

export default App;
