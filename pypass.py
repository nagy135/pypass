#!/bin/python

import pickle
import os
import getpass
from subprocess import call
from encoder import encrypt, decrypt

colors = {
            'red' : "\033[31m",
            'green' : "\033[32m",
            'yellow' : "\033[33m",
            'light_yellow' : "\033[35m",
            'blue' : "\033[34m",
            'cyan' : "\033[34m",
            'bold' : "\033[1m",
            'end' : "\033[00m"
        }

class Pypass(object):
    def __init__(self, master_pass=None):
        self.data = list()
        self.directory = os.path.expanduser("~") + '/.config/pypass/'
        self.load_data()
        self.master_pass = master_pass

    def get_master_password(self):
        return getpass.getpass("master password: ")

    def create_db(self):
        if not os.path.exists(self.directory):
            print('Creating self.directory structure {}'.format(self.directory))
            os.makedirs(self.directory)
        print('Creating {}db.dat file'.format(self.directory))
        self.save_data()

    def load_data(self):
        try:
            home_folder = os.path.expanduser("~")
            with open(self.directory + "db.dat", "rb") as t:
                self.data = pickle.load(t)
            return True
        except Exception as e:
            self.create_db()
            return False

    def save_data(self):
        home_folder = os.path.expanduser("~")
        with open(self.directory + "db.dat", "wb") as t:
            pickle.dump(self.data, t)

    def add_record(self):
        if self.master_pass is None:
            self.master_pass = self.get_master_password()
        username = input("username: ")
        password = getpass.getpass("password: ")
        website = input("website: ")
        description = input("description: ")
        key = input("key: ")
        record = {
                'username': username,
                'password': encrypt(self.master_pass, password),
                'website': website,
                'description': description,
                'key': key
        }
        self.data.append(record)
        self.save_data()

    def delete(self, record_index):
        if len(self.data) == 0:
            raise Exception('No records to delete from')
        deleted_record = self.data.pop(record_index)
        self.save_data()
        print('successfully removed record')
        print(deleted_record)

    def record_to_clipboard(self, record_index=None, record_key=None):
        if record_index is not None:
            record_index = int(record_index)
        if self.master_pass is None:
            self.master_pass = self.get_master_password()
        if record_key is not None:
            for i, record in enumerate(self.data):
                if record['key'] == record_key:
                    record_index = i
            if record_index is None:
                raise Exception('No record with given key')
        os.system('echo "' + str(decrypt(self.master_pass, self.data[record_index]['password']).decode('cp1252')) + '" | xclip -r -selection clipboard')

    def print(self, decrypt_password=False, record_index=None, record_key=None):
        if decrypt_password and self.master_pass is None:
            self.master_pass = self.get_master_password()
        print(colors['red'] + '########### PASSWORDS #########' + colors['end'])
        for i,record in enumerate(self.data):
            if record_index is not None and record_index != i:
                continue
            if record_key is not None and record['key'] != record_key:
                continue
            key = ''
            if record['key'] != '':
                key = ' :: ' + record['key']
            print(colors['cyan'] + '#' + str(i) + key + colors['end'])
            print(colors['bold'] + 'username: ' + colors['end'] + '{}'.format(record['username']))
            if decrypt_password:
                try:
                    print(colors['green'] + 'password' + colors['end'] + ': {}'.format(decrypt(self.master_pass,record['password']).decode('cp1252')))
                except UnicodeDecodeError:
                    print(colors['green'] + 'password' + colors['end'] + ': decryption failed')
            else:
                print('password: {}'.format(record['password']))
            if record['website'] != '':
                print(colors['bold'] + 'website' + colors['end'] + ': {}'.format(record['website']))
            if record['description'] != '':
                print(colors['bold'] + 'description' + colors['end'] + ': {}'.format(record['description']))
            print(colors['red'] + '###'+ colors['end'])

if __name__ == "__main__":
    instance = Pypass()
    # instance.add_record()
    # instance.data = list()
    # instance.save_data()
    instance.print(decrypt_password=True)
