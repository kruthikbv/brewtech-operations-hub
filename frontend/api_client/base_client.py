import os
import requests
from dotenv import load_dotenv
load_dotenv()


class APIClient:
    def __init__(self, token=None):
        self.base_url = os.getenv('BACKEND_API_BASE_URL', 'http://127.0.0.1:8000/api/v1').rstrip('/')
        self.token = token

    def request(self, method, path, **kwargs):
        headers = kwargs.pop('headers', {})
        headers.update({'Authorization': f'Bearer {self.token}'} if self.token else {})
        response = requests.request(method, f'{self.base_url}/{path.lstrip("/")}', headers=headers, timeout=15, **kwargs)
        if response.status_code == 401 and self.token:
            response = self._refresh_and_retry(method, path, headers, kwargs)
        if not response.ok:
            try:
                payload = response.json()
                detail = payload.get('detail', payload) if isinstance(payload, dict) else payload
            except ValueError:
                detail = response.text
            raise RuntimeError(detail or 'Request failed')
        return response.json() if response.content else None

    def _refresh_and_retry(self, method, path, headers, kwargs):
        try:
            import streamlit as st
            refresh_token = st.session_state.get('refresh_token')
            if not refresh_token:
                return requests.Response()
            refresh_response = requests.post(f'{self.base_url}/auth/refresh/', json={'refresh': refresh_token}, timeout=15)
            if not refresh_response.ok:
                return refresh_response
            self.token = refresh_response.json()['access']
            st.session_state.access_token = self.token
            headers['Authorization'] = f'Bearer {self.token}'
            return requests.request(method, f'{self.base_url}/{path.lstrip("/")}', headers=headers, timeout=15, **kwargs)
        except (KeyError, requests.RequestException):
            return requests.Response()

    def get(self, path, **kwargs): return self.request('GET', path, **kwargs)
    def post(self, path, **kwargs): return self.request('POST', path, **kwargs)
    def patch(self, path, **kwargs): return self.request('PATCH', path, **kwargs)
    def delete(self, path, **kwargs): return self.request('DELETE', path, **kwargs)

    def all(self, path, **params):
        payload = self.get(path, params={**params, 'page_size': 100})
        return payload.get('results', payload) if isinstance(payload, dict) else payload
