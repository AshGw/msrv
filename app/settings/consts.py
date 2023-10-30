class Route:
    SERVER_GENERATE: str = "/server-gen"
    SERVER_TOKEN_GENERATE: str = "/token"
    SERVER_CLIENT_TOKEN_GENERATE: str = "/token-client"
    CLIENT_GENERATE: str = "/generate"


class TestRoute:
    peg = "/test"
    CLIENT_RATE_LIMITER: str = peg + "/rate-limit"
    CLIENT_AUTH: str = peg + "/client-auth"
    SERVER_AUTH: str = peg + "/server-auth"


class ClientPlan:
    PRO = "pro"
