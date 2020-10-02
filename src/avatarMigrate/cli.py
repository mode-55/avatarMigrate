from argparse import ArgumentParser 

def create_parser():
    parser = ArgumentParser()
    parser.add_argument('source_bucket', help="S3 source_bucket name")
    parser.add_argument('target_bucket', help="S3 target_bucket name")
    return parser


def main():
    import boto3
    import botocore
    from avatarMigrate import s3

    args = create_parser().parse_args()
    s3.migrate_objects(args.source_bucket,args.target_bucket)
    

if __name__ == "__main__":
    main()