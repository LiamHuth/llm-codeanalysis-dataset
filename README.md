# Dataset for LLM Static Analysis Tuning - Open Source Dataset Development

## Introduction

This repository includes our research on refining Large Language Models (LLMs) for static analysis in software security, focusing on specific vulnerabilities like SQL injection, command injection, and path traversal. Our work includes developing a dataset to enhance ChatGPT 3.5 Turbo's detection capabilities. We compare different LLMs, highlighting the effect of specialized training on performance. 

In the following sections, we will be detailing how to reproduce our results, facilitating further research and community collaboration.

## Environment Setup

### Requirements
`pip install -r requirements.txt`

### Environment Variables
To use the scripts you will need to put your api key in the following environment variable:

`export OPENAI_API_KEY='your-api-key-here'`

If you wish to link the tuned model to an organization, also define this environment variable:

`export OPENAI_ORGANIZATION_KEY='your-organization-key-here'`

### Configurations (optional)
In the directory `./data/`, there are two configuration files might be of your interests. 

#### config.json
You can configure the file directory paths, edit vulnerability types, and adjusting the ratio of validation and testing dataset.

#### prompts.json
You can configure the prompts used to tune ChatGPT. Make sure this has to be one line ONLY and DO NOT change the role's value.

## Result Replication

### Data Formatting
First, run `python3 data_formatter.py`, this will convert all raw dataset, pairs of source code `.py` and expected output `.out`, into a formatted `.JSONL` required by OpenAI's API.

### Training
Run `python3 train.py <path-to-training.jsonl> <path-to-validation.jsonl>`. This will validate the input data and give an estimate of the training costs. Once the costs are accepted it will send the job to OpenAI. 

### Testing
Run `python3 test.py <path-to-testdata.jsonl> <model-id>`. This will automatically run the test suite throught the API and output to a csv in `/results`.

## Contribution
We would thank anyone who would like to contribute to the dataset.

### Input
Go to `./data/source/${vulneralbility type}/input/`, add source code, and make sure the name format follows the below:

`${type}_${size_of_current_dataset + 1}.${file extension}`.

### Output
Go to `./data/source/${vulneralbility type}/output/`, add `.out` file, where 
* First line is an `int` indicating the type of vulnerability 
* Second line is an `Array<int>` indicating the lines of taint source
* Third line is an `Array<int>` indicating the lines of taint sink

and make sure the name format follows the below:

`${type}_${size_of_current_dataset + 1}.out`.

### Contribution List
Don't forget to add your name, any reference, and date to `./data/README.md` and follow the format.