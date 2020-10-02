### Requirments
To Write a Python program that moves all images from the legacy-s3 to the production-s3 and updates their paths in the MariaDB database. To clarify, the program will make sure that all objects in the legacy bucket/path are correctly moved to the new one. This means, that at the end of the execution, the database will also contain only paths with the modern prefix.

### Resources to use 

The program will interact with:

`production-db` MariaDB database RDS instance
`production-s3` AWS S3 bucket
`legacy-s3` AWS S3 bucket

### Goal 
Move all images from legacy-s3 to production-s3 and update database paths.  
Ability to run the below command in terminal to perform the migration: 

`$ avatarMigrate [source_bucket] [target_bucket] [update_db]`

### Dependencies 
- Python 3.8+
- AWS CLI installed and configured profile that has access to perform admin actions on S3, RDS.  
- All resources must be valid `legacy-s3` `production-s3` `production-db`
- Pipenv installed and configured
- .env file containing details - env.sample is provided in the repo. 
- boto3, botocore, mysql-connector-python, python-dotenv  

### How to Run Test 
Run tests locally using `make` if virtualenv is active: 

`$ make`

If virtualenv is not active run: 

`pipenv run make`


### How to install

- Please ensure that dependecies are installed and your .env file is created :

```sh
$ cd [your prefered location]
$ touch .env
$ pip3.8 install python-dotenv boto3 botocore mysql-connector-python
$ pip3.8 install --user https://avatarmigrate.s3.eu-west-2.amazonaws.com/avatarMigrate-0.1.0-py38-none-any.whl 
```
- You might get a warning about PATH which you can create if needed by running:  

```
$ export PATH="/Users/os/Library/Python/3.8/bin:$PATH" 

```
- Now you can run `$avatarMigrate` and you should get help. 
- Pass in the source bucket, target bucket and DB details. All args are required. 

`$ avatarMigrate [source_bucket] [target_bucket] [update_db]`

- Example: 

`$ avatarMigrate 'legacy-tj-s3' 'production-tj-s3' Yes`

`$ avatarMigrate 'legacy-tj-s3' 'production-tj-s3' No`


### To Uninstall package 

- Run `$ pip3.8 uninstall avatarMigrate` 


### Things to watchout for!
- Roles and permissions ie access to S3 Read+Write, access to both S3 buckets.
- AWS CLI configuration.
- User Access and roles.
- Check is same region and account, if not add attach a bucket policy to the source bucket.
- Check file pattern, move only file with "avatar-".
- waiter to check files exist before updating the database.

### Improvements, performance and scalability
- Implement Pagination incase there are lots of files to transfer S3 page max 1000. done!
- Add another flag to define transfer method ie to use awscli clidriver. TODO 

`$ avatarMigrate [source_bucket] [target_bucket] [update_db] --method sync`

- Using clidriver you can sync which would run a lot faster than loop through objects. Below is sample of the approach:  

```python 

import os
if os.environ.get('LC_CTYPE', '') == 'UTF-8':
    os.environ['LC_CTYPE'] = 'en_US.UTF-8'

from awscli.clidriver import create_clidriver
driver = create_clidriver()
driver.main('s3 sync s3://legacy-tj-s3/image/ s3://production-tj-s3/avatar/'.split())

```
- Alternatively configure LB to requirect requests with `https://legacy-url/image/avatar-32425.png` to `https://modern-url/avatar/avatar-32425.png` to avoid having issues with users Avatars until the transfer of files is successful and verified. 


