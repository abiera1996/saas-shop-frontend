from django.conf import settings
from threading import Thread
import logging, requests, json
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _

import hashlib
import datetime

logging = logging.getLogger('django')

DIMES_BASE_URL = "http://localhost:8000"

class CustomException(exceptions.APIException):
    status_code = 500
    default_detail = _('Invalid input.')
    default_code = 'invalid'

    def __init__(self, detail=None, code=None, status_code=500):
        self.status_code = status_code
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        # For validation failures, we may collect many errors together,
        # so the details should always be coerced to a list if not already.
        if isinstance(detail, tuple):
            detail = list(detail)
        elif not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = exceptions._get_error_details(detail, code)


class API:
    dimesUrl = DIMES_BASE_URL

    headers = {"Content-Type": "application/json"}
    code = None
    method = ''

    def __init__(self, request):
        self.request = request

    def api_logging(self, url, method, headers, payload, result):
        if payload:
            try:
                payload = json.loads(payload)
            except:
                pass
        logging_data = {
            "url": url,
            "method": method,
            "headers": headers,
            "payload": payload,
            "status_code": result.status_code,
        }
        try:
            response_data = result.json() 
        except:
            response_data = {}
        
        logging_data.update({"response": response_data})
        
        if result.status_code in [200, 201]:
            logging.debug(logging_data)
        else:
            logging.error(logging_data)

    def http_request(
        self, url_path, method, parameters="", xheaders=None, payload={}, base_url=1
    ) -> requests.Response: 
        self.base_url = base_url
        self.method = method

        if xheaders:
            if not type(xheaders).__name__ == "dict":
                assert "Invalid header format"
            
        headers = self.get_headers(xheaders=xheaders)
        url = self.get_url(url_path)
    
        result=None   
        result = requests.__dict__[method](
            url, headers=headers, params=parameters, data=json.dumps(payload), timeout=1000*30
        )   
        data = {}
        if parameters:
            data = parameters
        elif payload:
            data = payload
            
        Thread(
            target=self.api_logging, 
            daemon=True, 
            args=(url, method, headers, data, result)
        ).start()
          
        response_data = {}
     
        try:
            response_data = result.json() 
        except Exception as e: 
            response_data = {
                "message": f"Server Error",
                "data": {}
            }
        
        response_data = {
            **response_data, 
            'status_code': result.status_code
        } 

        return response_data

    def get_url(self, url_path):
        if self.base_url == 1:
            domain = self.dimesUrl 
        return domain + url_path


    def get_headers(self, xheaders={}):
        merge_headers = self.headers 
        if self.base_url == 1:
            auth_header = {}  
            if self.request.user.is_authenticated:
                auth_header = {"Authorization": f"Bearer {self.request.session['token']}"}
            else:
                auth_header = {"api-key": settings.API_KEY}
            if auth_header:
                merge_headers = {**merge_headers, **auth_header}
        
        if xheaders:
            merge_headers = {**merge_headers, **xheaders}
        
        return merge_headers
 