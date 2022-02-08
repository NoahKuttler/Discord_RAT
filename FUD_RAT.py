import base64

b64code = open('encoded.txt', 'rb').read()
code = base64.b64decode(b64code).decode('utf-8')

exec(code)