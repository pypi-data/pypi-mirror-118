import requests
import pandas as pd
from datetime import datetime


class SGClimaDataAPI:

    def __init__(self, token, endpoint='http://api.indoorclima.com'):
        self.token = token
        self.endpoint = endpoint

    def _call(self, url):
        api_url = self.endpoint + url
        r = requests.get(api_url, verify=False, headers={'Api-Key': self.token})
        return r.json()

    def _call_df(self, url, start_day, end_day):
        try:
            if isinstance(start_day, str) and isinstance(end_day, str):
                start_day = datetime.strptime(start_day, "%Y-%m-%d")
                end_day = datetime.strptime(end_day, "%Y-%m-%d")

            api_url = self.endpoint + url
            r = requests.get(api_url, verify=False, headers={'api_key': self.token}, 
                params={'start_day': start_day.strftime("%Y-%m-%d"), 
                        'end_day': end_day.strftime("%Y-%m-%d")})
            df = pd.read_json(r.content, orient='records', lines=True)
            return df
        except ValueError as e:
            print(f'[ERROR]: Both dates must be provided as date objects or in YYYY-MM-DD format ({e})')

    def get_site(self, id):
        return self._call("/sites/{id}".format(id=id))

    def get_zone(self, id):
        return self._call("/zones/{id}".format(id=id))

    def get_equipment(self, id):
        return self._call("/equipments/{id}".format(id=id))

    def get_site_data(self, id, start_day, end_day):
        df = self._call_df("/sites/{id}/data/download/json".format(id=id),
                            start_day, end_day)
        return df

    def get_zone_data(self, id, start_day, end_day):
        df = self._call_df("/zones/{id}/data/download/json".format(id=id),
                            start_day, end_day)
        return df


    def get_equipment_data(self, id, start_day, end_day):
        df = self._call_df("/equipments/{id}/data/download/json".format(id=id),
                             start_day, end_day)
        return df

    # this method extracts pids from layout
    def extract_pids(self, x):
        pids = []
        if type(x) == dict:
            for k, v in x.items():
                if k.endswith('_pid'):
                    try:
                        pids.append({k: int(v)})
                    except TypeError:
                        # print(k, '=>', v, 'is not ok')
                        pids.append({k: None})
                        pass
                    except ValueError:
                        pids.append({k: None})
                else:
                    pids.extend(self.extract_pids(v))
        elif type(x) == list:
            for v in x:
                pids.extend(self.extract_pids(v))
        return pids

    def extract_filtered_pids(self, x, tags=None):
        pids = []
        if type(x) == dict:
            for k, v in x.items():
                if k.endswith('_pid'):
                    try:
                        if k in tags:
                            pids.append(str(v))
                    except TypeError:
                        pass
                    except ValueError:
                        pass
                else:
                    pids.extend(self.extract_filtered_pids(v, tags))
        elif type(x) == list:
            for v in x:
                pids.extend(self.extract_filtered_pids(v, tags))
        return pids