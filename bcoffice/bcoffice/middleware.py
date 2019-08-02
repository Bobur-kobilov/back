import json
from django.conf import settings

from django.core.exceptions import PermissionDenied
from django.http import HttpResponsePermanentRedirect
from django.urls import is_valid_path
from django.utils.deprecation import MiddlewareMixin
from django.middleware.common import CommonMiddleware
from .message import ResponseMessage

class BackofficeCommonLoggingMiddleware(CommonMiddleware):
    def process_request(self, request):
        """
        Check for denied User-Agents and rewrite the URL based on
        settings.APPEND_SLASH and settings.PREPEND_WWW
        """
        print("REQUEST START")
        
        # Check for denied User-Agents
        if 'HTTP_USER_AGENT' in request.META:
            for user_agent_regex in settings.DISALLOWED_USER_AGENTS:
                if user_agent_regex.search(request.META['HTTP_USER_AGENT']):
                    raise PermissionDenied('Forbidden user agent')

        # Check for a redirect based on settings.PREPEND_WWW
        host = request.get_host()
        must_prepend = settings.PREPEND_WWW and host and not host.startswith('www.')
        redirect_url = ('%s://www.%s' % (request.scheme, host)) if must_prepend else ''

        # Check if a slash should be appended
        if self.should_redirect_with_slash(request):
            path = self.get_full_path_with_slash(request)
        else:
            path = request.get_full_path()

        # Return a redirect if necessary
        if redirect_url or path != request.get_full_path():
            redirect_url += path
            return self.response_redirect_class(redirect_url)

    def process_response(self, request, response):
        if response.status_code == 404:
            if self.should_redirect_with_slash(request):
                return self.response_redirect_class(self.get_full_path_with_slash(request))
        elif response.status_code == 403:
            forbidden_data = ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00029)
            response.content = json.dumps(forbidden_data)


        if settings.USE_ETAGS and self.needs_etag(response):
            warnings.warn(
                "The USE_ETAGS setting is deprecated in favor of "
                "ConditionalGetMiddleware which sets the ETag regardless of "
                "the setting. CommonMiddleware won't do ETag processing in "
                "Django 2.1.",
                RemovedInDjango21Warning
            )
            if not response.has_header('ETag'):
                set_response_etag(response)

            if response.has_header('ETag'):
                return get_conditional_response(
                    request,
                    etag=response['ETag'],
                    response=response,
                )
        # Add the Content-Length header to non-streaming responses if not
        # already set.
        if not response.streaming and not response.has_header('Content-Length'):
            response['Content-Length'] = str(len(response.content))

        return response