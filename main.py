#!/usr/bin/python2

from flask import Flask, render_template, request, Response
from waitress import serve
from os import getenv, environ
from subprocess import Popen, PIPE
from socket import socket, AF_INET, SOCK_STREAM, gaierror
from errno import errorcode
from json import dumps
from time import time 
import ssl
import urllib2
from datetime import datetime

app = Flask(__name__)

port = int(getenv("PORT",8081))

@app.route('/')
def root():
	enterprise = 'Fiserv'
	headerImg = 'data:image/png;base64,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'
	footerImg = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMAAAAA0CAYAAADc3zcIAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAYdEVYdFNvZnR3YXJlAHBhaW50Lm5ldCA0LjAuOWwzfk4AAAvcSURBVHhe7Z1/jB1VFceX/qClpaJBGmJqbBNJTIOKPyIQRVH5w2AaIQiYYrTlx6uhpamgFIK1asBqtJZUkBKNJdJIIDStQqwY41ak2oClVGLWrgUWRJYWaBfY0nZ33z1+z9w7O3funDdv3rz7pvPW+SafzNuZe+6vd87MvXdm3vYQUUVJqVSApI6vKAeVCpDU8RXloFIBkjq+ohxUKkBSx1eUg0oFSOr4inJQqQBJHe+NWs9ccDvYDsjiO2L6ihjdJNR3qlLqPHA92Fqv13eBfzP4+2mwDdyGdBeAU4zZ8VfY2d6p9VwEhiynrwKgRbpBqOcpcOwr4Oh92I7h71RxGnAQ3AzebbI5fkKdOkOtZ8BxepsqADJQZqF+k+DA58Lx/wHq+FtLKaLh14heHSAa7Cd6qY/oleeI3jhAVI/HB8wOII+F+DjVZFu8ULh/aj3nOw5v0wsWiXYVMcoq1O0EOO5XsR0CWmMjRP2PkdrwZVI3zye1/HRSX3sbqdpMUstmk7rxDFLrFpB6/AGio28ao+CKcASBsB7bmSb7YoU6+EcOgC3g7WL6CpEyCvWaDGddCqc9gs8QzvjP7CS1/mJSiyaDSc359odJPbFZm0PIrw7uBNNMMcUJ5fun1rPCcvyQi8S0FQ0po0ZHRy+B8x9F/XDWHyX60wZ9ppccPY3FU0htrBGNvBVkBecfQ74/NsUUJ5TtHx7jJwPgfDFtRUPKJjjpmeBl1I0H8ESbV5G6aprs4FlYjCvGTy/BkGg4yJKDACwwxRUjlOufKgC8UCahPpNwhv4Ntlo77yN19XTZsVsBVwK67xvjE2QEwB5Q3HwAZfqnCgAvlEkjIyMfgWPqoc8br2Bie5rs0HnAEIr6eoOsWSjnMlNs54Xy/FMFgBfKJDgl38TSZ+pNy2VHboc1cA+eU3AR9XovyitmQozy/FMFgBeOt+CEJzGoC6/87MOW6PX9pK5/j+zE7VCbSbT3L0ERKOt1MM9Uo7NCef7xHQC1nrMCe75/oO8w8+dsS6o6La9KcZ1COI+5Yvo0onoUspxbtFAm39U9G/wIZ+Ed2L5gGAAKx4n+9Wc9eZWcuF0e/kFQBJcFfc5Uq7NCef5IOn0j9J3gRvuj/NjZ0u4o8zNGcmDpYEmzZe4BcWeWnlviNPH9YTDa6fR+O6/GeR4S0zkUJZQ1BQ53MdgFRvB3Yz2wUnZeH9x5uSkkGAb9EHXBZYFmgBPBJFNdv0LG/oh/yWk0DwB9lnaPNyJ+j0E/gCelk+DnlaIgkAPA3ccBwNj7GPkRj+QzUdvFdA5FiJ0MbAT6DB+K/3z1ef1Ig/0Iw4YrZOf1AN1yJgpwq6GOAg5MruOXsGuGqbofIUN/xL/kNLIEQLOztw3fkseHwI6fQJXSME8J+5h7LHvX2d2/GT0MSu6/fTwfm6zpHDotONS7wOMoS4sfZ+jbTuquhaSum03qyimGqaRuO4/o0V+SuvXjovP6gG55PyoRDwBbqCtrEB9r2PpZKkVm/qj1rDbw8z7ul74RhMf1UCGZJgwM6eyqH6XQ8Gf3eJindPaPhjo6QKTgCo9LDu8SlnXI2Z88s8ttka8UDp0UHGgWhhmPohwtnO3Vmk+lr+3z2J/v4ErHfLD6o0SDezEZRrUQbPT0I0T7dhIdeFYHpxHqzpekv2M73zQnv5CRf/gLTn7pyfFxMk0YAOn2ejLqHtcP2MkOHJ/wyuN3PYxKDwAObA5gnV8y7VOxcnQaKQCSfSHQScH5bzWORLR/H6mb3ic7ZZFw8C19ZzzIOOj4wbrvnUP0101Exw4HVWah/s+Ac0yT8gn5+KczAeBOVt3joa27H7stO52m8VlZDoDdILlqJF1tkmmktmRageqU4DRzAE/EA6nv48xvO2JZ4WBAXWngSVPzIAj2g4+ZprUu5OEf+UtvLwCy27r7sTth22oAyGdsuZ3u1aZ5kDSgU4LDfBMoeA+p3/9EdrYys2w20T//iC7S8wU0ZQ82J5vmtSYY+kd2jHavAHH75PHOBYBrHyLn49bTzS/TChDTKWH48xjyJ3priNSqD8lOVnaufUfs8Qm0aR02U0wTswtG/mk/AKTHqfWxyJbH4zbhHMC1w27LTqfxFQDSilP8ZZ/kytPW2PEUfAr58U2ueeAzQM8oX+ojdc1JsoN1AzeeQTTEi0LBVYBfs3yvaW52wdY/7QeANMllmr9JJtkl0/gJAMZNmwzU9OMp+BCcYtrY2NhN2O4G0atYrN0PyY7VLfCcYPMq05ggCFaaZmcX7PzTbgDoY3xWd48z6UEg2STT+AwAN310hpevEJlfDGpXcAj+lQZemZL15G9lx+omvj6HaES/nIZhUD82rc0FYOAfPwHQ6CrANA4COT3Xx4bvCyTTaPtWA2Crkz4a48uBdlbMPoV2xG9uIY/ond3Dh/S6+kNrSG1aToTJLz34LdmpugzatcU0koYQ8B8wXZBNMPKPdjL3i28tAPRxab0+JOtd16zkDQC3rfZd6WT9bdsm5BWc4GycDQ8iD4wL6nqoc8Pc5NtbnbypVSRb+KsLhkBHwKdNN2QT7PzjKwB0Gr7x5KYLiR5hiNJL6bKQNwCSzyxFx9x+2D1+LAN5BLvJcP6/YQspoh2/IrVkluw4E4VfXBm0Fc7P66KXmq7IJhj4x2cA6HRpV4J4EMhpspA3AKShmm5r2vAoA3nEZ0Cg7/AO7tXP9EhOM5HYsJBP/0GT0favmK7IJtj4x3cAMPpM6z57E7LCSicd5/o0I3Ta1gKAcdM3zqtx+wTyCA6AwT1UHyV1x6Wyw0w07r0uaDLaPgouNF2RTbDzj3Yo+4tn2gsARp9tpSCIHmlOHsNuJ5808gXAc45NeDVxH4NuvoxrkUdwAB5mBevj6oZ5ssNMMKj37qDJaPswONd0RTbBzj+dCgCmcRCED7O5+7HbySONfAHg2ugJenwfk+yDFPII4399Z+jlfoz9c/xeT7eBib11M+xFMNt0RTbBzj/tBoB2cl5CDIkvHcpzgtDW3Y/dlq1Ow+vz4dAnpNGwBbsdexdtb9twHsklUMk2hTwaD4BBBEDtZNlpJhJ3fDFoLgvOf7/phuyCnX+SDsG0EgCuE8Ynj/qdAPs4o29AJfdjt2Wr00jr843Kxm7H3iUZkPz4g1tGptcgbfIIAaAflTz4IqkVc2SnmSgsmUX07BNBc+H8x0BrS6As2Pqn0wEg2+o0yf3YnbD1HQByfvG/W1oBYvIITnAXbIMXSIIfo5UcZyJw9XSibWuDprLQ7m3YTDfdkF0w8s//XwDIV6T435leg7TJIzjCAqB/rvyFPRPzHsBVJ5K6dxnR6LGgmWgv/4zKB00XtCbY+8d/AAxksA0nntJ7v+7LNNIcQi+l5gkAxp2Y6312PvZSLQcg95FNYoUoj2A3HcMgfj6ePYPoD+vb+/3OsnHNDKKH19jOz78nuhQfTzBd0Jpg6B/9hdpfPtNOADCRE0t3XyMHlp7zsV9657O1FCR6op0/AKQ620Ttl/sncZXLKzjEZ4F+d5AvBr13k7r2VNmhugUOYp7w9u8ImsVi50ewrzXNzifk45/2A0Cy5xfZeT8j/eul0IGl4Q3DTs9OKr0QH11h8gdAs59isQO4owHA4rMi0L89znrzNf1T5j+7nNTaC7uHny8i9Qgu7pjUw+V1WyC07RBYYpqbX8jLP/IX3EoA8DJlo7u+EvxqED6M5+uOv5sRPaKcPwCkNkc0T+s1AGDP/8Lo8+B5fI7EV4T6aPfgCGd8fuDtd2A+/sw37LGFTPzTbgDoYzxOzxIE/MK6O8bnYU7WIIjK1LZ5A6DRlYeJO3cBARBqeHj4dDjLOvBfoH/duYuEOvMY/zD4D/g1+CTw98O5KMM/2nndVxaTz8En08QngvpKsM4cs52FA4P38f+pitK76HpIgcDDIJ4rSEHJQxm7TvGrSyN0XeN2EW6QSf2TWCXyKTjNacjzAmwvAyvBd0vOarAYfAH1/gS2p5qm+JXd4RXlolIBkjq+ohxUKkBSx1eUg0oFSOr4inJQqQBJHV9RDioVIKnjK8pBpU6rp+d/SWb8stueTMwAAAAASUVORK5CYII='
	indexComment = ''' <!-- @Author: Michael Hug (Michael.Hug@fiserv.com) MichaelIsMetal-->
<!--
  .d88"
  d88P'
  888
8888888 888  .d888b.   ,d888b.  88.d8b 88b    d88
  888   888 88K   888 d8K' `Y8b 888P*" '88.  ;88'
  888   888 888ho.    888   888 888     "8"  "8"
  888   888   "Y888b. 888888888 888     'Y8;;8P'
  888   888      'Y88 Y8b.      888      Y8bd8P  
  888   888 888  ,888 Y8b.  .d8 888      'Y88P'  888
  888   888  "Y888P"   "Y8888"  888       "88"   888
-->'''	
	return render_template('index.html', enterprise=enterprise, headerImg=headerImg, footerImg=footerImg, indexComment=indexComment)

