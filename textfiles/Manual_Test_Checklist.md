# 🧪 Pet Care Project - Manual Test Checklist

## 🚀 Quick Start Testing Guide

### **Before Testing:**
1. ✅ Ensure Flask app is running: `python app.py`
2. ✅ Open browser to: `http://localhost:5000`
3. ✅ Have test data ready (pet details, appointment info)

---

## 📋 **BASIC FUNCTIONALITY TESTS**

### **Test 1: Homepage Loading**
- [ ] Navigate to `http://localhost:5000`
- [ ] Page loads within 3 seconds
- [ ] "PetCare Companion" title is visible
- [ ] Navigation menu is present
- [ ] Hero section displays correctly
- [ ] Feature cards are visible

**Expected Result:** Homepage loads completely with all elements visible

---

### **Test 2: Navigation Menu**
- [ ] Click on "Adoption" link
- [ ] Click on "Food Rec." link  
- [ ] Click on "Appointment" link
- [ ] Click on "Donation" link
- [ ] Click on "Nearby Services" link
- [ ] Click on "Admin" link

**Expected Result:** All pages load without errors

---

### **Test 3: Pet Adoption Page**
- [ ] Navigate to `/adoption`
- [ ] Pet cards are displayed
- [ ] Images load correctly (or show fallback)
- [ ] Pet details are visible (name, breed, age)
- [ ] "Adopt Me" buttons are present
- [ ] Filtering options work

**Expected Result:** Adoption page shows available pets with complete information

---

### **Test 4: AI Food Recommendation**
- [ ] Navigate to `/food_recommendation`
- [ ] Fill out the form:
  - Age: 24 months
  - Weight: 15 kg
  - Type: Dog
  - Activity: Medium
  - Health Conditions: Select "Diabetes"
- [ ] Click "Get Recommendations"
- [ ] Wait for results page
- [ ] Verify recommendations are displayed

**Expected Result:** AI provides relevant food recommendations based on input

---

### **Test 5: Appointment Booking**
- [ ] Navigate to `/appointment`
- [ ] Fill out appointment form:
  - Owner Name: Test User
  - Email: test@example.com
  - Phone: 9876543210
  - Pet Name: Buddy
  - Pet Type: Dog
  - Pet Age: 2
  - Appointment Type: General Checkup
  - Date: Tomorrow's date
  - Time: Morning
- [ ] Submit form
- [ ] Check confirmation page

**Expected Result:** Appointment booked successfully with confirmation

---

### **Test 6: Nearby Services**
- [ ] Navigate to `/nearby-services`
- [ ] Allow location access (if prompted)
- [ ] Verify veterinary hospitals are listed
- [ ] Check pet pharmacies section
- [ ] Verify pet shops section
- [ ] Click on a service to see details

**Expected Result:** Local Bangalore services are displayed with contact info

---

### **Test 7: Donation Page**
- [ ] Navigate to `/donation`
- [ ] Verify donation form is present
- [ ] Check G Pay QR code is visible
- [ ] Verify payment options are listed
- [ ] Test form validation (try submitting empty form)

**Expected Result:** Donation page loads with payment options

---

### **Test 8: Admin Panel Access**
- [ ] Navigate to `/admin`
- [ ] Try accessing without login
- [ ] Go to `/admin/login`
- [ ] Login with credentials:
  - Username: admin
  - Password: admin123
- [ ] Verify dashboard loads
- [ ] Check statistics are displayed

**Expected Result:** Admin login works and dashboard shows data

---

## 🔧 **ADVANCED FUNCTIONALITY TESTS**

### **Test 9: Pet Adoption Application**
- [ ] Go to adoption page
- [ ] Click "Adopt Me" on any pet
- [ ] Fill out adoption application:
  - Name: Test Adopter
  - Email: adopter@test.com
  - Phone: 9876543210
  - Address: Test Address, Bangalore
  - Experience: Some experience with pets
  - Living Situation: Apartment with garden
- [ ] Submit application
- [ ] Verify confirmation page

**Expected Result:** Application submitted with confirmation message

---

### **Test 10: Admin Pet Management**
- [ ] Login to admin panel
- [ ] Navigate to pet management
- [ ] Try adding a new pet
- [ ] Edit existing pet details
- [ ] Check application reviews
- [ ] Verify notifications

