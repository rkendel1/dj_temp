import argparse
from importlib import import_module

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("template", help="template type")

    args = parser.parse_args()
    import_module(args.template)