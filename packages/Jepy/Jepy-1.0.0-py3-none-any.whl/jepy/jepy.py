import warnings
from datetime import datetime
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
from quick_rest import Client, JWTClient, ServerResponse
from jepy.jepy_exceptions import ArgumentError, ServerError
from typing import Any, Union
from requests.models import Response



class JepyServerResponse(ServerResponse):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def auto(self, encoding: str = '') -> Union[dict, list]:
        if not encoding:
            encoding = self.encoding
        result = self.decode(encoding)
        if 'results' in result:
            return result['results']
        elif 'message' in result:
            return result['message']
        elif 'error' in result:
            raise ServerError(result['error'])

    def to_xml(self,
        export_path: str,
        custom_root: str = 'api_data',
        ignore_type: bool = False,
        **kwargs: Any
    ) -> None:
        response = self.decode()
        if not ignore_type and not isinstance(response, dict):
            error = (
                'Server response content is not a dict. Cannot build XML from'
                ' dict automatically. Can try to convert the response before'
                ' XML creation with to_xml(ignore_type=True).'
                )
            raise TypeError(error)
        xml = dicttoxml(response, custom_root=custom_root, **kwargs)
        dom = parseString(xml)
        legible_xml = dom.toprettyxml()
        with open(export_path, 'w') as xml_file:
            xml_file.write(legible_xml)


class Jepy(JWTClient):
    def __init__(self,
        username: str = '',
        password: str = '',
        vprefix: str = 'v0/',
        **kwargs: Any
    ) -> None:
        if not username and kwargs.get('user_id', ''):
            username = kwargs.pop('user_id')
            warning_msg = (
                'The "user_id" parameter has been replaced with "username" and'
                ' will be removed in a future release.'
                )
            if 'ignore' in [i[0] for i in warnings.filters if (i[2] == DeprecationWarning)]:
                warning_msg = f'Deprecation warning: {warning_msg}'
                warning_type = UserWarning
            else:
                warning_type = DeprecationWarning
            warnings.warn(warning_msg, warning_type)
        if not username and password:
            warning_msg = (
                "No credentials supplied, the server will automatically"
                " deny all requests other than checking status. Use"
                " keyword arguments user_id and password to make other calls."
                )
            warnings.warn(warning_msg)
        self.vprefix = vprefix
        creds = {"username": username, "password": password}
        settings = {
            'auth_route': 'auth',
            'token_name': 'access_token',
            'jwt_key_name': 'Authorization',
            'jwt_prefix': 'JWT '
            }
        super().__init__('https://je-api.com/', creds, **settings, **kwargs)

    # Same as quick_rest.ServerResponse but returns JepyServerResponse
    def _handle_response(self, response: Response) -> JepyServerResponse:
        code = str(response.status_code)[:1]
        if code not in ('2', '3') and not self.ignore_errors:
            raise ServerError(f'{response.status_code}: {response.reason} {response.text}')
        else:
            return JepyServerResponse(response, encoding=self.encoding,
                                  values_key=self.values_key)

    def get(self, route: str, **kwargs: Any) -> JepyServerResponse:
        route = f'{self.vprefix}{route}'
        return super().get(route, **kwargs)

    def claims(self, **kwargs: Any) -> JepyServerResponse:
        if len(kwargs) > 1:
            raise ArgumentError('Too many keyword arguments, use only one.')
        else:
            if 'detailed_list' in kwargs:
                if kwargs['detailed_list'] == True:
                    return self.get(f'claims/view_all_detail.json')
            elif 'claim_num' in kwargs:
                return self.get(f"claims/{kwargs['claim_num']}.json")
            else:
                return self.get(f'claims/view_all.json')

    def notes(self, claim_num: str) -> JepyServerResponse:
        return self.get(f'notes/{claim_num}.json')

    def checks(self,
        endpoint: str = 'checks',
        **kwargs: Any
    ) -> JepyServerResponse:
        claim_num = kwargs.get('from_date', 'all')
        from_date = kwargs.get('from_date', False)
        to_date = kwargs.get('to_date', False)
        if from_date:
            from_date = datetime.strptime(kwargs['from_date'], '%Y%m%d').date()
        if to_date:
            to_date = datetime.strptime(kwargs['to_date'], '%Y%m%d').date()
        return self.get(f'{endpoint}/{from_date}/{to_date}/{claim_num}.json')

    def reserves(self, **kwargs: Any) -> JepyServerResponse:
        return self.checks(endpoint='reserves', **kwargs)

    def additional(self, claim_num: str) -> JepyServerResponse:
        return self.get(f'additional/{claim_num}.json')

def status() -> str:
    client = Client('https://je-api.com/')
    response = client.get('').decode().get('message', None)
    return response
