from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pickle
import numpy as np
import pandas as pd
import json
import collections
from datetime import datetime
import os
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///petcare.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Configuration for file uploads
UPLOAD_FOLDER = 'static/images/pets'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Admin credentials (in production, use a proper authentication system)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database Models
class Pet(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    age = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    health_status = db.Column(db.String(100), nullable=False)
    vaccination_status = db.Column(db.String(100), nullable=False)
    spayed_neutered = db.Column(db.Boolean, default=False)
    special_needs = db.Column(db.Text)
    adoption_fee = db.Column(db.Integer, nullable=False)
    contact_info = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(200), default='default_pet.jpg')
    status = db.Column(db.String(50), default='available')  # available, adopted, pending
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'breed': self.breed,
            'age': self.age,
            'gender': self.gender,
            'size': self.size,
            'color': self.color,
            'description': self.description,
            'health_status': self.health_status,
            'vaccination_status': self.vaccination_status,
            'spayed_neutered': self.spayed_neutered,
            'special_needs': self.special_needs,
            'adoption_fee': self.adoption_fee,
            'contact_info': self.contact_info,
            'location': self.location,
            'image': self.image,
            'status': self.status,
            'date_added': self.date_added.strftime('%Y-%m-%d') if self.date_added else None
        }

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    owner_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    pet_name = db.Column(db.String(100), nullable=False)
    pet_type = db.Column(db.String(50), nullable=False)
    pet_age = db.Column(db.String(50), nullable=False)
    age_unit = db.Column(db.String(20), nullable=False)
    appointment_type = db.Column(db.String(100), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    notes = db.Column(db.Text)
    status = db.Column(db.String(50), default='pending')  # pending, confirmed, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'owner_name': self.owner_name,
            'email': self.email,
            'phone': self.phone,
            'pet_name': self.pet_name,
            'pet_type': self.pet_type,
            'pet_age': self.pet_age,
            'age_unit': self.age_unit,
            'appointment_type': self.appointment_type,
            'appointment_date': self.appointment_date.strftime('%Y-%m-%d') if self.appointment_date else None,
            'appointment_time': self.appointment_time.strftime('%H:%M') if self.appointment_time else None,
            'notes': self.notes,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None
        }

