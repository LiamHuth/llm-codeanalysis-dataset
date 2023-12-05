import json
import tiktoken
from collections import defaultdict
import sys
import argparse
import openai
import os

"""
This script will validate the input dataset, estimate the training cost, and train the model if desired

Usage:
python3 train.py training_data.jsonl validation_data.jsonl

Additional arguments:
-e      sets the number of epochs
-c      sets the cost of training per 1k tokens

The data validation in this file is modified from the tutorial on openai's cookbook site:
https://cookbook.openai.com/examples/chat_finetuning_data_prep

Assumptions
Model: GPT 3.5 turbo
"""

# default values (gpt 3.5 turbo)
num_epochs = 3
base_cost = 0.008
training_path = ""
validation_path = ""

def parse_args():
    global base_cost, num_epochs, training_path, validation_path

    parser = argparse.ArgumentParser()

    # Required file path argument
    parser.add_argument('training_path', type=str, help='Path to the training file')
    parser.add_argument('validation_path', type=str, help='Path to the validation file')

    # Optional arguments
    parser.add_argument('-c', '--cost', type=float, default=None, help='Set the cost of training per 1k tokens')
    parser.add_argument('-e', '--epochs', type=int, default=None, help='Set the number of epochs')

    args = parser.parse_args()

    training_path = args.training_path
    validation_path = args.validation_path

    if args.cost is not None:
        if args.cost < 0:
            print("Error: cost must be positive", file=sys.stderr)
            sys.exit(1)
        base_cost = args.cost
    if args.epochs is not None:
        if args.epochs < 1:
            print("Error: number of epochs must be greater than 1", file=sys.stderr)
            sys.exit(1)
        num_epochs = args.epochs

    try:
        with open(args.training_path, 'r', encoding='utf-8') as f:
            training_data = [json.loads(line) for line in f]
        with open(args.validation_path, 'r', encoding='utf-8') as f:
            validation_data = [json.loads(line) for line in f]
    except:
        print("Error: could not load dataset", file=sys.stderr)
        sys.exit(1)


    return training_data, validation_data


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


def check_tokens(dataset):

    encoding = tiktoken.get_encoding("cl100k_base")
    token_count = 0

    for i, d in enumerate(dataset):
        msg_count = 0
        for message in d['messages']:
            msg_count += len(encoding.encode(message['content']))

        if (msg_count > 4096):
            print(f"WARNING: datapoint {i+1} has {msg_count} tokens and will be truncated to 4096 tokens")
            token_count += 4096
        else:
            token_count += msg_count
    
    return token_count


def upload_file(file_path):
    try:
        res = client.files.create(
                file=open(file_path, "rb"),
                purpose="fine-tune"
              )
        return res
    except Exception as e:
        print(f"Error uploading file: {e}", file=sys.stderr)
        sys.exit(1)


def main():

    # ----- validate data -----

    # get filename and parameters
    training_data, validation_data = parse_args()

    # validate dataset
    err = validate_data(training_data)
    if err:
        print("\nFound errors in data:")
        for k, v in err.items():
            print(f"{k}: {v}", file=sys.stderr)
        sys.exit(1)
    else:
        print("\nTraining dataset validated")

    err = validate_data(validation_data)
    if err:
        print("\nFound errors in data:")
        for k, v in err.items():
            print(f"{k}: {v}", file=sys.stderr)
        sys.exit(1)
    else:
        print("Validation dataset validated")


    if (len(training_data) < 10):
        print("WARNING: training dataset must contain at least 10 items, currently has:", len(training_data), file=sys.stderr)

    # calculate token count, print message if token count too high for any individual datapoint
    token_count = check_tokens(training_data) + check_tokens(validation_data)

    # print cost estimate
    print("\n--------------- Cost Estimate ---------------")
    print("tokens:                 ", token_count)
    print("epochs:                 ", num_epochs)
    print(f"cost:                    ${base_cost: .3f} / 1k tokens")
    print(f"estimated training cost: ${(token_count/1000) * base_cost * num_epochs: .3f} USD\n")

    # ask to train to model
    res = input("Proceed to training? (y/n): ")
    if (res.lower()[0] != "y"):
        print("exiting without training...\n")
        sys.exit(0)

    # ----- train model -----

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

    # upload training and validation files
    training_file = upload_file(training_path)
    validation_file = upload_file(validation_path)

    # create job to tune model
    tuning_job = client.fine_tuning.jobs.create(
                  training_file=training_file.id, 
                  validation_file=validation_file.id,
                  model="gpt-3.5-turbo"
                )

if __name__ == "__main__":
    main()