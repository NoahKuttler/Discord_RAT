import base64
import codecs

r13code = open('encoded.txt', 'r').read()
b64code = codecs.decode(r13code, 'rot_13')
code = base64.b64decode(b64code.encode('utf-8')).decode('utf-8')

exec(code)