@app.route('/api/traceroute/<host>', defaults={'maxttl': "30"}, methods = ["GET"])
@app.route('/api/traceroute/<host>/<maxttl>', methods = ["GET"])
def treaceroute(host, maxttl):
	p = Popen(["traceroute", "-m", maxttl, host], stdout=PIPE, stderr=PIPE)
	results = p.communicate()
	ret =  dumps({"stdout":results[0],"stderr":results[1]})
	print ret
	return Response(ret, status=200, mimetype='application/json')

@app.route('/api/telnet/<host>/<port>', defaults={'timeout': 7}, methods = ["GET"])
@app.route('/api/telnet/<host>/<port>/<timeout>', methods = ["GET"])
def telnet(host, port, timeout):
        ret = {}
        s = socket(AF_INET, SOCK_STREAM)
        s.settimeout(float(timeout))
        start = time()
        try:
                result = s.connect_ex((host, int(port)))
        except gaierror:
                ret['return'] = 1
                ret['status'] = 404
                ret['elapsed'] = -1
                return dumps(ret)
        elapsed = format(time()-start, '.4f')
        s.close()
        if result:
                ret['return'] = 1
                ret['status'] = 408
                ret['elapsed'] = elapsed
        else:
                ret['return'] = 0
                ret['status'] = 200
                ret['elapsed'] = elapsed
        print dumps(ret)
	return Response(dumps(ret), status=200, mimetype='application/json')

