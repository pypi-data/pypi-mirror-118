"""CLI Executable"""

import argparse

from .pybankers import main


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bankers Analysis Tool")
    parser.prog = "python -m pybankers"
    parser.add_argument("max_count", type=int, help="max steps count")
    args = parser.parse_args()
    main(args.max_count)
