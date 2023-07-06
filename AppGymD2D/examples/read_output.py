import re

filename='out.txt'
info=""
with open(filename) as f:
    while True:
        c = f.read(1)
        if not c:
            print("End of file")
            break
        if c=='{':
        	while True:
        		c=f.read(1)
        		if c=='}':
        			end="true"
        			break
        		if c=='{':
        			info=""
        			end="false"
        			continue
        		else:
        			info=info+c
        	print(info)
        	val=re.split(":|,", info)
        	print(val[9])
        	info=""



