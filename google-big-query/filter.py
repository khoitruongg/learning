def filter_by_min_age(data, min_age):
    return [row for row in data if int(row['age']) >= min_age]
