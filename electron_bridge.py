import sys
import json
from main import main

def run():
    # Parse command line arguments
    directory = sys.argv[1]
    openai_key = sys.argv[2]

    # Call main function and capture output
    result = main(directory, openai_key)

    # Print result as JSON
    print(json.dumps(result))

if __name__ == "__main__":
    run()