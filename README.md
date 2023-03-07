

### Step 1 - Install the requirements

```bash
pip install -r requirements.txt
```

### Step 2 - Run main.py file

```bash
python main.py
```

# To download your dataset
https://archive.ics.uci.edu/ml/datasets/thyroid+disease


# Git commands

if you are starting a project and you want to use git in your project

git init

Note: This is going to initalize git in your source code.

OR
you can clone exiting github repo

Note: Clone/ Downlaod github repo in your system

Add your changes made in file to git stagging are

git add file_name
Note: You can given file_name to add specific file or use "." to add everything to staging are

Create commits

git commit -m "message"
git push origin main
Note: origin--> contains url to your github repo main--> is your branch name

To push your changes forcefully.

git push origin main -f
To pull changes from github repo

git pull origin main

Note: origin--> contains url to your github repo main--> is your branch name

.env file has

MONGO_DB_URL="mongodb://localhost:27017/neurolabDB"

AWS_ACCESS_KEY_ID="sfsdfsdfsdf"

AWS_SECRET_ACCESS_KEY="fergdfgrgerg"

## DOCKER COMMAND
curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh

sudo usermod -aG docker ubuntu

newgrp docker
