import csv

def read_csv(filename):
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            data = list(reader) 
            
            for row in data:
                print(f"{row['name']} is {row['age']} years old and lives in {row['city']}.")

            return data
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


