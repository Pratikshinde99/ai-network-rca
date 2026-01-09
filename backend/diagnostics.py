"""
Network Diagnostics Module
Performs real network tests: DNS, HTTP, TCP, Latency
"""

import socket
import time
import requests
from typing import Dict, List
import logging

class NetworkDiagnostics:
    def __init__(self, target: str, service_type: str = "web"):
        self.target = target
        self.service_type = service_type
        self.results = []
        
        # Extract hostname and port if specified
        if ':' in target:
            self.hostname, port_str = target.split(':', 1)
            self.port = int(port_str)
        else:
            self.hostname = target
            self.port = 443 if service_type == "web" else 80
    
    def run_all_diagnostics(self) -> List[Dict]:
        """
        Run all diagnostic tests in logical order
        Returns structured results for each test
        """
        logging.info(f"Starting diagnostics for {self.target}")
        
        # Test 1: DNS Resolution (foundational)
        dns_result = self.test_dns_resolution()
        self.results.append(dns_result)
        
        # If DNS fails, infer downstream failures
        if dns_result['status'] == 'FAIL':
            self.results.append(self._infer_failure('TCP_CONNECTIVITY', 'DNS resolution failed'))
            self.results.append(self._infer_failure('HTTP_STATUS', 'DNS resolution failed'))
            self.results.append(self._infer_failure('LATENCY', 'DNS resolution failed'))
            return self.results
        
        # Test 2: TCP Connectivity
        tcp_result = self.test_tcp_connectivity()
        self.results.append(tcp_result)
        
        # If TCP fails, infer application-level failures
        if tcp_result['status'] == 'FAIL':
            self.results.append(self._infer_failure('HTTP_STATUS', 'TCP connection failed'))
            self.results.append(self._infer_failure('LATENCY', 'TCP connection failed'))
            return self.results
        
        # Test 3: HTTP/HTTPS Status
        http_result = self.test_http_status()
        self.results.append(http_result)
        
        # Test 4: Latency Measurement
        latency_result = self.test_latency()
        self.results.append(latency_result)
        
        return self.results
    
    def test_dns_resolution(self) -> Dict:
        """Test DNS resolution"""
        test_name = "DNS_RESOLUTION"
        start_time = time.time()
        
        try:
            ip_address = socket.gethostbyname(self.hostname)
            latency_ms = round((time.time() - start_time) * 1000, 2)
            
            logging.info(f"DNS resolved: {self.hostname} -> {ip_address}")
            
            return {
                "test_name": test_name,
                "status": "PASS",
                "latency_ms": latency_ms,
                "details": {
                    "hostname": self.hostname,
                    "ip_address": ip_address
                },
                "failure_reason": None
            }
        
        except socket.gaierror as e:
            latency_ms = round((time.time() - start_time) * 1000, 2)
            logging.warning(f"DNS resolution failed for {self.hostname}: {str(e)}")
            
            return {
                "test_name": test_name,
                "status": "FAIL",
                "latency_ms": latency_ms,
                "details": None,
                "failure_reason": f"DNS resolution failed: {str(e)}"
            }
    
    def test_tcp_connectivity(self) -> Dict:
        """Test TCP port connectivity"""
        test_name = "TCP_CONNECTIVITY"
        start_time = time.time()
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            
            result = sock.connect_ex((self.hostname, self.port))
            latency_ms = round((time.time() - start_time) * 1000, 2)
            sock.close()
            
            if result == 0:
                logging.info(f"TCP connection successful: {self.hostname}:{self.port}")
                return {
                    "test_name": test_name,
                    "status": "PASS",
                    "latency_ms": latency_ms,
                    "details": {
                        "hostname": self.hostname,
                        "port": self.port
                    },
                    "failure_reason": None
                }
            else:
                logging.warning(f"TCP connection failed: {self.hostname}:{self.port}")
                return {
                    "test_name": test_name,
                    "status": "FAIL",
                    "latency_ms": latency_ms,
                    "details": {
                        "hostname": self.hostname,
                        "port": self.port
                    },
                    "failure_reason": f"Port {self.port} is closed or unreachable"
                }
        
        except socket.timeout:
            latency_ms = round((time.time() - start_time) * 1000, 2)
            return {
                "test_name": test_name,
                "status": "FAIL",
                "latency_ms": latency_ms,
                "details": None,
                "failure_reason": "Connection timeout"
            }
        
        except Exception as e:
            latency_ms = round((time.time() - start_time) * 1000, 2)
            return {
                "test_name": test_name,
                "status": "FAIL",
                "latency_ms": latency_ms,
                "details": None,
                "failure_reason": str(e)
            }
    
    def test_http_status(self) -> Dict:
        """Test HTTP/HTTPS status"""
        test_name = "HTTP_STATUS"
        start_time = time.time()
        
        # Determine protocol
        protocol = "https" if self.port == 443 else "http"
        url = f"{protocol}://{self.hostname}"
        if self.port not in [80, 443]:
            url = f"{protocol}://{self.hostname}:{self.port}"
        
        try:
            response = requests.get(url, timeout=10, allow_redirects=True)
            latency_ms = round((time.time() - start_time) * 1000, 2)
            
            logging.info(f"HTTP request successful: {url} -> {response.status_code}")
            
            return {
                "test_name": test_name,
                "status": "PASS" if response.status_code < 400 else "FAIL",
                "latency_ms": latency_ms,
                "details": {
                    "url": url,
                    "status_code": response.status_code,
                    "response_time_ms": round(response.elapsed.total_seconds() * 1000, 2)
                },
                "failure_reason": None if response.status_code < 400 else f"HTTP {response.status_code}"
            }
        
        except requests.exceptions.SSLError as e:
            latency_ms = round((time.time() - start_time) * 1000, 2)
            return {
                "test_name": test_name,
                "status": "FAIL",
                "latency_ms": latency_ms,
                "details": {"url": url},
                "failure_reason": f"SSL/TLS error: {str(e)}"
            }
        
        except requests.exceptions.Timeout:
            latency_ms = round((time.time() - start_time) * 1000, 2)
            return {
                "test_name": test_name,
                "status": "FAIL",
                "latency_ms": latency_ms,
                "details": {"url": url},
                "failure_reason": "HTTP request timeout"
            }
        
        except Exception as e:
            latency_ms = round((time.time() - start_time) * 1000, 2)
            return {
                "test_name": test_name,
                "status": "FAIL",
                "latency_ms": latency_ms,
                "details": {"url": url},
                "failure_reason": str(e)
            }
    
    def test_latency(self) -> Dict:
        """Measure round-trip latency"""
        test_name = "LATENCY_CHECK"
        
        try:
            # Measure multiple samples
            samples = []
            for _ in range(3):
                start = time.time()
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((self.hostname, self.port))
                sock.close()
                samples.append((time.time() - start) * 1000)
            
            avg_latency = round(sum(samples) / len(samples), 2)
            min_latency = round(min(samples), 2)
            max_latency = round(max(samples), 2)
            
            logging.info(f"Latency measured: avg={avg_latency}ms")
            
            return {
                "test_name": test_name,
                "status": "PASS",
                "latency_ms": avg_latency,
                "details": {
                    "avg_ms": avg_latency,
                    "min_ms": min_latency,
                    "max_ms": max_latency,
                    "samples": len(samples)
                },
                "failure_reason": None
            }
        
        except Exception as e:
            return {
                "test_name": test_name,
                "status": "FAIL",
                "latency_ms": 0,
                "details": None,
                "failure_reason": str(e)
            }
    
    def _infer_failure(self, test_name: str, reason: str) -> Dict:
        """Create inferred failure result"""
        return {
            "test_name": test_name,
            "status": "INFERRED_FAIL",
            "latency_ms": 0,
            "details": None,
            "failure_reason": f"Inferred failure: {reason}"
        }
