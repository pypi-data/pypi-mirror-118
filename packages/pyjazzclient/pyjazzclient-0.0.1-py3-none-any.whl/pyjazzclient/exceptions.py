class JazzClientRequestError(Exception):
    def __init__(self, request, response):
        self.request = request
        self.response = response
