import os
import json
import numpy as np
import math

def init_config():
    global config_data, formatted_training_file_path, formatted_validation_file_path, formatted_testing_file_path, prompt_format_path, source_directory, temp_source_directory_input, temp_source_directory_output, vulnerabilities, validation_ratio, test_ratio

    with open("./data/config.json", 'r') as config:
        config_data = json.load(config)
        formatted_training_file_path = config_data["formatted_training_file_path"]
        formatted_validation_file_path = config_data["formatted_validation_file_path"]
        formatted_testing_file_path = config_data["formatted_testing_file_path"]
        prompt_format_path = config_data["prompt_format_path"]
        source_directory = config_data["source_directory"]
        temp_source_directory_input = config_data["source_directory_input"]
        temp_source_directory_output = config_data["source_directory_output"]
        vulnerabilities = config_data["vulnerabilities"]
        validation_ratio = config_data["validation_ratio"]
        test_ratio = config_data["test_ratio"]

def init_source_files(vulnerabilityDir: str):
    # Lists to hold the matched file names
    global formatted_source_directory_input, formatted_source_directory_output
    formatted_source_directory_input = temp_source_directory_input % vulnerabilityDir
    # print(formatted_source_directory_input)
    formatted_source_directory_output = temp_source_directory_output % vulnerabilityDir
    
    python_files = []
    output_files = []
    
    # Populate the lists with the respective file types
    for file in os.listdir(formatted_source_directory_input):
        python_files.append(file)

    for file in os.listdir(formatted_source_directory_output):
        output_files.append(file)

    # Sort the lists to ensure they are in the same order for pairing
    python_files.sort()
    output_files.sort()

    assert len(python_files) == len(output_files)

    return python_files, output_files

def add_line_num(source_code):
    lines = source_code.splitlines()

    # Prepend line numbers to each line
    numbered_lines = [f"{i + 1}: {line}" for i, line in enumerate(lines)]

    # Join the numbered lines back into a single string
    numbered_code = "\n".join(numbered_lines)

    return numbered_code

def init_formatted_file():
    with open(formatted_training_file_path, 'w') as file:
        pass
    with open(formatted_validation_file_path, 'w') as file:
        pass
    with open(formatted_testing_file_path, 'w') as file:
        pass

def add_content(role, content, data):
    for i in range(len(data["messages"])):
        if data["messages"][i]["role"] == role:
            data["messages"][i]["content"] = content
    return data 

def add_to_formatted_file(data, path):
    with open(path, 'a') as formatted_file:
        formatted_file.write(json.dumps(data))
        formatted_file.write('\n')

def format():
    init_formatted_file()

    for vulnerabilityDir in os.listdir(source_directory):
        full_path = os.path.join(source_directory, vulnerabilityDir)
        if not os.path.isdir(full_path):
            continue

        python_files, output_files = init_source_files(vulnerabilityDir)

        file_num = len(python_files)

        # Initialize boolean arrays
        is_validation_list = np.full(file_num, False, dtype=bool)
        is_test_list = np.full(file_num, False, dtype=bool)

        # Randomly select indices for validation set
        elements_to_change_for_val = math.ceil(file_num * validation_ratio)
        indices_to_change = np.random.choice(file_num, elements_to_change_for_val, replace=False)
        is_validation_list[indices_to_change] = True

        # Randomly select indices for test set from the remaining data
        remaining_indices = np.where(is_validation_list == False)[0]
        elements_to_change_for_test = math.floor(file_num * test_ratio)

        test_indices_to_change = np.random.choice(remaining_indices, elements_to_change_for_test, replace=False)
        is_test_list[test_indices_to_change] = True

        # Convert to list if needed
        is_validation_list = is_validation_list.tolist()
        is_test_list = is_test_list.tolist()

        i = 0

        for py_file, out_file in zip(python_files, output_files):
            with open(prompt_format_path, 'r') as prompt_format:
                prompt_format_data = json.load(prompt_format)

            # Check if the base name (without extension) is the same for the pair
            if os.path.splitext(py_file)[0] == os.path.splitext(out_file)[0]:
                # Full paths to the files
                py_file_path = os.path.join(formatted_source_directory_input, py_file)
                out_file_path = os.path.join(formatted_source_directory_output, out_file)
                
                # Read the content of the .py file
                with open(py_file_path, 'r') as file:
                    py_content = file.read()
                    source_code = add_line_num(py_content)
                    prompt_format_data = add_content("user", source_code, prompt_format_data)
                
                # Read the content of the .out file
                with open(out_file_path, 'r') as file:
                    out_content = file.read()
                    prompt_format_data = add_content("assistant", out_content, prompt_format_data)
            else:
                print(f"No matching pair found for {py_file}")

            if is_validation_list[i]:
                path = formatted_validation_file_path
            elif is_test_list[i]:
                path = formatted_testing_file_path
            else:
                path = formatted_training_file_path

            add_to_formatted_file(prompt_format_data, path)
            i += 1

def main():
    init_config()
    format()

if __name__ == "__main__":
    main()