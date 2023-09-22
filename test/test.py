import json

# Read input data from a JSON file
with open('/home/yash/Desktop/sony_iam.json', 'r') as input_file:
    items = json.load(input_file)

# Serialize each item as JSON and join with newline characters
with open('/home/yash/Desktop/sony_iam_output.json', 'w') as output_file:
    for i in items:
        # Serialize the current item as JSON and write it as a separate line
        json_string = json.dumps(i)
        output_file.write(json_string+"\n")
    