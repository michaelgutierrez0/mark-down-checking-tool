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
elif len(scan_result.scan_failures) > 0:
    print("Scan completed with errors. Please see the following list of errors:")
    for error in scan_result.scan_failures:
        # Need to parse an error such as:
        # PyMarkdownScanFailure(
        # scan_file='MarkDownInput/SixthStreetPlatform-v0.0.1a.md',
        # line_number=1,
        # column_number=1,
        # rule_id='MD041',
        # rule_name='first-line-heading,first-line-h1',
        # rule_description='First line in file should be a top level heading',
        # extra_error_information=''
        # parsed_error = error.PyMarkdownScanFailure
        # print(parsed_error)
        # print(type(parsed_error))
        print(f"Rule ID: {error.rule_id}")
        print(f"Rule Name: {error.rule_name}")
        print(f"Rule Description: {error.rule_description}")
        print(f"At line {error.line_number}")
        print(f"At column {error.column_number}")
        print(f"In file {error.scan_file}")
        if error.extra_error_information != "":
            print(f"Extra error information: {error.extra_error_information}")
        print()
elif len(scan_result.pragma_errors) > 0:
    print("Scan completed with pragma errors. Please see the following list of errors:")
    for error in scan_result.scan_failures:
        print(f"Error: {error}")
