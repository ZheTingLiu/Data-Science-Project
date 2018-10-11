import requests
from bs4 import BeautifulSoup

def get_comment(url):
	payload = {
		'from' : '/bbs/Gossiping/index.html',
		'yes' : 'yes'
		}
	rs = requests.session()
	response = rs.post('https://www.ptt.cc/ask/over18', verify = False, data = payload)
	response = rs.get(url)
	content = response.content
	content = bytes.decode(content)
	content = content.replace('//images.ptt.cc/bbs/v2.25/','./')
	content = str.encode(content)
	open('demo.html', 'wb').write(content)
	soup = BeautifulSoup(response.text,'html.parser')
	com = soup.find_all('span','f3 push-content')
	usr = soup.find_all('span','f3 hl push-userid')
	user=[]
	comment=[]
	for row in com:
		comment.append(row.text[2:])
	for row in usr:
		user.append(row.text)
	return comment,user
		
# get_comment('https://www.ptt.cc/bbs/Gossiping/M.1528699755.A.2B9.html')