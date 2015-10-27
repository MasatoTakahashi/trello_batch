# coding: utf-8

import os, sys, time
import csv
# import urllib2
from urllib.request import * 
import urllib.parse
import json
from datetime import date
import argparse

class Trello_agent:
    def __init__(self):
        self.credential_key = ''
        self.token = ''
        self.board_name = ''
        self.board_id = ''
        self.username = ''
        self.list_id = ''
        self.done_cards = []
    
    def __str__(self):
        return 'ckey:' + self.credential_key + \
                '\ntoken:' + self.token + '\nboard_name:' + self.board_name + \
                '\nboard_id:' + self.board_id + '\nlist_id:' + self.list_id
        
    def read_credential_file(self, filepath):
        # try to read credential file        
        try:
            fn = open(filepath, 'r')
        except IOError:
            print('Error: credential file does not exist')
            sys.exit()
        
        for buf in fn.readlines():
            k, v = buf.split(':')
            if k == 'credential_key':
                self.credential_key = v.strip()
            elif k == 'token':
                self.token = v.strip()
            elif k == 'board_name':
                self.board_name = v.strip()
            elif k == 'username':
                self.username = v.strip()
            else:
                print('following information is not valid')
                print(k + ':' + v)

    def get_board_id(self):
        qstr = 'https://trello.com/1/members/' + self.username + '/boards?key=' + \
                self.credential_key + '&token=' + self.token + '&fields=name'
        try:
            qres = urlopen(qstr).read().decode('utf-8')
        except:
            print('Access error')
            sys.exit()
        
        # find specified board        
        qres = json.loads(qres)
        for name_id in qres:
            if name_id['name'] == self.board_name:
                self.board_id = name_id['id'].strip()
        
    def get_list_id(self, list_name):
        qstr = 'https://trello.com/1/boards/' + self.board_id + '/lists?key=' + \
                self.credential_key + '&token=' + self.token + '&fields=name'
        try:
            qres = urlopen(qstr).read().decode('utf-8')
        except:
            print('Access error: could not get list id')
            sys.exit()
        
        qres = json.loads(qres)
        for name_id in qres:
            if name_id['name'] == list_name:
                self.list_id = name_id['id'].strip()        
    
    def get_done_cards(self):
        qstr = 'https://api.trello.com/1/lists/' + self.list_id + \
                '/cards?key=' + self.credential_key + '&token=' + self.token + \
                '&filter=open'
        
        qres = urlopen(qstr).read().decode('utf-8')
        self.done_cards = json.loads(qres)
    
    def write_done_cards(self):
        outfn = 'trello_done_log_' + time.strftime('%Y-%m-%d') + '.md'
        fn = open(outfn, 'a+', encoding = 'utf-8')
        
        for card in self.done_cards:
            due = str(card['due'])
            if due != 'None':
                due = due[0:10].replace('-','/')
            write_str = '## ' + card['name'] + ' (' + due + ') \n\n\n'
            fn.write(write_str)

    def archive_all_dones(self):
        qstr = 'https://api.trello.com/1/lists/' + self.list_id + \
                '/archiveAllCards'
        post_data = {
                     'key':self.credential_key,
                     'token':self.token
                     }
        encoded_post_data = urllib.parse.urlencode(post_data).encode()
        # generate POST to archive all cards 
        urllib.request.urlopen(qstr, data = encoded_post_data)
        
    def batch_card_create(self, filepath):
        # import schedule list
        schedules = csv.reader(open(filepath, 'r'), delimiter = ',')
        
        for row in schedules:
            datebuf = row[1]
            counter_datesep = datebuf.count('/')
            error_flg = 0
            if counter_datesep == 1:
                datebuf = str(date.today().year) + '/' + datebuf
            elif counter_datesep == 2:
                datebuf
            else:
                error_flg = 1
            
            if error_flg == 0:
                qstr = 'https://trello.com/1/cards'
                post_data = {
                             'key': self.credential_key,
                             'token': self.token,
                             'idList': self.list_id,
                             'name': row[0],
                             'due': datebuf
                             }
                encoded_post_data = urllib.parse.urlencode(post_data).encode()
                urllib.request.urlopen(qstr, data = encoded_post_data)
            else:
                print('Error: date column is not correct format')
                print(row)
        
def make_log():
    ai = Trello_agent()
    ai.read_credential_file(os.getcwd() + '/credential')
    ai.get_board_id()
    ai.get_list_id('Done')
    ai.get_done_cards()
    ai.write_done_cards()
    ai.archive_all_dones()

def card_batch_generate():
    ai = Trello_agent()
    ai.read_credential_file(os.getcwd() + '/credential')
    ai.get_board_id()
    ai.get_list_id('Plan')
    ai.batch_card_create(os.getcwd() + '/trello_list.csv')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', default = 'archive', help = 'archive or create')
    args = parser.parse_args()
    
    if args.mode == 'archive':
        make_log()
    elif args.mode == 'create':
        card_batch_generate()
    else:
        print('Error: invalid mode is assigned')
    
