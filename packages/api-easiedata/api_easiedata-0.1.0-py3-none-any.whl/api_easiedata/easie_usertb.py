import json
import os
import pandas as pd
import requests
import time
import zipfile

class EasieUsertb():
    def __getitem__(self, k):
        try:
            return getattr(self, k)
        except:
            return None

    def __init__(self, username, developer_key, url_api="https://api.easiedata.com", workspace_abs_path=None):
        self.url_api = url_api
        self.username = username
        self.developer_key = developer_key

        if workspace_abs_path is None:
            workspace_abs_path = os.getcwd()

        self.path = workspace_abs_path + '/'
        self.headers = {
            'Authorization': json.dumps({
                'username': self.username,
                'developer_key':self.developer_key
            })
        }

        return None

    def post_easieusertb(
        self, action, table_name, params={}, df=None):

        files = None
        if df is not None:
            timedelta_cols = [col for col in df.columns if df[col].dtype == 'timedelta64[ns]']
            df[timedelta_cols] = df[timedelta_cols].astype(str)

            file_name = table_name + 'temp'
            zip_name = file_name + '.zip'
            file_name += '.json'

            filepath = self.path + file_name
            zip_path = self.path + zip_name

            df.to_json(filepath, orient='table')

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                zf.write(os.path.join(self.path, file_name), file_name)

            with open(zip_path, 'rb') as f:
                files = {'data': ('df', f, 'application/json')}

                r = requests.post(
                    self.url_api + '/developer/easie_usertb',
                    headers=self.headers,
                    data={'action':action, 'front_tablename': table_name, 'params':json.dumps(params)},
                    files=files
                )

            try:
                os.remove(zip_path)
                os.remove(filepath)
            except Exception as e:
                print('Created files couldn\'t be removed')
                print(e)

        else:
            r = requests.post(
                self.url_api + '/developer/easie_usertb',
                headers=self.headers,
                data={'action':action, 'front_tablename': table_name, 'params':json.dumps(params)},
                files=files
            )

        try:
            self.res = r.json()
        except:
            self.res = r

        self.http_status = r.status_code
        return self

    def get_easieusertb(self, table_name, params={}):
        r = requests.post(
            self.url_api + '/developer/add_to_queue',
            headers=self.headers,
            data={'action':'get_df', 'front_tablename': table_name, 'method': 'GET', 'params': json.dumps(params)}
        )

        self.res = r
        self.http_status = self.res.status_code
        try:
            self.res = r.json()
        except:
            self.res = r

        if self.http_status != 200:
            return self

        self.queue_pk = self.res['data'][0]
        self.token = self.res['data'][1]

        done = 0
        while(not done):
            time.sleep(2)
            r = requests.get(
                self.url_api + '/developer/check_if_done',
                headers=self.headers,
                data={'pk': self.queue_pk, 'token': self.token}
            )

            try:
                self.res = r.json()
            except:
                self.res = r

            if self.http_status != 200:
                return self

            done = self.res['data']

        r = requests.get(
            self.url_api + '/developer/easie_usertb_get',
            headers=self.headers,
            data={'pk': self.queue_pk, 'token': self.token}
        )

        self.http_status = r.status_code
        if self.http_status == 200:
            zip_path = self.path + 'temp_zip.zip'
            zip_file = r.content

            with open(zip_path, 'wb') as z:
                z.write(zip_file)

            with zipfile.ZipFile(zip_path, 'r') as zf:
                name_list = zf.namelist()
                zf.extractall(self.path)

            filepath = self.path + name_list[0]
            with open(filepath, 'rb') as f:
                self.df = pd.read_json(f, orient='table')
                self.res = {
                    'success': True,
                    'front_msg': 'Success!'
                }

            try:
                os.remove(zip_path)
                os.remove(filepath)
            except Exception as e:
                print('Created files couldn\'t be removed')
                print(e)
        else:
            try:
                self.res = r.json()
            except:
                self.res = r

        return self