class AdoptionApplication(db.Model):
    __tablename__ = 'adoption_applications'

    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    applicant_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    experience_with_pets = db.Column(db.Text)
    living_situation = db.Column(db.String(200))
    application_status = db.Column(db.String(50), default='pending')  # pending, approved, rejected
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)

    # Relationship
    pet = db.relationship('Pet', backref=db.backref('applications', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'pet_id': self.pet_id,
            'pet_name': self.pet.name if self.pet else 'Unknown',
            'applicant_name': self.applicant_name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'experience_with_pets': self.experience_with_pets,
            'living_situation': self.living_situation,
            'application_status': self.application_status,
            'application_date': self.application_date.strftime('%Y-%m-%d %H:%M') if self.application_date else None,
            'notes': self.notes
        }

class Donation(db.Model):
    __tablename__ = 'donations'

    id = db.Column(db.Integer, primary_key=True)
    donor_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    transaction_id = db.Column(db.String(100))
    donation_date = db.Column(db.DateTime, default=datetime.utcnow)
    purpose = db.Column(db.String(200))
    status = db.Column(db.String(50), default='completed')  # pending, completed, failed
    notes = db.Column(db.Text)

# Load the trained model
model = pickle.load(open('model.pkl', 'rb'))

# Load food dataset (JSON) once at startup
with open('food_data.json', 'r') as f:
    food_data = json.load(f)

# Helper functions for file uploads
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Database initialization function
def init_database():
    """Initialize database with sample data"""
    with app.app_context():
        db.create_all()

        # Check if we already have data
        if Pet.query.count() == 0:
            # Migrate data from JSON file if it exists
            try:
                with open('pets_data.json', 'r') as f:
                    pets_data = json.load(f)

                for pet_data in pets_data['pets']:
                    pet = Pet(
                        name=pet_data['name'],
                        type=pet_data['type'],
                        breed=pet_data['breed'],
                        age=pet_data['age'],
                        gender=pet_data['gender'],
                        size=pet_data['size'],
                        color=pet_data['color'],
                        description=pet_data['description'],
                        health_status=pet_data['health_status'],
                        vaccination_status=pet_data['vaccination_status'],
                        spayed_neutered=pet_data['spayed_neutered'],
                        special_needs=pet_data['special_needs'],
                        adoption_fee=pet_data['adoption_fee'],
                        contact_info=pet_data['contact_info'],
                        location=pet_data['location'],
                        image=pet_data['image']
                    )
                    db.session.add(pet)

                db.session.commit()
                print("Database initialized with sample data from JSON file!")

            except FileNotFoundError:
                print("No existing pets data found. Database initialized empty.")

# Calculate statistics from JSON data
def get_food_stats():
    total_records = len(food_data)

    # Count by brand
    brand_counts = collections.Counter([item['brand'] for item in food_data])

    # Count by life stage
    life_stage_counts = collections.Counter([item['lifeStage'] for item in food_data])

    # Count by animal size
    animal_size_counts = collections.Counter([item['animalSize'] for item in food_data])

    # Count by condition (if not null)
    condition_counts = collections.Counter([item['condition'] for item in food_data if item['condition']])

    return {
        'total_records': total_records,
        'brand_counts': dict(brand_counts),
        'life_stage_counts': dict(life_stage_counts),
        'animal_size_counts': dict(animal_size_counts),
        'condition_counts': dict(condition_counts)
    }

@app.route('/')
def home():
    # Get statistics from JSON data
    stats = get_food_stats()

    return render_template(
        'home.html',
        total_records=stats['total_records'],
        brand_counts=stats['brand_counts'],
        life_stage_counts=stats['life_stage_counts']
    )

@app.route('/dashboard')
def dashboard():
    # Get statistics from JSON data
    stats = get_food_stats()

    return render_template(
        'dashboard.html',
        total_records=stats['total_records'],
        brand_counts=stats['brand_counts'],
        life_stage_counts=stats['life_stage_counts'],
        animal_size_counts=stats['animal_size_counts'],
        condition_counts=stats['condition_counts']
    )

@app.route('/food_recommendation')
def food_recommendation():
    return render_template('food.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        age = int(request.form['age'])
        weight = int(request.form['weight'])
        pet_type = request.form['type']
        activity = request.form['activity']

        # Get multiple health conditions (returns a list)
        health_conditions = request.form.getlist('health_conditions')

        # Encoding categorical values
        type_encoded = {'dog': 0, 'cat': 1}[pet_type.lower()]
        activity_encoded = {'low': 0, 'medium': 1, 'high': 2}[activity.lower()]

        # Prepare input for prediction
        input_data = np.array([[age, weight, type_encoded, activity_encoded]])

        # Model prediction (should return a string _id like '001', '002')
        prediction = model.predict(input_data)[0]

        # Find foods that match the criteria
        matching_foods = []

        # First, try to find foods that match both the model prediction and health conditions
        if health_conditions:
            # Look for foods with any of the selected health conditions
            for item in food_data:
                # Determine if this is a dog or cat food based on ID
                item_pet_type = 'dog' if int(item['_id']) <= 100 else 'cat'

                # Only consider foods that match the pet type
                if item_pet_type.lower() == pet_type.lower():
                    # Check if the food's condition matches any of the selected health conditions
                    if (item['condition'] and item['condition'] in health_conditions and
                        (item['lifeStage'] == 'All' or determine_life_stage(age, pet_type) == item['lifeStage']) and
                        (item['animalSize'] == 'All' or determine_size(weight, pet_type) == item['animalSize'])):
                        matching_foods.append(item)

        # If no matches with health condition, or no health condition specified, use model prediction
        if not matching_foods:
            # Find the food item with matching _id from model prediction
            recommended_food = next((item for item in food_data if item['_id'] == prediction), None)

            # Verify that the recommended food matches the pet type
            if recommended_food:
                item_pet_type = 'dog' if int(recommended_food['_id']) <= 100 else 'cat'
                if item_pet_type.lower() == pet_type.lower():
                    matching_foods.append(recommended_food)
                else:
                    # If pet types don't match, find a food with the correct pet type
                    for item in food_data:
                        item_pet_type = 'dog' if int(item['_id']) <= 100 else 'cat'
                        if item_pet_type.lower() == pet_type.lower():
                            matching_foods.append(item)
                            break

        # If still no matches, find any foods that match the pet type, life stage, and size
        if not matching_foods:
            life_stage = determine_life_stage(age, pet_type)
            size = determine_size(weight, pet_type)

            for item in food_data:
                # Determine if this is a dog or cat food based on ID
                item_pet_type = 'dog' if int(item['_id']) <= 100 else 'cat'

                # Only consider foods that match the pet type
                if item_pet_type.lower() == pet_type.lower():
                    if ((item['lifeStage'] == 'All' or item['lifeStage'] == life_stage) and
                        (item['animalSize'] == 'All' or item['animalSize'] == size)):
                        matching_foods.append(item)
                        # Limit to 3 recommendations
                        if len(matching_foods) >= 3:
                            break

        if not matching_foods:
            return render_template('food_results.html',
                                  pet_type=pet_type,
                                  recommendations=[],
                                  error_message="No matching food found for your pet's profile.")

        # Create a list of recommendations
        recommendations = []
        for food in matching_foods[:3]:  # Limit to top 3 recommendations
            recommendations.append({
                'food_name': food['name'],
                'brand': food['brand'],
                'price': food['price'],
                'calories': food['calories'],
                'life_stage': food['lifeStage'],
                'animal_size': food['animalSize'],
                'breed': food['breed'],
                'image_url': food['picture'],
                'special_needs': food['condition'] if food['condition'] else 'None',
                'rating': 4.5,  # Placeholder rating
                'rating_count': 120,  # Placeholder rating count
                'purchase_link': '#'  # Placeholder purchase link
            })

        return render_template('food_results.html',
                              pet_type=pet_type,
                              recommendations=recommendations,
                              health_conditions=health_conditions)

    except Exception as e:
        return render_template('food.html', error_message=f"Error: {str(e)}")

def determine_life_stage(age, pet_type='dog'):
    """Determine life stage based on age in months and pet type"""
    if pet_type.lower() == 'dog':
        if age < 12:
            return "Puppy"
        elif age > 84:  # 7 years
            return "Senior"
        else:
            return "Adult"
    elif pet_type.lower() == 'cat':
        if age < 12:
            return "Kitten"
        elif age > 132:  # 11 years
            return "Senior"
        else:
            return "Adult"
    else:
        # Default to dog life stages
        if age < 12:
            return "Puppy"
        elif age > 84:
            return "Senior"
        else:
            return "Adult"

def determine_size(weight, pet_type):
    """Determine size category based on weight and pet type"""
    if pet_type.lower() == 'dog':
        if weight < 10:
            return "X-Small"
        elif weight < 25:
            return "Small"
        elif weight < 50:
            return "Medium"
        elif weight < 90:
            return "Large"
        else:
            return "Giant"
    elif pet_type.lower() == 'cat':
        return "Small"  # Most cats are considered small
    else:
        return "Small"  # Default for other pets

@app.route('/adoption')
def adoption():
    pets = Pet.query.filter_by(status='available').all()
    pets_dict = [pet.to_dict() for pet in pets]
    return render_template('adoption.html', pets=pets_dict)

@app.route('/adopt/<int:pet_id>', methods=['GET', 'POST'])
def adopt_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)

    if request.method == 'POST':
        try:
            # Create new adoption application
            application = AdoptionApplication(
                pet_id=pet_id,
                applicant_name=request.form['applicant_name'],
                email=request.form['email'],
                phone=request.form['phone'],
                address=request.form['address'],
                experience_with_pets=request.form.get('experience_with_pets', ''),
                living_situation=request.form.get('living_situation', ''),
                notes=request.form.get('notes', '')
            )

            db.session.add(application)
            db.session.commit()

            # Return success response for AJAX
            return render_template('adoption_confirmation.html',
                                 pet=pet.to_dict(),
                                 application=application.to_dict())

        except Exception as e:
            db.session.rollback()
            flash(f'Error submitting application: {str(e)}', 'error')

    return render_template('adopt_form.html', pet=pet.to_dict())

@app.route('/donation')
def donation():
    return render_template('donation.html')

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        # Get form data
        owner_name = request.form.get('owner_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        pet_name = request.form.get('pet_name')
        pet_type = request.form.get('pet_type')
        pet_age = request.form.get('pet_age')
        age_unit = request.form.get('age_unit')
        appointment_type = request.form.get('appointment_type')
        appointment_date = request.form.get('appointment_date')
        appointment_time = request.form.get('appointment_time')
        notes = request.form.get('notes')

        # Validate required fields
        required_fields = {
            'owner_name': owner_name,
            'email': email,
            'phone': phone,
            'pet_name': pet_name,
            'pet_type': pet_type,
            'pet_age': pet_age,
            'appointment_type': appointment_type,
            'appointment_date': appointment_date,
            'appointment_time': appointment_time
        }

        for field_name, field_value in required_fields.items():
            if not field_value:
                appointment_data = {
                    'owner_name': owner_name,
                    'email': email,
                    'phone': phone,
                    'pet_name': pet_name,
                    'pet_type': pet_type,
                    'pet_age': pet_age,
                    'age_unit': age_unit,
                    'appointment_type': appointment_type,
                    'appointment_date': appointment_date,
                    'appointment_time': appointment_time,
                    'notes': notes
                }
                return render_template('appointment.html',
                                      error_message=f"Please fill in the {field_name.replace('_', ' ')} field.",
                                      appointment_data=appointment_data)

        try:
            # Convert time slot to actual time
            time_mapping = {
                'morning': '10:00',
                'afternoon': '14:00',
                'evening': '18:00'
            }
            actual_time = time_mapping.get(appointment_time, '10:00')

            # Create new appointment in database
            new_appointment = Appointment(
                owner_name=owner_name,
                email=email,
                phone=phone,
                pet_name=pet_name,
                pet_type=pet_type,
                pet_age=pet_age,
                age_unit=age_unit,
                appointment_type=appointment_type,
                appointment_date=datetime.strptime(appointment_date, '%Y-%m-%d').date(),
                appointment_time=datetime.strptime(actual_time, '%H:%M').time(),
                notes=notes
            )

            db.session.add(new_appointment)
            db.session.commit()

            # Get the saved appointment data for confirmation
            appointment_data = new_appointment.to_dict()

            flash('Appointment booked successfully!', 'success')
            return render_template('appointment_confirmation.html', appointment_data=appointment_data)

        except Exception as e:
            db.session.rollback()
            return render_template('appointment.html',
                                  error_message=f"Error booking appointment: {str(e)}")

    # For GET requests, show the appointment form
    return render_template('appointment.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/test-location')
def test_location():
    return render_template('test_location.html')

@app.route('/nearby-services')
def nearby_services():
    # Sample data for Bangalore locations
    veterinary_hospitals = [
        # Central Bangalore
        {
            'name': 'Cessna Lifeline Veterinary Hospital',
            'address': '47, 80 Feet Rd, Koramangala 4th Block, Bangalore - 560034',
            'phone': '+91 80 4112 4444',
            'rating': 4.5,
            'distance': '2.3 km',
            'services': ['Emergency Care', '24/7 Service', 'Surgery', 'Vaccination'],
            'timings': '24 Hours',
            'lat': 12.9352,
            'lng': 77.6245
        },
        {
            'name': 'Vets Plus Animal Hospital',
            'address': '1st Floor, 100 Feet Rd, Indiranagar, Bangalore - 560038',
            'phone': '+91 80 2520 2020',
            'rating': 4.3,
            'distance': '3.1 km',
            'services': ['General Checkup', 'Grooming', 'Dental Care', 'X-Ray'],
            'timings': '9:00 AM - 9:00 PM',
            'lat': 12.9716,
            'lng': 77.6412
        },
        {
            'name': 'MG Road Pet Clinic',
            'address': 'Brigade Road, MG Road, Bangalore - 560001',
            'phone': '+91 80 2558 9999',
            'rating': 4.1,
            'distance': '4.2 km',
            'services': ['General Care', 'Vaccination', 'Emergency Care', 'Consultation'],
            'timings': '9:00 AM - 8:00 PM',
            'lat': 12.9716,
            'lng': 77.6103
        },
        {
            'name': 'Commercial Street Vet Hospital',
            'address': 'Commercial Street, Bangalore - 560001',
            'phone': '+91 80 2559 1234',
            'rating': 4.0,
            'distance': '3.8 km',
            'services': ['Pet Surgery', 'Vaccination', 'Health Checkup', 'Grooming'],
            'timings': '10:00 AM - 7:00 PM',
            'lat': 12.9716,
            'lng': 77.6103
        },

        # South Bangalore
        {
            'name': 'Animal Care Veterinary Clinic',
            'address': 'JP Nagar 7th Phase, Bangalore - 560078',
            'phone': '+91 80 2659 8888',
            'rating': 4.2,
            'distance': '4.5 km',
            'services': ['Pet Surgery', 'Vaccination', 'Health Checkup', 'Boarding'],
            'timings': '10:00 AM - 8:00 PM',
            'lat': 12.8956,
            'lng': 77.5850
        },
        {
            'name': 'HSR Layout Animal Hospital',
            'address': 'Sector 2, HSR Layout, Bangalore - 560102',
            'phone': '+91 80 4567 8901',
            'rating': 4.3,
            'distance': '5.1 km',
            'services': ['24/7 Emergency', 'Surgery', 'Vaccination', 'Health Checkup'],
            'timings': '24 Hours',
            'lat': 12.9116,
            'lng': 77.6400
        },
        {
            'name': 'Banashankari Pet Clinic',
            'address': '3rd Stage, Banashankari, Bangalore - 560085',
            'phone': '+91 80 2672 3456',
            'rating': 4.1,
            'distance': '6.7 km',
            'services': ['General Care', 'Grooming', 'Dental Care', 'Boarding'],
            'timings': '9:00 AM - 8:00 PM',
            'lat': 12.9250,
            'lng': 77.5667
        },
        {
            'name': 'Jayanagar Veterinary Hospital',
            'address': '4th Block, Jayanagar, Bangalore - 560011',
            'phone': '+91 80 2665 7890',
            'rating': 4.2,
            'distance': '5.8 km',
            'services': ['Emergency Care', 'Surgery', 'Vaccination', 'Lab Tests'],
            'timings': '8:00 AM - 9:00 PM',
            'lat': 12.9279,
            'lng': 77.5937
        },
        {
            'name': 'BTM Layout Pet Care',
            'address': '2nd Stage, BTM Layout, Bangalore - 560076',
            'phone': '+91 80 2661 2345',
            'rating': 4.0,
            'distance': '6.2 km',
            'services': ['General Care', 'Vaccination', 'Grooming', 'Consultation'],
            'timings': '9:00 AM - 8:00 PM',
            'lat': 12.9165,
            'lng': 77.6101
        },

        # North Bangalore - Specific Areas
        # Mathikere
        {
            'name': 'Mathikere Pet Care Clinic',
            'address': 'BEL Road, Mathikere, Bangalore - 560054',
            'phone': '+91 80 2839 5678',
            'rating': 4.3,
            'distance': '2.1 km',
            'services': ['General Care', 'Vaccination', 'Emergency Care', 'Surgery'],
            'timings': '9:00 AM - 8:00 PM',
            'lat': 13.0358,
            'lng': 77.5700
        },
        {
            'name': 'BEL Road Animal Hospital',
            'address': 'Near BEL Circle, Mathikere, Bangalore - 560054',
            'phone': '+91 80 2839 1234',
            'rating': 4.1,
            'distance': '2.3 km',
            'services': ['Pet Surgery', 'Vaccination', 'Health Checkup', 'Grooming'],
            'timings': '10:00 AM - 7:00 PM',
            'lat': 13.0340,
            'lng': 77.5720
        },

        # Sanjay Nagar
        {
            'name': 'Sanjay Nagar Veterinary Clinic',
            'address': 'Sanjay Nagar Main Road, Bangalore - 560094',
            'phone': '+91 80 2361 7890',
            'rating': 4.4,
            'distance': '1.8 km',
            'services': ['24/7 Emergency', 'Surgery', 'Vaccination', 'Lab Tests'],
            'timings': '24 Hours',
            'lat': 13.0250,
            'lng': 77.5850
        },
        {
            'name': 'North Bangalore Pet Hospital',
            'address': '2nd Cross, Sanjay Nagar, Bangalore - 560094',
            'phone': '+91 80 2361 4567',
            'rating': 4.2,
            'distance': '1.9 km',
            'services': ['General Care', 'Dental Care', 'X-Ray', 'Boarding'],
            'timings': '8:00 AM - 9:00 PM',
            'lat': 13.0260,
            'lng': 77.5870
        },

        # Yelahanka
        {
            'name': 'Yelahanka New Town Vet Clinic',
            'address': 'Yelahanka New Town, Bangalore - 560064',
            'phone': '+91 80 2856 3456',
            'rating': 4.5,
            'distance': '3.2 km',
            'services': ['Emergency Care', 'Pet Surgery', 'Vaccination', 'Health Checkup'],
            'timings': '9:00 AM - 8:00 PM',
            'lat': 13.1007,
            'lng': 77.5963
        },
        {
            'name': 'Yelahanka Animal Care Center',
            'address': 'Doddaballapur Road, Yelahanka, Bangalore - 560064',
            'phone': '+91 80 2856 7890',
            'rating': 4.3,
            'distance': '3.5 km',
            'services': ['General Care', 'Grooming', 'Vaccination', 'Consultation'],
            'timings': '10:00 AM - 7:00 PM',
            'lat': 13.1020,
            'lng': 77.5980
        },

        # Hebbal
        {
            'name': 'Hebbal Veterinary Hospital',
            'address': 'Outer Ring Road, Hebbal, Bangalore - 560024',
            'phone': '+91 80 2846 5678',
            'rating': 4.6,
            'distance': '2.8 km',
            'services': ['24/7 Emergency', 'Surgery', 'Lab Tests', 'Boarding'],
            'timings': '24 Hours',
            'lat': 13.0358,
            'lng': 77.5970
        },
        {
            'name': 'Hebbal Pet Care Clinic',
            'address': 'Hebbal Main Road, Bangalore - 560024',
            'phone': '+91 80 2846 9012',
            'rating': 4.2,
            'distance': '2.9 km',
            'services': ['General Care', 'Vaccination', 'Dental Care', 'Grooming'],
            'timings': '9:00 AM - 8:00 PM',
            'lat': 13.0370,
            'lng': 77.5990
        },

        # R T Nagar
        {
            'name': 'R T Nagar Animal Hospital',
            'address': '16th Cross, R T Nagar, Bangalore - 560032',
            'phone': '+91 80 2341 2345',
            'rating': 4.4,
            'distance': '1.5 km',
            'services': ['Emergency Care', 'Pet Surgery', 'Vaccination', 'Health Checkup'],
            'timings': '8:00 AM - 9:00 PM',
            'lat': 13.0200,
            'lng': 77.5950
        },
        {
            'name': 'RT Nagar Pet Clinic',
            'address': 'BEL Road, R T Nagar, Bangalore - 560032',
            'phone': '+91 80 2341 6789',
            'rating': 4.1,
            'distance': '1.7 km',
            'services': ['General Care', 'Grooming', 'Vaccination', 'Consultation'],
            'timings': '10:00 AM - 7:00 PM',
            'lat': 13.0220,
            'lng': 77.5970
        },

        # Nagavara
        {
            'name': 'Nagavara Veterinary Center',
            'address': 'Nagavara Main Road, Bangalore - 560045',
            'phone': '+91 80 2847 3456',
            'rating': 4.3,
            'distance': '2.2 km',
            'services': ['Emergency Care', 'Surgery', 'Vaccination', 'Lab Tests'],
            'timings': '9:00 AM - 8:00 PM',
            'lat': 13.0450,
            'lng': 77.6100
        },

        # RMV 2nd Stage
        {
            'name': 'RMV Pet Care Hospital',
            'address': '2nd Stage, RMV Extension, Bangalore - 560094',
            'phone': '+91 80 2360 7890',
            'rating': 4.5,
            'distance': '1.2 km',
            'services': ['24/7 Emergency', 'Pet Surgery', 'Vaccination', 'Health Checkup'],
            'timings': '24 Hours',
            'lat': 13.0150,
            'lng': 77.5800
        },
        {
            'name': 'RMV Animal Clinic',
            'address': '60 Feet Road, RMV 2nd Stage, Bangalore - 560094',
            'phone': '+91 80 2360 4567',
            'rating': 4.2,
            'distance': '1.4 km',
            'services': ['General Care', 'Grooming', 'Dental Care', 'Boarding'],
            'timings': '9:00 AM - 8:00 PM',
            'lat': 13.0170,
            'lng': 77.5820
        },

        # Sadashiv Nagar
        {
            'name': 'Sadashiv Nagar Pet Hospital',
            'address': 'Sadashiv Nagar Main Road, Bangalore - 560080',
            'phone': '+91 80 2361 8901',
            'rating': 4.4,
            'distance': '1.6 km',
            'services': ['Emergency Care', 'Surgery', 'Vaccination', 'Lab Tests'],
            'timings': '8:00 AM - 9:00 PM',
            'lat': 13.0100,
            'lng': 77.5750
        },

        # CBI Bus Stop Area
        {
            'name': 'CBI Road Veterinary Clinic',
            'address': 'Near CBI Bus Stop, CBI Road, Bangalore - 560024',
            'phone': '+91 80 2847 5555',
            'rating': 4.3,
            'distance': '0.5 km',
            'services': ['General Care', 'Emergency Care', 'Vaccination', 'Pet Surgery'],
            'timings': '9:00 AM - 8:00 PM',
            'lat': 13.0400,
            'lng': 77.5950
        },
        {
            'name': 'Hebbal CBI Pet Hospital',
            'address': 'CBI Road, Near Bus Stop, Bangalore - 560024',
            'phone': '+91 80 2847 6666',
            'rating': 4.2,
            'distance': '0.3 km',
            'services': ['24/7 Emergency', 'Surgery', 'Lab Tests', 'Health Checkup'],
            'timings': '24 Hours',
            'lat': 13.0420,
            'lng': 77.5970
        },

        # East Bangalore
        {
            'name': 'Whitefield Veterinary Hospital',
            'address': 'ITPL Main Road, Whitefield, Bangalore - 560066',
            'phone': '+91 80 2845 6789',
            'rating': 4.4,
            'distance': '8.2 km',
            'services': ['Emergency Care', 'Pet Surgery', 'Vaccination', 'Lab Tests'],
            'timings': '8:00 AM - 10:00 PM',
            'lat': 12.9698,
            'lng': 77.7500
        },
        {
            'name': 'Marathahalli Pet Hospital',
            'address': 'Outer Ring Road, Marathahalli, Bangalore - 560037',
            'phone': '+91 80 2847 1234',
            'rating': 4.1,
            'distance': '9.8 km',
            'services': ['General Care', 'Vaccination', 'Grooming', 'Health Checkup'],
            'timings': '9:00 AM - 8:00 PM',
            'lat': 12.9591,
            'lng': 77.6974
        },
        {
            'name': 'Bellandur Animal Care',
            'address': 'Sarjapur Road, Bellandur, Bangalore - 560103',
            'phone': '+91 80 2844 5678',
            'rating': 4.0,
            'distance': '11.2 km',
            'services': ['Emergency Care', 'Surgery', 'Vaccination', 'Consultation'],
            'timings': '10:00 AM - 7:00 PM',
            'lat': 12.9259,
            'lng': 77.6648
        },

        # West Bangalore
        {
            'name': 'Vijayanagar Vet Clinic',
            'address': '2nd Stage, Vijayanagar, Bangalore - 560040',
            'phone': '+91 80 2330 9876',
            'rating': 4.1,
            'distance': '9.5 km',
            'services': ['General Care', 'Vaccination', 'Grooming', 'Emergency Care'],
            'timings': '9:00 AM - 8:00 PM',
            'lat': 12.9634,
            'lng': 77.5199
        },
        {
            'name': 'Basavanagudi Pet Hospital',
            'address': 'Bull Temple Road, Basavanagudi, Bangalore - 560004',
            'phone': '+91 80 2661 3456',
            'rating': 4.2,
            'distance': '7.3 km',
            'services': ['Pet Surgery', 'Vaccination', 'Health Checkup', 'Lab Tests'],
            'timings': '8:00 AM - 8:00 PM',
            'lat': 12.9423,
            'lng': 77.5741
        },

        # Outer Bangalore
        {
            'name': 'Electronic City Pet Hospital',
            'address': 'Phase 1, Electronic City, Bangalore - 560100',
            'phone': '+91 80 2783 4567',
            'rating': 4.2,
            'distance': '12.5 km',
            'services': ['Emergency Care', 'Surgery', 'Lab Tests', 'Boarding'],
            'timings': '9:00 AM - 9:00 PM',
            'lat': 12.8456,
            'lng': 77.6603
        },
        {
            'name': 'Sarjapur Road Animal Hospital',
            'address': 'Sarjapur Road, Bangalore - 560035',
            'phone': '+91 80 2843 7890',
            'rating': 4.0,
            'distance': '13.8 km',
            'services': ['General Care', 'Vaccination', 'Emergency Care', 'Consultation'],
            'timings': '9:00 AM - 7:00 PM',
            'lat': 12.9010,
            'lng': 77.6953
        },
        {
            'name': 'Yelahanka Veterinary Clinic',
            'address': 'New Town, Yelahanka, Bangalore - 560064',
            'phone': '+91 80 2856 1234',
            'rating': 4.1,
            'distance': '18.2 km',
            'services': ['Pet Surgery', 'Vaccination', 'Health Checkup', 'Grooming'],
            'timings': '10:00 AM - 8:00 PM',
            'lat': 13.1007,
            'lng': 77.5963
        }
    ]

    pet_pharmacies = [
        # North Bangalore Pharmacies - Specific Areas
        # Mathikere
        {
            'name': 'Mathikere Pet Pharmacy',
            'address': 'BEL Road, Mathikere, Bangalore - 560054',
            'phone': '+91 80 2839 9876',
            'rating': 4.2,
            'distance': '2.0 km',
            'services': ['Prescription Medicines', 'Pet Vaccines', 'Flea Control', 'Health Supplements'],
            'timings': '9:00 AM - 8:00 PM',
            'lat': 13.0358,
            'lng': 77.5700
        },

        # Sanjay Nagar
        {
            'name': 'Sanjay Nagar Animal Pharmacy',
            'address': 'Sanjay Nagar Main Road, Bangalore - 560094',
            'phone': '+91 80 2361 5432',
            'rating': 4.3,
            'distance': '1.7 km',
            'services': ['Emergency Medicines', 'Veterinary Drugs', 'Pet Nutrition', 'First Aid Kits'],
            'timings': '8:00 AM - 9:00 PM',
            'lat': 13.0250,
            'lng': 77.5850
        },

        # Yelahanka
        {
            'name': 'Yelahanka Pet Medicine Store',
            'address': 'Yelahanka New Town, Bangalore - 560064',
            'phone': '+91 80 2856 2468',
            'rating': 4.1,
            'distance': '3.1 km',
            'services': ['Prescription Drugs', 'Pet Vitamins', 'Dewormers', 'Grooming Products'],
            'timings': '9:30 AM - 8:30 PM',
            'lat': 13.1007,
            'lng': 77.5963
        },

        # Hebbal
        {
            'name': 'Hebbal Animal Health Pharmacy',
            'address': 'Outer Ring Road, Hebbal, Bangalore - 560024',
            'phone': '+91 80 2846 1357',
            'rating': 4.4,
            'distance': '2.7 km',
            'services': ['24/7 Emergency Medicines', 'Pet Vaccines', 'Lab Supplies', 'Health Products'],
            'timings': '24 Hours',
            'lat': 13.0358,
            'lng': 77.5970
        },

        # R T Nagar
        {
            'name': 'RT Nagar Pet Pharmacy',
            'address': '16th Cross, R T Nagar, Bangalore - 560032',
            'phone': '+91 80 2341 9753',
            'rating': 4.2,
            'distance': '1.4 km',
            'services': ['Prescription Medicines', 'Pet Supplements', 'Flea & Tick Control', 'Wound Care'],
            'timings': '9:00 AM - 8:00 PM',
            'lat': 13.0200,
            'lng': 77.5950
        },

        # Nagavara
        {
            'name': 'Nagavara Pet Medicine Center',
            'address': 'Nagavara Main Road, Bangalore - 560045',
            'phone': '+91 80 2847 8642',
            'rating': 4.0,
            'distance': '2.1 km',
            'services': ['Veterinary Medicines', 'Pet Nutrition', 'Health Supplements', 'First Aid'],
            'timings': '10:00 AM - 7:00 PM',
            'lat': 13.0450,
            'lng': 77.6100
        },

        # RMV 2nd Stage
        {
            'name': 'RMV Pet Pharmacy',
            'address': '2nd Stage, RMV Extension, Bangalore - 560094',
            'phone': '+91 80 2360 1975',
            'rating': 4.3,
            'distance': '1.1 km',
            'services': ['Emergency Medicines', 'Pet Vaccines', 'Prescription Drugs', 'Health Products'],
            'timings': '8:30 AM - 9:30 PM',
            'lat': 13.0150,
            'lng': 77.5800
        },

        # Sadashiv Nagar
        {
            'name': 'Sadashiv Nagar Animal Pharmacy',
            'address': 'Sadashiv Nagar Main Road, Bangalore - 560080',
            'phone': '+91 80 2361 3698',
            'rating': 4.1,
            'distance': '1.5 km',
            'services': ['Prescription Medicines', 'Pet Vitamins', 'Dewormers', 'Skin Care Products'],
            'timings': '9:00 AM - 8:00 PM',
            'lat': 13.0100,
            'lng': 77.5750
        },

        # CBI Bus Stop Area
        {
            'name': 'CBI Road Pet Pharmacy',
            'address': 'Near CBI Bus Stop, CBI Road, Bangalore - 560024',
            'phone': '+91 80 2847 7777',
            'rating': 4.4,
            'distance': '0.2 km',
            'services': ['Emergency Medicines', 'Pet Vaccines', 'Prescription Drugs', 'First Aid Kits'],
            'timings': '8:00 AM - 9:00 PM',
            'lat': 13.0400,
            'lng': 77.5950
        },
        {
            'name': 'Hebbal CBI Animal Pharmacy',
            'address': 'CBI Road, Opposite Bus Stop, Bangalore - 560024',
            'phone': '+91 80 2847 8888',
            'rating': 4.3,
            'distance': '0.4 km',
            'services': ['24/7 Emergency Medicines', 'Pet Nutrition', 'Health Supplements', 'Grooming Products'],
            'timings': '24 Hours',
            'lat': 13.0420,
            'lng': 77.5970
        },

        # Additional Central Bangalore Pharmacies
        {
            'name': 'PetCare Pharmacy',
            'address': 'Commercial Street, Bangalore - 560001',
            'phone': '+91 80 2558 7777',
            'rating': 4.4,
            'distance': '1.8 km',
            'services': ['Prescription Medicines', 'Supplements', 'Flea Control', 'Dewormers'],
            'timings': '9:00 AM - 9:00 PM',
            'lat': 12.9716,
            'lng': 77.6103
        },
        {
            'name': 'Koramangala Pet Pharmacy',
            'address': '5th Block, Koramangala, Bangalore - 560095',
            'phone': '+91 80 2553 4567',
            'rating': 4.3,
            'distance': '2.1 km',
            'services': ['Emergency Medicines', 'Pet Vaccines', 'Health Supplements', 'Grooming Products'],
            'timings': '8:00 AM - 10:00 PM',
            'lat': 12.9352,
            'lng': 77.6245
        }
    ]

    pet_shops = [
        # North Bangalore Pet Shops - Specific Areas
        # Mathikere
        {
            'name': 'Mathikere Pet World',
            'address': 'BEL Road, Mathikere, Bangalore - 560054',
            'phone': '+91 80 2839 7531',
            'rating': 4.2,
            'distance': '2.0 km',
            'services': ['Pet Food', 'Toys & Accessories', 'Grooming Supplies', 'Pet Bedding'],
            'timings': '9:00 AM - 8:00 PM',
            'lat': 13.0358,
            'lng': 77.5700
        },

        # Sanjay Nagar
        {
            'name': 'Sanjay Nagar Pet Store',
            'address': 'Sanjay Nagar Main Road, Bangalore - 560094',
            'phone': '+91 80 2361 8642',
            'rating': 4.3,
            'distance': '1.6 km',
            'services': ['Premium Pet Food', 'Training Equipment', 'Pet Toys', 'Health Products'],
            'timings': '9:30 AM - 9:00 PM',
            'lat': 13.0250,
            'lng': 77.5850
        },

        # Yelahanka
        {
            'name': 'Yelahanka Pet Corner',
            'address': 'Yelahanka New Town, Bangalore - 560064',
            'phone': '+91 80 2856 9753',
            'rating': 4.1,
            'distance': '3.0 km',
            'services': ['Pet Food', 'Grooming Tools', 'Pet Carriers', 'Bird Accessories'],
            'timings': '10:00 AM - 8:00 PM',
            'lat': 13.1007,
            'lng': 77.5963
        },

        # Hebbal
        {
            'name': 'Hebbal Pet Mart',
            'address': 'Outer Ring Road, Hebbal, Bangalore - 560024',
            'phone': '+91 80 2846 4826',
            'rating': 4.4,
            'distance': '2.6 km',
            'services': ['Imported Pet Food', 'Designer Pet Clothing', 'Interactive Toys', 'Aquarium Products'],
            'timings': '9:00 AM - 9:00 PM',
            'lat': 13.0358,
            'lng': 77.5970
        },

        # R T Nagar
        {
            'name': 'RT Nagar Pet Shop',
            'address': '16th Cross, R T Nagar, Bangalore - 560032',
            'phone': '+91 80 2341 5937',
            'rating': 4.2,
            'distance': '1.3 km',
            'services': ['Pet Food', 'Toys & Accessories', 'Grooming Supplies', 'Pet Care Books'],
            'timings': '9:00 AM - 8:00 PM',
            'lat': 13.0200,
            'lng': 77.5950
        },

        # Nagavara
        {
            'name': 'Nagavara Pet Paradise',
            'address': 'Nagavara Main Road, Bangalore - 560045',
            'phone': '+91 80 2847 1593',
            'rating': 4.0,
            'distance': '2.0 km',
            'services': ['Organic Pet Food', 'Natural Treats', 'Eco-friendly Toys', 'Pet Bedding'],
            'timings': '10:00 AM - 7:00 PM',
            'lat': 13.0450,
            'lng': 77.6100
        },

        # RMV 2nd Stage
        {
            'name': 'RMV Pet Store',
            'address': '2nd Stage, RMV Extension, Bangalore - 560094',
            'phone': '+91 80 2360 7418',
            'rating': 4.3,
            'distance': '1.0 km',
            'services': ['Premium Pet Food', 'Training Equipment', 'Pet Toys', 'Grooming Services'],
            'timings': '9:00 AM - 9:00 PM',
            'lat': 13.0150,
            'lng': 77.5800
        },

        # Sadashiv Nagar
        {
            'name': 'Sadashiv Nagar Pet World',
            'address': 'Sadashiv Nagar Main Road, Bangalore - 560080',
            'phone': '+91 80 2361 2847',
            'rating': 4.1,
            'distance': '1.4 km',
            'services': ['Pet Food', 'Toys & Accessories', 'Pet Clothing', 'Health Supplements'],
            'timings': '9:30 AM - 8:30 PM',
            'lat': 13.0100,
            'lng': 77.5750
        },

        # CBI Bus Stop Area
        {
            'name': 'CBI Road Pet Store',
            'address': 'Near CBI Bus Stop, CBI Road, Bangalore - 560024',
            'phone': '+91 80 2847 9999',
            'rating': 4.5,
            'distance': '0.1 km',
            'services': ['Premium Pet Food', 'Toys & Accessories', 'Pet Carriers', 'Training Equipment'],
            'timings': '9:00 AM - 9:00 PM',
            'lat': 13.0400,
            'lng': 77.5950
        },
        {
            'name': 'Hebbal CBI Pet Mart',
            'address': 'CBI Road, Next to Bus Stop, Bangalore - 560024',
            'phone': '+91 80 2847 1010',
            'rating': 4.3,
            'distance': '0.3 km',
            'services': ['Pet Food', 'Grooming Supplies', 'Pet Beds', 'Health Products'],
            'timings': '8:30 AM - 8:30 PM',
            'lat': 13.0420,
            'lng': 77.5970
        },
        {
            'name': 'CBI Junction Pet Corner',
            'address': 'CBI Road Junction, Near Bus Stop, Bangalore - 560024',
            'phone': '+91 80 2847 2020',
            'rating': 4.2,
            'distance': '0.2 km',
            'services': ['Imported Pet Food', 'Designer Toys', 'Pet Clothing', 'Aquarium Supplies'],
            'timings': '10:00 AM - 8:00 PM',
            'lat': 13.0410,
            'lng': 77.5960
        },

        # Additional Popular Pet Shops
        {
            'name': 'Petzone - The Pet Store',
            'address': 'Forum Mall, Koramangala, Bangalore - 560095',
            'phone': '+91 80 4112 5555',
            'rating': 4.6,
            'distance': '2.1 km',
            'services': ['Pet Food', 'Toys & Accessories', 'Grooming Supplies', 'Pet Clothing'],
            'timings': '10:00 AM - 10:00 PM',
            'lat': 12.9279,
            'lng': 77.6271
        },
        {
            'name': 'Paws & Claws Pet Shop',
            'address': 'Indiranagar 100 Feet Road, Bangalore - 560038',
            'phone': '+91 80 2520 1234',
            'rating': 4.4,
            'distance': '3.1 km',
            'services': ['Premium Dog Food', 'Cat Supplies', 'Bird Accessories', 'Aquarium Products'],
            'timings': '9:30 AM - 9:30 PM',
            'lat': 12.9716,
            'lng': 77.6412
        }
    ]

    return render_template('nearby_services.html',
                         veterinary_hospitals=veterinary_hospitals,
                         pet_pharmacies=pet_pharmacies,
                         pet_shops=pet_shops)

@app.route('/admin')
def admin_page():
    try:
        pets_count = Pet.query.count()
        appointments_count = Appointment.query.count()
        pending_appointments = Appointment.query.filter_by(status='pending').count()
        return render_template('admin_page.html',
                             pets_count=pets_count,
                             appointments_count=appointments_count,
                             pending_appointments=pending_appointments)
    except Exception as e:
        # If database tables don't exist yet, show basic page
        return render_template('admin_page.html',
                             pets_count=0,
                             appointments_count=0,
                             pending_appointments=0)

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Successfully logged in as admin!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials!', 'error')

    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Successfully logged out!', 'success')
    return redirect(url_for('home'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        flash('Please log in to access admin panel!', 'error')
        return redirect(url_for('admin_login'))

    pets = Pet.query.all()
    pets_dict = [pet.to_dict() for pet in pets]

    # Get counts and recent items
    try:
        total_appointments = Appointment.query.count()
        pending_appointments = Appointment.query.filter_by(status='pending').count()
        recent_appointments = Appointment.query.order_by(Appointment.created_at.desc()).limit(5).all()
    except Exception as e:
        total_appointments = 0
        pending_appointments = 0
        recent_appointments = []

    try:
        total_adoptions = AdoptionApplication.query.count()
        pending_adoptions = AdoptionApplication.query.filter_by(application_status='pending').count()
        recent_adoptions = AdoptionApplication.query.order_by(AdoptionApplication.application_date.desc()).limit(5).all()
    except Exception as e:
        total_adoptions = 0
        pending_adoptions = 0
        recent_adoptions = []

    return render_template('admin/dashboard.html',
                         pets=pets_dict,
                         total_appointments=total_appointments,
                         pending_appointments=pending_appointments,
                         total_adoptions=total_adoptions,
                         pending_adoptions=pending_adoptions,
                         unread_appointments=pending_appointments,
                         unread_adoptions=pending_adoptions,
                         recent_appointments=recent_appointments,
                         recent_adoptions=recent_adoptions)

@app.route('/admin/pets/add', methods=['GET', 'POST'])
def admin_add_pet():
    if not session.get('admin_logged_in'):
        flash('Please log in to access admin panel!', 'error')
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        # Handle file upload
        image_filename = 'default_pet.jpg'
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to filename to avoid conflicts
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_filename = filename

        try:
            # Create new pet in database
            new_pet = Pet(
                name=request.form['name'],
                type=request.form['type'],
                breed=request.form['breed'],
                age=request.form['age'],
                gender=request.form['gender'],
                size=request.form['size'],
                color=request.form['color'],
                description=request.form['description'],
                health_status=request.form['health_status'],
                vaccination_status=request.form['vaccination_status'],
                spayed_neutered=request.form.get('spayed_neutered') == 'on',
                special_needs=request.form['special_needs'],
                adoption_fee=int(request.form['adoption_fee']),
                contact_info=request.form['contact_info'],
                location=request.form['location'],
                image=image_filename
            )

            db.session.add(new_pet)
            db.session.commit()

            flash('Pet added successfully!', 'success')
            return redirect(url_for('admin_dashboard'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error adding pet: {str(e)}', 'error')
            return render_template('admin/add_pet.html')

    return render_template('admin/add_pet.html')

@app.route('/admin/pets/edit/<int:pet_id>', methods=['GET', 'POST'])
def admin_edit_pet(pet_id):
    if not session.get('admin_logged_in'):
        flash('Please log in to access admin panel!', 'error')
        return redirect(url_for('admin_login'))

    pet = Pet.query.get_or_404(pet_id)

    if not pet:
        flash('Pet not found!', 'error')
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        try:
            # Handle file upload
            image_filename = pet.image  # Keep existing image by default
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename != '' and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    # Add timestamp to filename to avoid conflicts
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                    filename = timestamp + filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image_filename = filename

            # Update pet data
            pet.name = request.form['name']
            pet.type = request.form['type']
            pet.breed = request.form['breed']
            pet.age = request.form['age']
            pet.gender = request.form['gender']
            pet.size = request.form['size']
            pet.color = request.form['color']
            pet.description = request.form['description']
            pet.health_status = request.form['health_status']
            pet.vaccination_status = request.form['vaccination_status']
            pet.spayed_neutered = request.form.get('spayed_neutered') == 'on'
            pet.special_needs = request.form['special_needs']
            pet.adoption_fee = int(request.form['adoption_fee'])
            pet.contact_info = request.form['contact_info']
            pet.location = request.form['location']
            pet.image = image_filename

            db.session.commit()
            flash('Pet updated successfully!', 'success')
            return redirect(url_for('admin_dashboard'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error updating pet: {str(e)}', 'error')

    return render_template('admin/edit_pet.html', pet=pet.to_dict())

@app.route('/admin/pets/delete/<int:pet_id>', methods=['POST'])
def admin_delete_pet(pet_id):
    if not session.get('admin_logged_in'):
        flash('Please log in to access admin panel!', 'error')
        return redirect(url_for('admin_login'))

    try:
        pet = Pet.query.get_or_404(pet_id)
        db.session.delete(pet)
        db.session.commit()
        flash('Pet deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting pet: {str(e)}', 'error')

    return redirect(url_for('admin_dashboard'))

@app.route('/admin/appointments')
def admin_appointments():
    if not session.get('admin_logged_in'):
        flash('Please log in to access admin panel!', 'error')
        return redirect(url_for('admin_login'))

    appointments = Appointment.query.order_by(Appointment.appointment_date.desc()).all()
    appointments_dict = [appointment.to_dict() for appointment in appointments]
    return render_template('admin/appointments.html', appointments=appointments_dict)

@app.route('/admin/appointments/update/<int:appointment_id>', methods=['POST'])
def admin_update_appointment_status(appointment_id):
    if not session.get('admin_logged_in'):
        flash('Please log in to access admin panel!', 'error')
        return redirect(url_for('admin_login'))

    try:
        appointment = Appointment.query.get_or_404(appointment_id)
        new_status = request.form.get('status')
        appointment.status = new_status
        db.session.commit()
        flash(f'Appointment status updated to {new_status}!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating appointment: {str(e)}', 'error')

    return redirect(url_for('admin_appointments'))

@app.route('/admin/adoptions')
def admin_adoptions():
    if not session.get('admin_logged_in'):
        flash('Please log in to access admin panel!', 'error')
        return redirect(url_for('admin_login'))

    adoptions = AdoptionApplication.query.order_by(AdoptionApplication.application_date.desc()).all()
    adoptions_dict = [adoption.to_dict() for adoption in adoptions]
    return render_template('admin/adoptions.html', adoptions=adoptions_dict)

@app.route('/admin/adoptions/<int:adoption_id>')
def admin_adoption_details(adoption_id):
    if not session.get('admin_logged_in'):
        flash('Please log in to access admin panel!', 'error')
        return redirect(url_for('admin_login'))

    adoption = AdoptionApplication.query.get_or_404(adoption_id)

    # Skip marking as read for now (will implement later)

    return render_template('admin/adoption_details.html', adoption=adoption.to_dict())

@app.route('/admin/adoptions/update/<int:adoption_id>', methods=['POST'])
def admin_update_adoption_status(adoption_id):
    if not session.get('admin_logged_in'):
        flash('Please log in to access admin panel!', 'error')
        return redirect(url_for('admin_login'))

    try:
        adoption = AdoptionApplication.query.get_or_404(adoption_id)
        new_status = request.form.get('status')
        adoption.application_status = new_status
        db.session.commit()
        flash(f'Adoption application status updated to {new_status}!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating adoption application: {str(e)}', 'error')

    return redirect(url_for('admin_adoptions'))

@app.route('/admin/appointments/<int:appointment_id>')
def admin_appointment_details(appointment_id):
    if not session.get('admin_logged_in'):
        flash('Please log in to access admin panel!', 'error')
        return redirect(url_for('admin_login'))

    appointment = Appointment.query.get_or_404(appointment_id)

    # Skip marking as read for now (will implement later)

    return render_template('admin/appointment_details.html', appointment=appointment.to_dict())

def get_current_season():
    """Determine the current season in Bangalore based on the month"""
    current_month = datetime.now().month

    if 3 <= current_month <= 5:
        return "summer"
    elif 6 <= current_month <= 9:
        return "monsoon"
    elif 10 <= current_month <= 11:
        return "autumn"
    else:  # 12, 1, 2
        return "winter"

def get_next_season(current_season):
    """Get the next season after the current one"""
    seasons = ["winter", "summer", "monsoon", "autumn", "winter"]
    current_index = seasons.index(current_season)
    return seasons[current_index + 1]

def calculate_days_to_next_season():
    """Calculate days remaining until the next season starts"""
    current_date = datetime.now()
    current_month = current_date.month
    current_day = current_date.day
    current_year = current_date.year

    # Define season start dates
    if current_month in [12, 1, 2]:  # Winter
        if current_month == 12:
            next_season_date = datetime(current_year + 1, 3, 1)  # Summer starts March 1
        else:
            next_season_date = datetime(current_year, 3, 1)  # Summer starts March 1
    elif current_month in [3, 4, 5]:  # Summer
        next_season_date = datetime(current_year, 6, 1)  # Monsoon starts June 1
    elif current_month in [6, 7, 8, 9]:  # Monsoon
        next_season_date = datetime(current_year, 10, 1)  # Autumn starts October 1
    else:  # Autumn (10, 11)
        next_season_date = datetime(current_year, 12, 1)  # Winter starts December 1

    # Calculate days difference
    delta = next_season_date - current_date
    return delta.days

@app.route('/seasonal-tips')
def seasonal_tips():
    """Display seasonal pet care tips based on the current season in Bangalore"""
    current_season = get_current_season()
    next_season = get_next_season(current_season)
    days_to_next_season = calculate_days_to_next_season()

    # Load seasonal tips from JSON file
    try:
        with open('seasonal_tips.json', 'r') as f:
            all_tips = json.load(f)

        season_data = all_tips[current_season]
        next_season_data = all_tips[next_season]

        return render_template(
            'seasonal_tips.html',
            current_season=current_season,
            season_data=season_data,
            next_season=next_season,
            next_season_title=next_season_data['title'],
            days_to_next_season=days_to_next_season
        )
    except Exception as e:
        return render_template('error.html', error_message=f"Error loading seasonal tips: {str(e)}")

if __name__ == "__main__":
    # Initialize database
    init_database()
    app.run(debug=True)
