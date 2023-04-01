import requests

from .checker import ValidationError, register_check


@register_check()
def check_http_request(context: dict, args: dict) -> str:
    if "app_url" not in context:
        raise Exception("app_url is not present in context vars")

    app_url = context["app_url"]

    endpoint = args["endpoint"]
    method = args.get("method", "GET")
    payload_json = args.get("json")
    payload_data = args.get("data")
    request_headers = args.get("request_headers")
    allow_redirects = args.get("allow_redirects")

    expected_status = args.get("expected_status")
    expected_json = args.get("expected_json")
    # TODO: add support for expected_headers, and other parameters...

    url = app_url + endpoint

    request_kwargs = {
        "json": payload_json,
        "data": payload_data,
        "headers": request_headers,
        "allow_redirects": allow_redirects
    }
    request_kwargs = {k: v for k, v in request_kwargs.items() if v is not None}

    r = requests.request(
        method=method, url=url, **request_kwargs)

    if expected_status is not None and r.status_code != expected_status:
        raise ValidationError("check-http-request: unexpected status code\n"
                              f"Expected status: {expected_status}\n"
                              f"Actual status: {r.status_code}\n"
                              f"Endpoint: {endpoint}\n"
                              f"Full URL: {url}")
    if expected_json is not None:
        try:
            response_json = r.json()
        except requests.exceptions.JSONDecodeError:
            raise ValidationError("check-http-request: JSON decode error\n"
                                  "Response couldn't be decoded as JSON\n"
                                  f"Actual response: {r.content.decode()}")
        if response_json != expected_json:
            raise ValidationError("check-http-request: JSON response doesn't match expected response\n"
                                  f"Expected JSON response: {expected_json}\n"
                                  f"Actual JSON response: {response_json}")
