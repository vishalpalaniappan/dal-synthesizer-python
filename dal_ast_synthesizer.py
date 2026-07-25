import sys
import json
import argparse
from Synthesizer import Synthesizer

def main(argv):

    args_parser = argparse.ArgumentParser(
        description="Synthesizes a python program given the AST"
    )

    args_parser.add_argument(
        "--ast",
        required=True,
        help="Path to ast file"
    )
    
    parsed_args = args_parser.parse_args(argv[1:])

    try:
        with open(parsed_args.ast, 'r') as f:
            tree = json.loads(f.read())
    except Exception as e:
        print(f"Invalid arguments: {str(e)}", file=sys.stderr)
        return -1

    synth = Synthesizer(tree)
    synth.run()

if __name__ == "__main__":
    sys.exit(main(sys.argv))