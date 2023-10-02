from pymarkdown.api import PyMarkdownApi, PyMarkdownApiException
import os
import sys

source_path = "MarkDownInput"

# Get a list of all files in the directory (excluding directories)
files = [f for f in os.listdir(source_path) if os.path.isfile(
    os.path.join(source_path, f))]

# Quit the program if no files are found
if len(files) == 0:
    print("No files found in directory. Please add file(s) to the MarkDownInput directory.")
    exit()

# Scan the files
try:
    scan_result = PyMarkdownApi().scan_path(source_path)
except PyMarkdownApiException as this_exception:
    print(f"API Exception: {this_exception}", file=sys.stderr)
    sys.exit(1)

if (len(scan_result.scan_failures) == 0 and len(scan_result.pragma_errors) == 0):
    print("Scan completed successfully! No errors found.")

else:
    # Create an empty dictionary to hold the error information for each file
    # The key will be the file name and the value will be a list of errors
    files_with_errors = {}

    print("Scan completed with errors.")
    for error in scan_result.scan_failures:

        # If the file name is not already in the dictionary, add it
        if error.scan_file not in files_with_errors:
            files_with_errors[error.scan_file] = []

        # Add the error information to the list of errors for the file
        files_with_errors[error.scan_file].append(
            {
                "rule_id": error.rule_id,
                "rule_name": error.rule_name,
                "rule_description": error.rule_description,
                "line_number": error.line_number,
                "column_number": error.column_number,
                "extra_error_information": error.extra_error_information
            }
        )
    print(f"Found {len(files_with_errors)} file(s) with errors.")

    for file_name, errors in files_with_errors.items():
        print(f"File Name: {file_name}")
        print(f"Number of errors: {len(errors)}")
        
        # Create a dictionary to hold the unique errors
        unique_errors = {}

        # Loop through the errors and add them to the dictionary
        for error in errors:
            if error['rule_id'] not in unique_errors:
                error_information = {
                    "rule_id": error['rule_id'],
                    "rule_name": error['rule_name'],
                    "rule_description": error['rule_description'],
                    "found_count": 1
                }
                unique_errors[error['rule_id']] = error_information
            else:
                unique_errors[error['rule_id']]['found_count'] += 1
        # Print the unique errors
        print("Unique Errors: ")
        for error in unique_errors.values():
            print(f"Rule Description: {error['rule_description']}")
            print(f"Found {error['found_count']} times")

        print()

        for error in errors:
            print(f"Rule ID: {error['rule_id']}")
            print(f"Rule Name: {error['rule_name']}")
            print(f"Rule Description: {error['rule_description']}")
            print(f"At line: {error['line_number']}")
            print(f"At column: {error['column_number']}")
            if error['extra_error_information'] != "":
                print(
                    f"Extra error information: {error['extra_error_information']}")
            print()