@app.route('/api/wget', defaults={'chars': 500}, methods = ["GET"])
@app.route('/api/wget/<chars>', methods = ["GET"])
def wget(chars):
	host = request.args.get('url')
	try:
		r = urllib2.urlopen(host, timeout = 3, context=ssl._create_unverified_context())
	except : 
		return dumps({"code":"Exception" ,"url":"Exception","body":"Exception","headers":["Exception"]})
	body = unicode(r.read(), errors='ignore')
	if chars > 0:
		body = body[:int(chars)] 
	url = r.geturl()
	code = r.code
	headers = r.info().headers
	r.close()
	ret = dumps({"code":code,"url":url,"body":body,"headers":headers})
	print ret
	return Response(ret, status=200, mimetype='application/json')

@app.route('/api/wget/vars', methods = ["GET"])
def wgetVars():
	http_proxy = getenv("http_proxy", "UNSET")
	https_proxy = getenv("https_proxy", "UNSET")
	no_proxy = getenv("no_proxy", "UNSET")
	ret = dumps({"http_proxy":http_proxy,"https_proxy":https_proxy,"no_proxy":no_proxy})
	print ret
	return Response(ret, status=200, mimetype='application/json')

@app.route('/api/setenv/http_proxy/<value>', methods = ["PUT"])
def setHttpProxy(value):
	environ["http_proxy"] = value
	ret = dumps({"status":"sucess"})
	print ret
	return Response(ret, status=200, mimetype='application/json')

@app.route('/api/setenv/https_proxy/<value>', methods = ["PUT"])
def setHttpsProxy(value):
	environ["https_proxy"] = value
	ret = dumps({"status":"sucess"})
	print ret
	return Response(ret, status=200, mimetype='application/json')

@app.route('/api/setenv/no_proxy/<value>', methods = ["PUT"])
def setNoProxy(value):
	environ["no_proxy"] = value
	ret = dumps({"status":"sucess"})
	print ret
	return Response(ret, status=200, mimetype='application/json')

@app.route('/api/unsetproxyvars', methods = ["PUT"])
def unsetProxySettings():
	if environ.get("no_proxy") is not None:
		del environ["no_proxy"]
	if environ.get("https_proxy") is not None:
		del environ["https_proxy"]
	if environ.get("http_proxy") is not None:
		del environ["http_proxy"]
	ret = dumps({"status":"sucess"})
	print ret
	return Response(ret, status=200, mimetype='application/json')

@app.route('/api/datetime', methods = ["GET"])
def datatimenow():
	ret = dumps(dict(datetimestring=str(datetime.now())))
	print ret
	return Response(ret, status=200, mimetype='application/json')

if __name__ == '__main__':
	serve(app, port=port)
