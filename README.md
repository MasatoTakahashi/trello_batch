# What's this?
A script for batch processing for everyday's Trello operation.

# Requirements
Python 3.x

# How to use
1. make ** credential ** file in the same directory as these scripts
1. get and write your credential key and access token etc. as followings
```
credential_key:xxxxxxxxxxxxx
token:xxxxxxxxxxxxx
board_name:project name
username:yourname
```
1. just kick **.sh** file to execute each process.
or directly type like
```sh
python trello_batch.py --mode archive
```
or
```sh
python trello_batch.py --mode create
```


# update
## 2015/11/05
add batch create from icalendar url
