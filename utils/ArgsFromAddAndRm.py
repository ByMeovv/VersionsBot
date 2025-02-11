import argparse

def get_args_from_add_and_rm(msg):
    parser = argparse.ArgumentParser()
    parser.add_argument('version', type=int, help='Version must be an integer')
    parser.add_argument('name_client', type=str, help='Client name must be a string')

    return parser