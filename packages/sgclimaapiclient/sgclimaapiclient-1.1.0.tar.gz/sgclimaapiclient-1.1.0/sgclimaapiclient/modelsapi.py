import json
from io import BytesIO

import requests
import pandas as pd


class SGClimaModelsAPI:

    def __init__(self, token, endpoint='https://models-api.dc.indoorclima.com', verify=False):
        self.token = token
        self.endpoint = endpoint
        self.verify = verify

    def _call(self, url, params={}, json_payload={}, headers={}):
        api_url = self.endpoint + url
        headers['Api-Key'] = self.token
        r = requests.get(api_url, verify=self.verify, headers=headers, params=params, data=json_payload)
        if r.status_code >= 400:
            try:
                raise ResponseCodeException(json.loads(r.content))
            except json.decoder.JSONDecodeError:
                raise ResponseCodeException(str(r.content))
        return r

    def _call_json(self, *args, **kwargs):
        return self._call(*args, **kwargs).json()

    def _call_df(self, url, format="json", *args, **kwargs):
        r = self._call(url, *args, **kwargs)
        if format == "json":
            df = pd.read_json(r.content, orient='records', lines=True)
        else:
            df = pd.read_csv(BytesIO(r.content))
        return df

    def list_models(self):
        """
        List models
        :return: List with a JSON of registered models
        """
        return self._call_json("/ml/list")

    def get_model(self, id):
        """
        Get model by id
        :return: List with a JSON of registered models
        """
        return self._call_json("/ml/{id}/".format(id=id))

    def predict(self, id, df, version="production"):
        params = {"version": version}
        data = df.to_json(orient="split")
        headers = {'Content-Type': 'application/json; format=pandas-split'}
        df = self._call_df(url="/ml/predict/{id}".format(id=id), params=params, json_payload=data, headers=headers)
        df = df.stack().to_frame().reset_index()[[0]]
        df.columns = ["prediction"]
        return df


class ResponseCodeException(Exception):
    """
    Exception raised when the API returns an unexpected response code
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
