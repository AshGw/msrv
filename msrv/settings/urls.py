from msrv.lib.env import Env


class URL:
    class Index:
        PREFIX: str = "/"

    class Docs:
        class Swagger:
            PREFIX: str = Env.Prod.SWAGGER_DOCS_PATH

    class Token:
        class Index:
            PREFIX: str = "/token"

        class Server:
            PREFIX: str = "/token/server"

        class Client:
            PREFIX: str = "/token/u"

            class Refresh:
                PREFIX: str = "/token/u/refresh"
                # rate limit this endpoint & also oauth

    class Generate:
        class Index:
            PREFIX: str = "/generate"

        class Free:
            PREFIX: str = "/generate/free"

        class Hobby:
            PREFIX: str = "/generate/hobby"

        class Pro:
            PREFIX: str = "/generate/pro"

        class Server:
            PREFIX: str = "/generate/srv"

    class Test:
        class Index:
            PREFIX: str = "/test"

        class ServerAuth:
            PREFIX: str = "/test/auth/server"

        class ClientAuth:
            PREFIX: str = "/test/auth/client"

        class RateLimit:
            PREFIX: str = "/test/rate-limit"

        class ThrowAwaytests:
            PREFIX: str = "/test/throw-away-tests"
