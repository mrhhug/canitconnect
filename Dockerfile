#author : Michael Hug

#builds a docker image that can run the unit_tests
FROM ubuntu

RUN  \
	echo 'Acquire::http::Proxy "http://sddc-test-outboundproxy.onefiserv.net:8080";' > /etc/apt/apt.conf && \
    echo 'Acquire::https::Proxy "http://sddc-test-outboundproxy.onefiserv.net:8080";' >> /etc/apt/apt.conf && \
	apt-get update && \
	apt-get -y upgrade && \
	apt-get -y install traceroute git python3 python3-pip && \
	pip3 install flask waitress
