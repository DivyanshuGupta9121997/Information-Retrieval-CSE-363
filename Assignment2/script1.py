import os

for root,dirs,files in os.walk('/home/dg/Desktop/Assignment2/20news_18828'):
	if not dirs:
		for f in files:
			print(os.path.join(root,f))
