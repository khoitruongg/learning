from utils.read_csv import read_csv
from utils.write_csv import write_csv
from utils.filter import filter_by_min_age

def main():
    input_file = 'data.csv'
    output_file = 'people_below_30.csv'
    min_age = 20

    data = read_csv(input_file)
    print(data)
    filtered = filter_by_min_age(data, min_age)

    if filtered:
        headers = filtered[0].keys()
        write_csv(output_file, filtered, headers)
        print(f"{len(filtered)} rows written to {output_file}")
    else:
        print("No data matched the filter.")

if __name__ == "__main__":
    main()
