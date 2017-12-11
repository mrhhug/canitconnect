from flask import Flask, render_template
from os import getenv
from subprocess import Popen, PIPE
from socket import socket, AF_INET, SOCK_STREAM 
from errno import errorcode
from json import dumps

app = Flask(__name__)

port = int(getenv("PORT",8081))

@app.route('/')
def root():
	enterprise = 'MyEnterprise'
	headerImg = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEYAAABGCAYAAABxLuKEAAAACXBIWXMAAA7EAAAOxAGVKw4bAAANYElEQVR4nO2cfWwc1XbAf7PfjndtE0hTmRjHCcTm2aoISuVCKvScRCJ/IBGkCDnopSkoSEigQNoE0b9Q/gioRBECRWoBVYRETVVEICgqUKV1jB4EB0iakBY1INsB/JGHQxJ77fXuzs6c/rF7p7PjmZ1Ze0M/Hke62vt5zrnnno97Z3auxs8HSWADsB64C1gONJXapoBLwFngBPAvQCYg3hDwh8BGYC3wK2BZiV4BuAoMAeeAfwU+AbJ+SLUS4qBgzqP/cmA38BugIRqN0t7ezu23387ixYsJh8Ncu3aNwcFBvv76a3K5HKXJ/C2wH7hegfZG4GmKAg81NTXR2dlJS0sLyWQSXdf58ccfuXjxIsPDw4gIwBXgIPAycDnoRLwmHbK1Bc0vAl4EcuFwWDZt2iRHjx6Va9euiWmaYpqmOGFqakqOHj0qGzduFE3TBJgAeh18hYAu4LeALFmyRHbv3i2ff/656Lpehk/RME1TRkdH5Y033pC1a9cKIEAa+Asg4jL/kH1CtUy/Av4DkIcffli+/fZbSxhB02effSZ33XWXmsTLpQmEgCeA2WQyKS+++KJMT0+XCSBI+uSTT6S7u1vh/mdgscsc5la4rJCbZnil+4BrN998s7z//vtVC8SeMpmMbNu2TU3gb0oaKN3d3TI4OLgg3Lquy969eyUcDgvwb8AtfoJZSPoTIL1y5UpLSxYKhmHI9u3blXBk8+bNkslkPPvbaQbJv/POOxKLxQT4FEg4lKAmsAz4XUtLi1y6dMlzpewq75V3plwuJ/fee69s2rRJ8vm8a99K4/3ov/XWW8qnvWyfkJvzVOXbgHspev0/BVbw37ZuHxMCTsTjcTl9+vT81aMCDA0NSTqdrgkupyabpimPPfaYAAZwNzZTUtAA/DlwHLhGSX0dKV1q7wVipfG9gOzZsyeQ+lbDtFdbEHzV8HLlyhVpbGwU4J+AkFYSSBPwl8BTQNPixYvp6elhzZo1tLW10dDQQD6fZ2RkhDNnzvDhhx9y+fJlKG6cdgN7W1paOr755hvi8TgAmqapfYMnaFqRvLOfV70Tb9B+QeufffZZ9u3bZwLtUNx4/Q6Q9evXy7FjxySbzVZciVwuJ0eOHJEVK1ZYmvTqq6/6ruD/dvjqq6/UfHYBSFdXl/T19VWNaHp6WrZt2yZ1dXVy9erVG8DqjQGvDaZhGLJ06VIBjvPMM8/I7OzsHM/thsDNwxuGIe+9917gKGHH5ZX3i15ubX71lQRj52/dunUCfEst9hr/n6C3t1cAI6Qc2O8TiMP52sudnZ309PSEtJKgyjy809t7le2IvcZXwuXXLygvC8HlFJICTbxafs8h8otc3MHyMZqmlZmI01xUuz3Z+znHutV79XPD6cVLkDFB8k7cc2iYpnlDVKbaned8cC0Ub0V8N0ow/9chUinCVIKgkci5kn5jKtGwjw8C1UZIe59AGlMxrNVYhd3wg/tB8Uby8YspecC8TckLgpjIz4U7iLl7QUR1dENqBzdVdXs24jY2CC43fG5+wZ73wuvFixc+N55+MSUPmGNK84EgUanWdBbKI1SOcBH7IGdYDXLwc1Nrtwl4mY4ffa8w7gb2MX5bBCeeX0wpIITczh7VJnA/k1Sqq2UCeP3119myZQsffPBBbXCKBHu06NbPa4yzT5AXbl5tbjScbSdOnLAeysdiMfnhhx8C8+vVL2T3EU4/Yc+79XOOGRkZ4dixY/z000+eIdWLhlebG1/OtitXrljt+XyeycnJQPxWmhdSIxgeHlYvrKS1tVWmpqZqhdoXZmdnZfPmzXLLLbfI7t27XR+CV3pl6waupuRE5tVmzx8+fLjsjeWnn37qaS5+uNyg0kT8zNI0TTEMQwzDkEKhIIVCwSp74V1wVFJhbmxsjNWrVzMxMUF7eztnz56lrq5uIahrAqXFxzRNKwGEQiEr2Z24gpo+852YmOD8+fN0d3eTSqVqhXZeYBdIoVBA13V0XbcEEw6HiUajRCIRIpHIHAHNEYy4bIKqfW4S5ODmhctvskF4Ub+maaLrOtlslmw2Sy6Xo1AooGkakUiERCJBIpEgHo8TiUQIh8MWTteH4ZXqFEOqXOmQ5ze2GmUNsvt20jQMg1wuRyaTYXp6mtnZWQqFAgCxWMzSIE3TLLNSEPisNMcGbWU/HJXGVgNeNN2OHyJCoVCYIxhd19E0jWg0immahEIhotEo0WjU0hhN08r+sThv8DMfp3Y5+wXBW2mMk6ZKhmGg6zq5XI5cLkc2m7U0xjRNwuEw8XgcXdcxDKNM80J2RJWSIuok7qxzy9sn4NXPD6+IsHPnTk6ePOnaz4uWaZoYhoFhGGWRyV52wxP4rORccSdxJ3I/XOPj43M0wI+Hw4cPMzIyUtV5LRQKEQ6HCYfDZSG6UrjWNK26fyc61dQeBnVdp1AoWCrpFJQdBgcHWbZsGRcuXKiKdjabZdGiRVbZC9REVUiOx+Nzkj0i2f2LglAQdbTXq31BPp8nm80yMzNjpWw2a9mr2i84BQqwcuVK1qxZw2uvvTan3SuNjY2RyWRobW2taH52f6Z8yKJFi0gmk6RSqbLf+vp66urqiMViZYIRkblRyc/bG4ZBPp+3nFk+ny/aZChELBazViMWi3maoKZp7Nq1i61bt7Jjxw46Ojo8V19BX18fqVSKrq4u34ioTDQSiRCLxaxyLBaz9jFKkxSvvhs8L7ALJZPJWFqSy+XKPHx9ff2clXCbgGmarF+/nnQ6TX9/P8lk0pO2aZr09PTQ1tbGwYMHg7DravLK1JU2RSIRa/frKhi7+jlDn51QoVBgdnaWdDrN1NQU09PTZLNZaz+QSCRIpVI0NDSQSqVIJBJEIhHPsPz9999zzz33sGrVKt5++22WLFlitSleRITnn3+e/fv3c/78ee644w6LHzc+7WNVmz0aqXo352uff0QhsiN15u3Rx+5fZmdnyzQGIBqNkkgkKBQKFiNuhzSA1tZW+vr6ePDBB+ns7GTHjh088MADrFixgkwmw8DAAK+88gqnTp3i4MGDllAq8exWpyKSM2p6/c7MzFQflez7AuVk7WV7fRAr7ejo4MyZMzz99NO8+eab3H333TQ1NdHc3Exvby/JZJJTp07xyCOPVMOqBXZt8NISJZTLly+zb98+Vq1aFczHKIHk83lmZmaYnJzk+vXrpNNpS2PsptTU1ERjYyP19fVEo1GLET8wTZPx8XHGx8eJxWK0tbXdsFP6xYsXGRgYIJ1OMzQ0xOnTp/niiy/QdR3g88D/qFISVw4rHo+Tz+cBMAzDcr6xWGyOQ4NgB0ZN02hubqa5udmqq4a/oH0B+vv7eeKJJ1QxD3xD8ZPDfwC+rOrdtTpwKR8iIkSjUUswiUSC+vp6y+l6PQS6URCUjogwNTWliqspCqXsG8zAjx0AS2PUk7lIJEI+n7dMKRaLUVdXRyKRIBqNVqUtPzd89913UNSUr0u/ZVDV6VoJBrA2SUpzVNl+hLc/35gvBDWRak3pyy+/hKKmFEpVilkTCFX92EEJR5mVPSQ7D2e1gKCTrUYoExMTSjD9FAWB7Rfw+X+MfeNnLyvfEQ6HK+4NVN6tTyVfFoSXIOAcr/KHDh3CMAyAf8TjM7+ynW8lqLQrrgbmYxpe+SD4nO0zMzO0t7czNjZ2FvhjlyFFU6pWVRfqSOdjGl75IPic7Xv27GFsbAzgr3CYjw1MxAHqBdTo6KicOHEi8Cd7blBp7HzwLpSX48ePSygUEuAt/L4IVoLIZDJy7tw5OXDggNx///0SjUYlmUzO+SJWEfFLQfv59bdPbCGpv79f6uvrBbhA8dvPyoJZvny5LF26VKLRqP0V6yjwBjCzbt060XV9wYz5pUwm4/pBWC3SoUOHpK6uToBBil8GB4L3KW6D9wPbgT+ySW47IE8++aQYhhFIxd3UPYgJPPfcc6Jpmjz11FMyOTnpSycIL6Ojo7Jlyxa12GeAZl9NCXCFgUovA7Jz584y4bipuVveXudlJh999JG6SuA7QG699VY5cODAnH9MBDW5oaEh2bVrlySTSaH4LfUrFC/hwDZHPObs7OMJIYr3KshDDz0kV69eramaDwwMqL+PDAN/QPFuiM8AaWxslK1bt8qRI0dkeHhYCoWCK47p6WkZGBiQl156Se677z4lZKH4DfWaIJP0mniQ9Bxg3HbbbXL8+HFf8wmi8u+++66kUinl0zoc9H4N/D0wWZqkpFIp6ejokO7ublm7dq2sXr1ali1bZheE8iN/7YKv2uSrNnb1+jXFlZUNGzbIyZMnXVXZz9zGxsbk0UcfVfcpnKd4NYIX3QRFLdoF/B3Fa01OA18AHwNHgX3AnwG3O/i1L7wz7zb3eZ1j1KBFwB5KK9nV1SUvvPCCnDt3rmL0yuVy8vHHH8vjjz+uIoRO0X95PwX/HwSN+V8J0gQ8BjxK8SIdbrrpJu68805aW1tpaipePzU5OcmlS5e4cOEC6XQaikf8d4C9wH9WSTPIVVA16WMXjOpsutS5IVTb6RBFe94AdAOrKIbFhlL7dWAE+HeK1yd9QPEOKjs9hceNhhs9v37V4HLF+1+Ed+AoA/yhRQAAAABJRU5ErkJggg=='
	footerImg = headerImg
	indexComment = ''' <!-- @Author: Michael Hug (Michael.Hug@fiserv.com) -->
<!--
   _____         ___________       __                            .__               
  /     \ ___.__.\_   _____/ _____/  |_  ________________________|__| ______ ____  
 /  \ /  <   |  | |    __)_ /    \   __\/ __ \_  __ \____ \_  __ \  |/  ___// __ \ 
/    Y    \___  | |        \   |  \  | \  ___/|  | \/  |_> >  | \/  |\___ \\  ___/ 
\____|__  / ____|/_______  /___|  /__|  \___  >__|  |   __/|__|  |__/____  >\___  >
        \/\/             \/     \/          \/      |__|                 \/     \/ 
-->'''
	return render_template('index.html', enterprise=enterprise, headerImg=headerImg, footerImg=footerImg, indexComment=indexComment)

@app.route('/api/traceroute/<host>')
def treaceroute(host):
	#p = Popen(["/usr/sbin/traceroute", host], stdout=PIPE, stderr=PIPE)
	p = Popen(["traceroute", host], stdout=PIPE, stderr=PIPE)
	results = p.communicate()
	return dumps({"stdout":results[0],"stderr":results[1]})

@app.route('/api/telnet/<host>/<port>')
def telnet(host, port):
	s = socket(AF_INET, SOCK_STREAM)
	result = s.connect_ex((host, int(port)))
	s.close()
	ret = {}
	if result:
		ret['return'] = 1
	else:
		ret['return'] = 0
	return dumps(ret)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port)
