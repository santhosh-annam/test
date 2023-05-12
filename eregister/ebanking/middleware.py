from django.utils.cache import add_never_cache_headers
import urllib.parse
import re
import json


class CustomMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        try:
            callback_url = request.GET.get('callback_url', "")

            if callback_url:
                callback_url = str(urllib.parse.unquote_plus(callback_url))

            add_never_cache_headers(response)

            report_endpoint = "/csp-violation-report/"

            response['Referrer-Policy'] = 'no-referrer'
            # response['X-XSS-Protection'] = '1; mode=block'

            csp = """default-src 'self';
            script-src 'self' 'unsafe-inline';
            style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
            font-src 'self' https://fonts.googleapis.com
            https://gstsatic.com https://fonts.gstatic.com;
            style-src-elem 'self' https://fonts.googleapis.com;
            base-uri 'self';
            object-src 'none';
            form-action 'self' {0};
            sandbox allow-scripts allow-forms allow-popups
            allow-same-origin allow-modals;
            report-uri {1};
            report-to cspendpoint"""

            try:
                report_url = "{0}://{1}{2}".format(request.scheme,
                                                   request.META['HTTP_HOST'],
                                                   report_endpoint)
                report_to = {"group": "cspendpoint",
                             "max_age": 31536000,
                             "endpoints": [
                                 {"url": report_url}
                                 ]
                             }
                response['Report-To'] = json.dumps(report_to)
            except Exception as e1:
                print(e1)

            csp = re.sub('\s+', " ", csp.format(callback_url, report_endpoint))
            response['Content-Security-Policy'] = csp
        except Exception as e2:
            print(e2)
        return response
