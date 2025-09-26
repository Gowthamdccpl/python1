import json
import pandas as pd
from tabulate import tabulate
import os

def load_json_dataset(file_path='food_data.json'):
    """
    Load the pet food dataset from a JSON file and return it as a list of dictionaries
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        print(f"✅ Successfully loaded {len(data)} records from {file_path}")
        return data
    except FileNotFoundError:
        print(f"❌ Error: File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"❌ Error: File '{file_path}' is not a valid JSON file.")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def convert_to_dataframe(data):
    """
    Convert the JSON data to a pandas DataFrame for easier manipulation
    """
    if data is None:
        return None
    
    df = pd.DataFrame(data)
    return df

def display_dataset_summary(df):
    """
    Display a summary of the dataset
    """
    if df is None:
        return
    
    print("\n=== Dataset Summary ===")
    print(f"Total records: {len(df)}")
    
    # Count by brand
    print("\nBrands:")
    brand_counts = df['brand'].value_counts()
    for brand, count in brand_counts.items():
        print(f"  - {brand}: {count} products")
    
    # Count by life stage
    print("\nLife Stages:")
    life_stage_counts = df['lifeStage'].value_counts()
    for stage, count in life_stage_counts.items():
        print(f"  - {stage}: {count} products")
    
    # Count by animal size
    print("\nAnimal Sizes:")
    size_counts = df['animalSize'].value_counts()
    for size, count in size_counts.items():
        print(f"  - {size}: {count} products")
    
    # Count by condition (if not null)
    print("\nSpecial Conditions:")
    condition_counts = df['condition'].dropna().value_counts()
    for condition, count in condition_counts.items():
        print(f"  - {condition}: {count} products")

def display_sample_records(df, num_records=5):
    """
    Display a sample of records from the dataset
    """
    if df is None:
        return
    
    print(f"\n=== Sample of {num_records} Records ===")
    sample = df.sample(min(num_records, len(df)))
    
    # Select only the most relevant columns for display
    display_cols = ['_id', 'name', 'brand', 'lifeStage', 'animalSize', 'calories', 'price']
    sample_display = sample[display_cols]
    
    # Format the table for better display
    print(tabulate(sample_display, headers='keys', tablefmt='pretty', showindex=False))

def search_dataset(df, query=None, brand=None, life_stage=None, animal_size=None, condition=None):
    """
    Search the dataset based on various criteria
    """
    if df is None:
        return None
    
    result = df.copy()
    
    if query:
        # Search in name field
        result = result[result['name'].str.contains(query, case=False)]
    
    if brand:
        result = result[result['brand'] == brand]
    
    if life_stage:
        result = result[result['lifeStage'] == life_stage]
    
    if animal_size:
        result = result[result['animalSize'] == animal_size]
    
    if condition:
        # Handle null values in condition
        if condition == 'None':
            result = result[result['condition'].isna()]
        else:
            result = result[result['condition'] == condition]
    
    return result

def main():
    # Clear the console (works on both Windows and Unix-like systems)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("=== Pet Food Dataset Viewer ===\n")
    
    # Load the dataset
    data = load_json_dataset()
    if data is None:
        return
    
    # Convert to DataFrame
    df = convert_to_dataframe(data)
    
    # Display summary
    display_dataset_summary(df)
    
    # Display sample records
    display_sample_records(df)
    
    # Interactive search
    while True:
        print("\n=== Search Options ===")
        print("1. Search by keyword")
        print("2. Filter by brand")
        print("3. Filter by life stage")
        print("4. Filter by animal size")
        print("5. Filter by condition")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':
            query = input("Enter search keyword: ")
            results = search_dataset(df, query=query)
            if len(results) > 0:
                print(f"\nFound {len(results)} matching records:")
                display_sample_records(results, 10)
            else:
                print("No matching records found.")
        
        elif choice == '2':
            brands = sorted(df['brand'].unique())
            print("\nAvailable brands:")
            for i, brand in enumerate(brands, 1):
                print(f"{i}. {brand}")
            
            brand_idx = int(input("\nSelect brand number: ")) - 1
            if 0 <= brand_idx < len(brands):
                results = search_dataset(df, brand=brands[brand_idx])
                print(f"\nFound {len(results)} matching records:")
                display_sample_records(results, 10)
            else:
                print("Invalid selection.")
        
        elif choice == '3':
            life_stages = sorted(df['lifeStage'].unique())
            print("\nAvailable life stages:")
            for i, stage in enumerate(life_stages, 1):
                print(f"{i}. {stage}")
            
            stage_idx = int(input("\nSelect life stage number: ")) - 1
            if 0 <= stage_idx < len(life_stages):
                results = search_dataset(df, life_stage=life_stages[stage_idx])
                print(f"\nFound {len(results)} matching records:")
                display_sample_records(results, 10)
            else:
                print("Invalid selection.")
        
        elif choice == '4':
            sizes = sorted(df['animalSize'].unique())
            print("\nAvailable animal sizes:")
            for i, size in enumerate(sizes, 1):
                print(f"{i}. {size}")
            
            size_idx = int(input("\nSelect animal size number: ")) - 1
            if 0 <= size_idx < len(sizes):
                results = search_dataset(df, animal_size=sizes[size_idx])
                print(f"\nFound {len(results)} matching records:")
                display_sample_records(results, 10)
            else:
                print("Invalid selection.")
        
        elif choice == '5':
            conditions = ['None'] + sorted(df['condition'].dropna().unique())
            print("\nAvailable conditions:")
            for i, condition in enumerate(conditions, 1):
                print(f"{i}. {condition}")
            
            condition_idx = int(input("\nSelect condition number: ")) - 1
            if 0 <= condition_idx < len(conditions):
                results = search_dataset(df, condition=conditions[condition_idx])
                print(f"\nFound {len(results)} matching records:")
                display_sample_records(results, 10)
            else:
                print("Invalid selection.")
        
        elif choice == '6':
            print("\nExiting program. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
