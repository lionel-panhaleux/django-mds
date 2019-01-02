from mds.server.settings import AUTH_MEANS


def conf_check_middleware(get_response):

    if not AUTH_MEANS:
        raise Exception(
            "JWT authentication configuration is incomplete: neither secret nor public key found"
        )

    def middleware(request):
        return get_response(request)

    return middleware
