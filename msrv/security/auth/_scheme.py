from fastapi.security import OAuth2PasswordBearer

from msrv.settings.urls import URL

scheme = OAuth2PasswordBearer(tokenUrl=URL.Token.Client.PREFIX, auto_error=False)
# auto_erros set to True ==> will lock the whole api unless u have a bearer token of either client
# or server scope
