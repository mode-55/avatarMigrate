from argparse import ArgumentParser 

def create_parser():
    parser = ArgumentParser()
    parser.add_argument('source_bucket', help="S3 source_bucket name")
    parser.add_argument('target_bucket', help="S3 target_bucket name")
    return parser


def main():
    create_parser()

if __name__ == "__main__":
    main()