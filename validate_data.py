import json
import tiktoken
from collections import defaultdict
import sys
import argparse

"""
This script will validate the input dataset and estimate the training cost

Usage:
python3 validate_data.py relative_path_to_dataset.jsonl

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
data_path = ""


def parse_args():
    global base_cost, num_epochs

    parser = argparse.ArgumentParser()

    # Required file path argument
    parser.add_argument('file_path', type=str, help='Path to the file')

    # Optional arguments
    parser.add_argument('-c', '--cost', type=float, default=None, help='Set the cost of training per 1k tokens')
    parser.add_argument('-e', '--epochs', type=int, default=None, help='Set the number of epochs')

    args = parser.parse_args()

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
        with open(args.file_path, 'r', encoding='utf-8') as f:
            dataset = [json.loads(line) for line in f]
    except:
        print("Error: could not load dataset", file=sys.stderr)
        sys.exit(1)


    return dataset

    



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


def main():

    # get filename and parameters
    dataset = parse_args()

    # validate dataset
    err = validate_data(dataset)
    
    if err:
        print("Found errors in data:")
        for k, v in err.items():
            print(f"{k}: {v}", file=sys.stderr)
        sys.exit(1)
    else:
        print("Dataset Validated")

    # calculate token count, print message if token count too high for any individual datapoint
    token_count = check_tokens(dataset)

    # print cost estimate
    print("\n--- Cost Estimate ---")
    print("# tokens: ", token_count)
    print("# epochs: ", num_epochs)
    print(f"cost:      ${base_cost: .3f} / 1k tokens")
    print(f"Estimated Training Cost: ${(token_count/1000) * base_cost * num_epochs: .3f} USD\n")


if __name__ == "__main__":
    main()