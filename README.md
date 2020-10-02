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


### Preparing the development 

- Ensure `pip` and `pipenv` are installed. 
- Clone repository: `git clone git@github.com:....`
- `cd` into the repository.
- Fetch development dependencies `$ make install`
- Activate virtualenv: `pipenv shell` 
- Run `pip install -e . ` to install the package in your local env (make sure your virtualenv is active) 
- Then you can run:

`$ avatarMigrate [source_bucket] [target_bucket] [update_db]`

### How to Run Test 
Run tests locally using `make` if virtualenv is active: 

`$ make`

If virtualenv is not active run: 

`pipenv run make`


### How to Run

Pass in the source bucket, target bucket and DB details. All args are required. 

`$ avatarMigrate [source_bucket] [target_bucket] [update_db]`

### To Uninstall package 

- Run ```pip uninstall avatarMigrate``` 


### Things to watchout for!
- Roles and permissions ie access to S3 Read+Write, access to `production-db`
- AWS CLI configuration 
- User Access and roles
- Check is same region and account, if not add attach a bucket policy to the source bucket
- Check file pattern, move only file with "avatar-".
- waiter to check files exist before updating the database.

### Improvements, performance and scalability
- Implement Pagination incase there are lots of files to transfer S3 page max 1000 
- Add another flag to define transfer method ie to use awscli clidriver 

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


