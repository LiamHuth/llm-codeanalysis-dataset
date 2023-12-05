import json
from collections import defaultdict
import sys
import argparse
import openai
import os
import csv

model_id = ""
testing_data = []
testing_path = ""


def parse_args():
    global model_id, testing_data, testing_path

    parser = argparse.ArgumentParser()

    # Required file path argument
    parser.add_argument('testing_path', type=str, help='Path to the testing file')
    parser.add_argument('model_id', type=str, help='OpenAI model id')

    args = parser.parse_args()

    testing_path = args.testing_path
    model_id = args.model_id

    try:
        with open(testing_path, 'r', encoding='utf-8') as f:
            testing_data = [json.loads(line) for line in f]

    except:
        print("Error: could not load dataset", file=sys.stderr)
        sys.exit(1)


    return model_id, testing_data


# checks formatting of the dataset
def validate_data(dataset):
    format_errors = defaultdict(int)

    for ex in dataset:
        if not isinstance(ex, dict):
            format_errors["data_type"] += 1
            continue
            
        messages = ex.get("messages", None)
        if not messages:
            format_errors["missing_messages_list"] += 1
            continue
            
        for message in messages:
            if "role" not in message or "content" not in message:
                format_errors["message_missing_key"] += 1
            
            if any(k not in ("role", "content", "name", "function_call") for k in message):
                format_errors["message_unrecognized_key"] += 1
            
            if message.get("role", None) not in ("system", "user", "assistant", "function"):
                format_errors["unrecognized_role"] += 1
                
            content = message.get("content", None)
            function_call = message.get("function_call", None)
            
            if (not content and not function_call) or not isinstance(content, str):
                format_errors["missing_content"] += 1
        
        if not any(message.get("role", None) == "assistant" for message in messages):
            format_errors["example_missing_assistant_message"] += 1
    
    return format_errors


def main():

    # ----- validate data -----

    # get filename and parameters
    model_id, testing_data = parse_args()

    # validate dataset
    err = validate_data(testing_data)
    if err:
        print("\nFound errors in data:")
        for k, v in err.items():
            print(f"{k}: {v}", file=sys.stderr)
        sys.exit(1)
    else:
        print("\nTesting dataset validated")

    # ----- test model -----

    # get user specific parameters from environment
    key = os.environ.get('OPENAI_API_KEY', None)
    org_id = os.environ.get('OPENAI_ORGANIZATION_KEY', None)

    if (key is None):
        print("API Key not defined in your environment", file=sys.stderr)
        sys.exit(1)

    params = {'api_key': key}

    if (org_id is not None):
        params['organization'] = org_id
    else:
        print("Note: no organization id associated with this model")

    # open connection
    global client
    client = openai.OpenAI(**params)

    # send test data to api
    with open(model_id + "_out.csv", 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(["Test Case", "Expected", "Result"])
        
        i = 1
        # for each test case
        for case in testing_data:
            print(f"Testing case {i}")

            # make api call
            response = client.chat.completions.create(
                model=model_id,
                messages=case["messages"][:2]
            )

            # write results to file
            writer.writerow(
                [
                "case " + str(i),                                # test case number
                case["messages"][2]["content"],             # expected result
                response.choices[0].message.content         # returned result
                ]
            )

            i += 1

if __name__ == "__main__":
    main()