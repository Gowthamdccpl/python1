#!/usr/bin/env python3
"""
Pet Care Project Health Check Tests
This script tests whether the project is running correctly
"""

import requests
import time
import json
import sys
from urllib.parse import urljoin

class PetCareHealthChecker:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, status, message="", response_time=None):
        """Log test results"""
        result = {
            "test": test_name,
            "status": "✅ PASS" if status else "❌ FAIL",
            "message": message,
            "response_time": f"{response_time:.2f}s" if response_time else "N/A"
        }
        self.test_results.append(result)
        print(f"{result['status']} {test_name} - {message} ({result['response_time']})")
        
    def test_server_connectivity(self):
        """Test if the server is running and responding"""
        try:
            start_time = time.time()
            response = self.session.get(self.base_url, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.log_test("Server Connectivity", True, "Server is running", response_time)
                return True
            else:
                self.log_test("Server Connectivity", False, f"HTTP {response.status_code}", response_time)
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Server Connectivity", False, f"Connection failed: {str(e)}")
            return False
    
    def test_homepage_load(self):
        """Test if homepage loads correctly"""
        try:
            start_time = time.time()
            response = self.session.get(self.base_url)
            response_time = time.time() - start_time
            
            if response.status_code == 200 and "PetCare" in response.text:
                self.log_test("Homepage Load", True, "Homepage loads with correct content", response_time)
                return True
            else:
                self.log_test("Homepage Load", False, "Homepage content missing", response_time)
                return False
        except Exception as e:
            self.log_test("Homepage Load", False, f"Error: {str(e)}")
            return False
    
    def test_adoption_page(self):
        """Test if adoption page is accessible"""
        try:
            start_time = time.time()
            url = urljoin(self.base_url, "/adoption")
            response = self.session.get(url)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.log_test("Adoption Page", True, "Adoption page accessible", response_time)
                return True
            else:
                self.log_test("Adoption Page", False, f"HTTP {response.status_code}", response_time)
                return False
        except Exception as e:
            self.log_test("Adoption Page", False, f"Error: {str(e)}")
            return False
    
    def test_food_recommendation_page(self):
        """Test if food recommendation page is accessible"""
        try:
            start_time = time.time()
            url = urljoin(self.base_url, "/food_recommendation")
            response = self.session.get(url)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.log_test("Food Recommendation Page", True, "Food page accessible", response_time)
                return True
            else:
                self.log_test("Food Recommendation Page", False, f"HTTP {response.status_code}", response_time)
                return False
        except Exception as e:
            self.log_test("Food Recommendation Page", False, f"Error: {str(e)}")
            return False
    
    def test_appointment_page(self):
        """Test if appointment page is accessible"""
        try:
            start_time = time.time()
            url = urljoin(self.base_url, "/appointment")
            response = self.session.get(url)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.log_test("Appointment Page", True, "Appointment page accessible", response_time)
                return True
            else:
                self.log_test("Appointment Page", False, f"HTTP {response.status_code}", response_time)
                return False
        except Exception as e:
            self.log_test("Appointment Page", False, f"Error: {str(e)}")
            return False
    
    def test_nearby_services_page(self):
        """Test if nearby services page is accessible"""
        try:
            start_time = time.time()
            url = urljoin(self.base_url, "/nearby-services")
            response = self.session.get(url)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.log_test("Nearby Services Page", True, "Services page accessible", response_time)
                return True
            else:
                self.log_test("Nearby Services Page", False, f"HTTP {response.status_code}", response_time)
                return False
        except Exception as e:
            self.log_test("Nearby Services Page", False, f"Error: {str(e)}")
            return False
    
    def test_admin_page(self):
        """Test if admin page is accessible"""
        try:
            start_time = time.time()
            url = urljoin(self.base_url, "/admin")
            response = self.session.get(url)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.log_test("Admin Page", True, "Admin page accessible", response_time)
                return True
            else:
                self.log_test("Admin Page", False, f"HTTP {response.status_code}", response_time)
                return False
        except Exception as e:
            self.log_test("Admin Page", False, f"Error: {str(e)}")
            return False
    
    def test_donation_page(self):
        """Test if donation page is accessible"""
        try:
            start_time = time.time()
            url = urljoin(self.base_url, "/donation")
            response = self.session.get(url)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.log_test("Donation Page", True, "Donation page accessible", response_time)
                return True
            else:
                self.log_test("Donation Page", False, f"HTTP {response.status_code}", response_time)
                return False
        except Exception as e:
            self.log_test("Donation Page", False, f"Error: {str(e)}")
            return False
    
    def test_ai_food_recommendation(self):
        """Test AI food recommendation functionality"""
        try:
            start_time = time.time()
            url = urljoin(self.base_url, "/predict")
            
            # Test data for AI recommendation
            test_data = {
                'age': '24',
                'weight': '15',
                'type': 'dog',
                'activity': 'medium',
                'health_conditions': ['diabetes']
            }
            
            response = self.session.post(url, data=test_data)
            response_time = time.time() - start_time
            
            if response.status_code == 200 and "recommendation" in response.text.lower():
                self.log_test("AI Food Recommendation", True, "AI engine working", response_time)
                return True
            else:
                self.log_test("AI Food Recommendation", False, "AI engine not responding", response_time)
                return False
        except Exception as e:
            self.log_test("AI Food Recommendation", False, f"Error: {str(e)}")
            return False
    
    def test_static_files(self):
        """Test if static files (CSS, JS) are loading"""
        try:
            start_time = time.time()
            css_url = urljoin(self.base_url, "/static/css/style.css")
            response = self.session.get(css_url)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.log_test("Static Files", True, "CSS files loading", response_time)
                return True
            else:
                self.log_test("Static Files", False, f"CSS not found: HTTP {response.status_code}", response_time)
                return False
        except Exception as e:
            self.log_test("Static Files", False, f"Error: {str(e)}")
            return False
    
    def test_database_connectivity(self):
        """Test database connectivity by checking if pets data loads"""
        try:
            start_time = time.time()
            url = urljoin(self.base_url, "/adoption")
            response = self.session.get(url)
            response_time = time.time() - start_time
            
            # Check if the page loads and contains pet-related content
            if response.status_code == 200 and ("pet" in response.text.lower() or "adoption" in response.text.lower()):
                self.log_test("Database Connectivity", True, "Database responding", response_time)
                return True
            else:
                self.log_test("Database Connectivity", False, "Database may not be connected", response_time)
                return False
        except Exception as e:
            self.log_test("Database Connectivity", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all health check tests"""
        print("🐾 Pet Care Project Health Check")
        print("=" * 50)
        
        # Core connectivity tests
        if not self.test_server_connectivity():
            print("\n❌ Server is not running! Please start the Flask application.")
            return False
        
        # Page accessibility tests
        self.test_homepage_load()
        self.test_adoption_page()
        self.test_food_recommendation_page()
        self.test_appointment_page()
        self.test_nearby_services_page()
        self.test_admin_page()
        self.test_donation_page()
        
        # Functionality tests
        self.test_ai_food_recommendation()
        self.test_static_files()
        self.test_database_connectivity()
        
        # Summary
        self.print_summary()
        return True
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        
        passed = sum(1 for result in self.test_results if "✅" in result["status"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 ALL TESTS PASSED! Your project is running perfectly!")
        elif passed >= total * 0.8:
            print("\n⚠️  Most tests passed. Check failed tests above.")
        else:
            print("\n❌ Multiple tests failed. Please check your application.")
        
        print("\n📋 Detailed Results:")
        for result in self.test_results:
            print(f"{result['status']} {result['test']} ({result['response_time']})")

def main():
    """Main function to run health checks"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Pet Care Project Health Checker')
    parser.add_argument('--url', default='http://localhost:5000', 
                       help='Base URL of the application (default: http://localhost:5000)')
    parser.add_argument('--quick', action='store_true', 
                       help='Run only basic connectivity tests')
    
    args = parser.parse_args()
    
    checker = PetCareHealthChecker(args.url)
    
    if args.quick:
        # Quick test - just check if server is running
        if checker.test_server_connectivity():
            print("✅ Server is running!")
            sys.exit(0)
        else:
            print("❌ Server is not running!")
            sys.exit(1)
    else:
        # Full test suite
        success = checker.run_all_tests()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
