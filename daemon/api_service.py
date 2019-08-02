import requests


class APIService:
    METHOD_MAP = {
        'GET': requests.get
        , 'POST': requests.post
        , 'PUT': requests.put
        , 'DELETE': requests.delete
    }
    """
    API 요청 메서드
    @param request API 요청 request 객체
    @param url API URL 주소
    @param params API 호출시 전송할 파라미터 값들(Dictonary)
    @return Response
    """
    def rpc_call(url=None, params=None, method=None, is_json=False, timeout=None):
        request_func = APIService.METHOD_MAP[method.upper()]
        response = None

        if method == 'get':
            if timeout is None:
                response = request_func(url, params=params)
            else:
                response = request_func(url, params=params, timeout=timeout)
        elif method == 'post':
            if is_json:
                if timeout is None:
                    response = request_func(url, json=params)
                else:
                    response = request_func(url, json=params, timeout=timeout)
            else:
                if timeout is None:
                    response = request_func(url, data=params)
                else:
                    response = request_func(url, data=params, timeout=timeout)
        elif method == 'put':
            if timeout is None:
                response = request_func(url, data=params)
            else:
                response = request_func(url, data=params, timeout=timeout)
        elif method == 'delete':
            if timeout is None:
                response = request_func(url)
            else:
                response = request_func(url, timeout=timeout)

        return response.json()