**Expected Result:** Admin can manage pets and view applications

---

### **Test 11: Mobile Responsiveness**
- [ ] Open site on mobile device or resize browser
- [ ] Test navigation menu (hamburger menu)
- [ ] Verify all pages are mobile-friendly
- [ ] Test form submissions on mobile
- [ ] Check image loading on mobile

**Expected Result:** Site works perfectly on mobile devices

---

### **Test 12: Error Handling**
- [ ] Try accessing non-existent page: `/nonexistent`
- [ ] Submit forms with invalid data
- [ ] Test with slow internet connection
- [ ] Try accessing admin pages without login

**Expected Result:** Appropriate error messages and graceful handling

---

## 🚨 **CRITICAL SYSTEM TESTS**

### **Test 13: Database Connectivity**
- [ ] Check if pets are loading on adoption page
- [ ] Submit an appointment and verify it's saved
- [ ] Login to admin and check if data persists
- [ ] Restart the application and verify data remains

**Expected Result:** All data persists correctly in database

---

### **Test 14: AI Model Functionality**
- [ ] Test food recommendations with different inputs:
  - Young puppy (6 months, 5kg, high activity)
  - Senior dog (8 years, 25kg, low activity)
  - Cat with health issues
- [ ] Verify different recommendations for different inputs
- [ ] Check response time is under 5 seconds

**Expected Result:** AI provides varied, relevant recommendations quickly

---

### **Test 15: File and Static Resources**
- [ ] Check if CSS styles are loading
- [ ] Verify JavaScript functionality works
- [ ] Test image uploads (if admin)
- [ ] Check if pet images display correctly

**Expected Result:** All static resources load properly

---

## 📊 **PERFORMANCE TESTS**

### **Test 16: Page Load Speed**
- [ ] Measure homepage load time
- [ ] Check adoption page load time
- [ ] Test AI recommendation response time
- [ ] Verify admin dashboard load time

**Target:** All pages should load within 3 seconds

---

### **Test 17: Multiple User Simulation**
- [ ] Open multiple browser tabs
- [ ] Perform different actions simultaneously
- [ ] Check if system remains responsive
- [ ] Verify no conflicts between sessions

**Expected Result:** System handles multiple users without issues

---

## ✅ **TEST COMPLETION CHECKLIST**

### **Basic Tests (Must Pass):**
- [ ] Homepage loads correctly
- [ ] All navigation links work
- [ ] Pet adoption page displays pets
- [ ] AI food recommendation works
- [ ] Appointment booking functions
- [ ] Admin login successful

### **Advanced Tests (Should Pass):**
- [ ] Mobile responsiveness works
- [ ] Database saves data correctly
- [ ] Error handling is graceful
- [ ] Static files load properly

### **Performance Tests (Nice to Have):**
- [ ] Pages load within 3 seconds
- [ ] System handles multiple users
- [ ] AI responds quickly
- [ ] No memory leaks or crashes

---

## 🎯 **SUCCESS CRITERIA**

**✅ Project is RUNNING CORRECTLY if:**
- All basic tests pass (6/6)
- At least 80% of advanced tests pass (6/8)
- No critical errors or crashes
- Core functionality works as expected

**⚠️ Project needs ATTENTION if:**
- Some basic tests fail
- Performance is significantly slow
- Database connectivity issues
- AI recommendations not working

**❌ Project is NOT WORKING if:**
- Homepage doesn't load
- Multiple basic tests fail
- Server connectivity issues
- Critical functionality broken

---

## 🔧 **Troubleshooting Guide**

### **If Homepage Doesn't Load:**
1. Check if Flask app is running: `python app.py`
2. Verify port 5000 is not blocked
3. Check console for error messages

### **If Database Issues:**
1. Run: `python -c "from app import db; db.create_all()"`
2. Check if `petcare.db` file exists
3. Verify database permissions

### **If AI Recommendations Fail:**
1. Check if `model.pkl` file exists
2. Verify `food_data.json` is present
3. Check Python ML libraries are installed

### **If Static Files Don't Load:**
1. Verify `static/` folder exists
2. Check CSS and JS files are present
3. Clear browser cache

---

**💡 Pro Tip:** Run the automated test script first (`python project_health_tests.py`) before doing manual testing to quickly identify any major issues!
