import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import json

# Load dataset from JSON file
with open('food_data.json', 'r') as f:
    food_data = json.load(f)

print(f"Loaded {len(food_data)} food items from JSON file")

# Create a synthetic dataset for training based on the JSON data
# We'll create sample pet profiles that would match with each food item
synthetic_data = []

# Map food items to their IDs for the model
food_id_mapping = {item['_id']: i for i, item in enumerate(food_data)}
reverse_food_id_mapping = {v: k for k, v in food_id_mapping.items()}

# Generate synthetic training data
for food_item in food_data:
    # Extract relevant features from the food item
    food_id = food_item['_id']
    life_stage = food_item['lifeStage']
    animal_size = food_item['animalSize']
    breed = food_item['breed']
    health_condition = food_item['condition']

    # Determine pet type based on food ID
    # IDs 001-100 are dog foods, IDs 101+ are cat foods
    pet_type = 'dog' if int(food_item['_id']) <= 100 else 'cat'

    # Generate age based on life stage and pet type
    if pet_type == 'dog':
        if life_stage == 'Puppy':
            age_range = (1, 12)  # 1-12 months for puppies
        elif life_stage == 'Adult':
            age_range = (12, 84)  # 1-7 years for adults
        elif life_stage == 'Senior':
            age_range = (84, 180)  # 7-15 years for seniors
        else:
            age_range = (1, 180)  # Any age for "All" life stages
    else:  # cat
        if life_stage == 'Kitten':
            age_range = (1, 12)  # 1-12 months for kittens
        elif life_stage == 'Adult':
            age_range = (12, 132)  # 1-11 years for adult cats
        elif life_stage == 'Senior':
            age_range = (132, 240)  # 11-20 years for senior cats
        else:
            age_range = (1, 240)  # Any age for "All" life stages

    # Generate weight based on animal size and pet type
    if pet_type == 'dog':
        if animal_size == 'X-Small':
            weight_range = (1, 5)
        elif animal_size == 'Small':
            weight_range = (5, 15)
        elif animal_size == 'Medium':
            weight_range = (15, 30)
        elif animal_size == 'Large':
            weight_range = (30, 60)
        elif animal_size == 'Giant':
            weight_range = (60, 100)
        else:
            weight_range = (1, 100)  # Any weight for "All" sizes
    else:  # cat
        # Cats have a much smaller weight range
        if animal_size == 'Small':
            weight_range = (2, 6)
        elif animal_size == 'Medium':
            weight_range = (6, 10)
        elif animal_size == 'Large':
            weight_range = (10, 15)
        else:
            weight_range = (2, 15)  # Any weight for "All" sizes

    # Generate multiple samples for each food item to create a robust dataset
    num_samples = 5  # Generate 5 samples per food item
    for _ in range(num_samples):
        age = np.random.randint(age_range[0], age_range[1])
        weight = np.random.randint(weight_range[0], weight_range[1])
        activity_level = np.random.choice(['low', 'medium', 'high'])

        # Create sample data
        sample = {
            'age': age,
            'weight': weight,
            'type': pet_type,
            'activity_level': activity_level,
            'food': food_id,
        }

        # Add health condition if present
        if health_condition:
            sample['health_condition'] = health_condition

        synthetic_data.append(sample)

# Convert to DataFrame
df = pd.DataFrame(synthetic_data)
print(f"Created synthetic dataset with {len(df)} samples")

# Encode categorical features
df['type'] = df['type'].map({'dog': 0, 'cat': 1})
df['activity_level'] = df['activity_level'].map({'low': 0, 'medium': 1, 'high': 2})

# Split features and target
X = df[['age', 'weight', 'type', 'activity_level']]
y = df['food'].map(food_id_mapping)  # Map food IDs to integers for the model

# Train model
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Save model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

# Save food mapping
with open('food_mapping.pkl', 'wb') as f:
    pickle.dump(reverse_food_id_mapping, f)

print("✅ Model and food mapping saved successfully.")
