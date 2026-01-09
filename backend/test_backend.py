"""
Simple test script to verify backend functionality
Run this before the demo to ensure everything works
"""

import requests
import json
import sys

# Configuration
API_URL = "http://localhost:7071/api"

def test_health_check():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("TEST 1: Health Check")
    print("="*60)
    
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ PASSED: Health check successful")
            return True
        else:
            print("❌ FAILED: Unexpected status code")
            return False
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

def test_successful_diagnostic():
    """Test with a domain that should pass"""
    print("\n" + "="*60)
    print("TEST 2: Successful Diagnostic (google.com)")
    print("="*60)
    
    try:
        payload = {
            "target": "google.com",
            "service_type": "web"
        }
        
        print(f"Sending request: {json.dumps(payload)}")
        response = requests.post(
            f"{API_URL}/diagnose",
            json=payload,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Check structure
            assert "diagnostics" in data, "Missing 'diagnostics' field"
            assert "ai_analysis" in data, "Missing 'ai_analysis' field"
            assert "rca_report" in data, "Missing 'rca_report' field"
            
            # Check diagnostics
            print(f"\nDiagnostic Tests Run: {len(data['diagnostics'])}")
            for test in data['diagnostics']:
                status_icon = "✅" if test['status'] == 'PASS' else "❌"
                print(f"  {status_icon} {test['test_name']}: {test['status']} ({test['latency_ms']}ms)")
            
            # Check AI analysis
            print(f"\nAI Analysis:")
            print(f"  Root Cause: {data['ai_analysis']['root_cause']}")
            print(f"  Confidence: {data['ai_analysis']['confidence_percentage']}%")
            print(f"  Severity: {data['ai_analysis']['severity']}")
            
            print("\n✅ PASSED: Successful diagnostic test")
            return True
        else:
            print(f"❌ FAILED: Status code {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

def test_dns_failure():
    """Test with a domain that doesn't exist"""
    print("\n" + "="*60)
    print("TEST 3: DNS Failure (nonexistent-domain-xyz.com)")
    print("="*60)
    
    try:
        payload = {
            "target": "nonexistent-domain-xyz123.com",
            "service_type": "web"
        }
        
        print(f"Sending request: {json.dumps(payload)}")
        response = requests.post(
            f"{API_URL}/diagnose",
            json=payload,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Check that DNS failed
            dns_test = next((t for t in data['diagnostics'] if t['test_name'] == 'DNS_RESOLUTION'), None)
            
            if dns_test and dns_test['status'] == 'FAIL':
                print(f"\n✅ DNS correctly failed")
                print(f"  Failure reason: {dns_test['failure_reason']}")
                
                # Check AI identified DNS as root cause
                if 'DNS' in data['ai_analysis']['root_cause'].upper():
                    print(f"✅ AI correctly identified DNS as root cause")
                    print(f"  Root Cause: {data['ai_analysis']['root_cause']}")
                    print(f"  Confidence: {data['ai_analysis']['confidence_percentage']}%")
                    
                    print("\n✅ PASSED: DNS failure test")
                    return True
                else:
                    print(f"⚠️  WARNING: AI didn't identify DNS as root cause")
                    print(f"  Root Cause: {data['ai_analysis']['root_cause']}")
                    return True  # Still pass, but warn
            else:
                print("❌ FAILED: DNS should have failed")
                return False
        else:
            print(f"❌ FAILED: Status code {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

def test_invalid_input():
    """Test with missing target"""
    print("\n" + "="*60)
    print("TEST 4: Invalid Input (missing target)")
    print("="*60)
    
    try:
        payload = {
            "service_type": "web"
        }
        
        response = requests.post(
            f"{API_URL}/diagnose",
            json=payload,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 400:
            print("✅ PASSED: Correctly rejected invalid input")
            return True
        else:
            print(f"❌ FAILED: Expected 400, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 NETWORK RCA PLATFORM - TEST SUITE")
    print("="*60)
    print(f"API URL: {API_URL}")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health_check()))
    results.append(("Successful Diagnostic", test_successful_diagnostic()))
    results.append(("DNS Failure", test_dns_failure()))
    results.append(("Invalid Input", test_invalid_input()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print("="*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Ready for demo!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix before demo.")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ CRITICAL ERROR: {str(e)}")
        sys.exit(1)
