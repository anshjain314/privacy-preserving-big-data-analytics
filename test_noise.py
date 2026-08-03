from feature_engineering.regex_features import extract_regex_features

samples = [

    "rahul@gmail.com",

    "9876543210",

    "ABCDE1234F",

    "123456789012",

    "A1234567",

    "Rahul Sharma",

    "Bangalore"

]

for sample in samples:

    print("=" * 60)

    print(sample)

    print(extract_regex_features(sample))