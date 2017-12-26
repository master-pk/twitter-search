Twitter search
==============


Setup Steps
===========


1. Environment Setup:

    * Create a virtual environment
      - Recommended python version: 2.7.12

    * Install the requirements by using command:
        * pip install -r `requirements.text`

2. Database Setup (Development environment):

    * Setup a database server (preferably MySQL 5.6.25 or higher)
      - Ubuntu: `sudo apt-get install mysql-server`
      - OSX: `brew install mysql && brew services start mysql`

    * Create a database with name 'twitter'(if using MySQL) using the command
        - `CREATE DATABASE twitter CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;`
        - Mentioning the `COLLATE utf8mb4_general_ci` part is very important, otherwise MySQL will raise error on saving twitter data.

    * Django DB setup and migrations:
        * Run `python manage.py migrate`

    * Creating admin accounts via shell:
    Run `python manage,py createsuperuser`

3. Run the server using `python manage.py runserver`

API Documentation
=================

API Endpoint - `/search/`
API method - POST (twitter recommends to have it POST for long data)

Required params:
By providing keywords, the api will fetch data from twitter based on that
 "keywords": ["key1", "key2"]
 
 Optional filter params:
 "text": "filter text" - text on which filtering need to be done
 "text_type_choice" - <choice - 1,2,3,4> - 1 is for exact match, 2 is for starts with, 3 is for ends with and 4 for contains
 "start_date": "YYYY-MM-DD" - date from which tweets will be returned
 "end_date": "YYYY-MM-DD" - date upto which tweets will be returned
 "lower_retweet_count": <integer> - Filter on basis of re-twet counts
 "upper_retweet_count": <integer> - Filter on basis of re-twet counts
 

