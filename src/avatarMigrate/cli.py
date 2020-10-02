from argparse import ArgumentParser 

def create_parser():
    parser = ArgumentParser()
    parser.add_argument('source_bucket', help="S3 source_bucket name")
    parser.add_argument('target_bucket', help="S3 target_bucket name")
    # parser.add_argument('database_url', help="RDS database url")
    # parser.add_argument('database_username', help="RDS database username")
    # parser.add_argument('database_password', help="RDS database password")
    # parser.add_argument('database_name', help="RDS database name")
    return parser


def main():
    import boto3
    import botocore
    from avatarMigrate import s3, rds

    args = create_parser().parse_args()
    if(args.source_bucket and args.target_bucket):
        copy_objects = s3.migrate_objects(args.source_bucket,args.target_bucket)
        #if(copy_objects and args.database_url and args.database_username and args.database_password and args.database_name):
        rds.update_database() 

if __name__ == "__main__":
    main()