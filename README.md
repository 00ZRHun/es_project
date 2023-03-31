# es_project

## Commands used in this project

### Django

- conda activate wordcloud
  - activate conda virtual env
- django-admin startproject es_project
  - create a new Django project
- cd es_project
  - enter into (chg dir) working directory
- pip install django-cors-headers
  - add cors to header (or else BE API can't be used in FE)
- python manage.py makemigrations (optional: app)
  - detect newly made change(s) to make migrations
- python manage.py migrate (optional: app)
  - add into tables of db
- python manage.py runserver 8080
  - run server

### PostgreSQL

- CREATE DATABASE esdb2;
  - create database
- \c esdb2
  - connect database
- \dt
  - list tables (List of relations)
- \d tweets_tweet
  - describe tables
- SELECT \* FROM django_migrations;
  - show all data in this table
