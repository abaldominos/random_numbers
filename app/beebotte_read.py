from beebotte import *
_hostname   = 'api.beebotte.com'
_token      = '1510099700783_0F8OPqJwsCC25m20'
bbt = BBT(token = _token, hostname = _hostname)
records = bbt.read("Numbers_Database", "numbers", limit = 10)
for document in records:
    print(document["data"])