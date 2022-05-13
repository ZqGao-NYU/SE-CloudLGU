# CloudLGU

> CloudLGU is a CUHKSZ CSC4001 Software Engineering course project, created by Ziqi, Mingjie, Hanyang, Yizhan. 

## Build Setup
```bash
# clone the project
git clone git@github.com:118010077/SE-CloudLGU.git

# enter the project directory
cd SE-CloudLGU/src/Back-End

pip install -r requirements.txt

```

## Initialize Database
1. Open your mysql work bench and run init_db.sql in (SE-CloudLGU\src\Back-End)
2. Find the settings.py in (SE-CloudLGU\src\Back-End\Back_End), change the mysql username and password into your username and password
3. run this:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Run server

```bash
python manage.py runserver
```