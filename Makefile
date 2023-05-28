
req:
	@pip freeze > requirements.txt

i:
	@pip install -i https://pypi.douban.com/simple $(p)