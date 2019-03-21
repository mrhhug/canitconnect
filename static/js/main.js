$('#traceroute-btn').click(function() {
	var traceroutehostname = $('#traceroutehostname').val()
	if(traceroutehostname.includes("/") || traceroutehostname.includes("\\")) {
		$('#response-body-traceroute').html('Tracroute does not understand network paths or protocals, please remove any forward or back slashes');
		return;
	}
	var url= "api/traceroute/" + traceroutehostname;
	$('#response-body-traceroute').html('Please wait ...');
	$.ajax({
		type: 'GET',
		url: url,
		success: function(tracerouteResult) {
		$('#response-body-traceroute').html('The output is as follows: <br>');
		$('#response-body-traceroute').append('<br>');
		$('#response-body-traceroute').append('<div>');
		if(tracerouteResult.exitcode == 0) {
			$('#response-body-traceroute').append(tracerouteResult.stdout.replace(/(?:\r\n|\r|\n)/g, '<br />'));
		} else {
			$('#response-body-traceroute').append(tracerouteResult.stderr);
		}
		$('#response-body-traceroute').append('</div>');
	},
	error: function(xhr, status, error) {
			console.log(status);
			console.log(error);
		$('#response-body-traceroute').html('Error');
		},
	dataType: 'json'
	});
});
$('#telnet-btn').click(function() {
	var telnethostname = $('#telnethostname').val()
	if(telnethostname.includes("/") || telnethostname.includes("\\")) {
		$('#response-body-telnet').html('Telnet does not understand network paths or protocals, please remove any forward or back slashes');
		return;
	}
	var telnetport=$('#telnetport').val();
	telnetport = parseInt(telnetport)
	if( ! Number.isInteger(telnetport)) {
		$('#response-body-telnet').html('Port must be an integer');
		return;
	}
	var url= "api/telnet/" + telnethostname + "/" + telnetport;
	$('#response-body-telnet').html('Please wait ...');
	$.ajax({
		type: 'GET',
		url: url,
		success: function(telnetResult) {
		dothtml = ''
		if(0 != telnetResult["return"]) {
			dothtml += '<font color="#a94442" style="text-align: center;">Failed</font><br/>'
		} else {
			dothtml += '<font color="#3c763d" style="text-align: center;">Success</font><br>'
		}
		dothtml += 'HTTP status Code: ' + telnetResult["status"]
		dothtml += '<br/>Time elapsed: ' + telnetResult["elapsed"] + 'seconds'
		$('#response-body-telnet').html(dothtml);
	},
	error: function(xhr, status, error) {
			console.log(status);
			console.log(error);
		$('#response-body-telnet').html("Error");
		},
	dataType: 'json'
	});
});

$('#curl-btn').click(function() {
	var method = $("input[name='curlradio']:checked").val();
	var curlhost=$('#curlhostname').val().trim();
	////there is some type of jquery bug that if host contains https and it has a trailing slash, jquery will call http://canitconnect... instead of https://canitconnect.... for some crazy reason. 
	// additionally, i spent waaaaay to much time tracking this one down!
	if (curlhost.slice(-1) === "/") {
		curlhost = curlhost.substring(0, curlhost.length - 1);
	}
	var myPOSTData = '{"url":"'+curlhost+'", "method":"'+method+'"';
	if (method == 'POST' ) {
		myPOSTData += ', "data":"'+$('#curl-postdata-input').val()+'"'
	}
	myPOSTData += '}';
	var url= "api/curl";
	$('#response-body-curl').html('Please wait ...');
	$.ajax({
		type: 'POST',
		url: url,
		contentType: 'application/json',
		data: myPOSTData,
		success: function(curlResult) {
		var ret = "<table>"
		if("url" in curlResult) {
					ret += "<tr><td>URL</td><td>"+curlResult["url"]+"</td></tr>";
		}
		if("method" in curlResult) {
					ret += "<tr><td>Verb</td><td>"+curlResult["method"]+"</td></tr>";
		}
		if("reason" in curlResult) {
					ret += "<tr><td>Reason</td><td>"+curlResult["reason"]+"</td></tr>";
		}
		if("code" in curlResult) {
					ret += "<tr><td>Code</td><td>"+curlResult["code"]+"</td></tr>";
		}
		if("headers" in curlResult) {
					ret += "<tr><td>Headers</td><td>"
			console.log("adding whitespace after every n characters so the table does not run off the screen");
			for(var i=0; i < curlResult["headers"].length; i++ ) {
				ret += curlResult["headers"][i][0]
				ret += " : "
				ret += curlResult["headers"][i][1].replace(/(.{100})/g,"$1 ")
				ret += "</br>"
			}
		}
		ret += "</td></tr>";
		if("body" in curlResult && curlResult["body"] != "") {
					ret += "<tr><td>Body</td><td>"+curlResult["body"].replace(/</g,"&lt;").replace(/>/g,"&gt;")+"</td></tr>";
		}
				ret += "</table>"
		$('#response-body-curl').html(ret);
	},
	error: function(xhr, status, error) {
			console.log(status);
			console.log(error);
		$('#response-body-curl').html("Error");
		},
	dataType: 'json'
	});
});
$('#sethttp-btn').click(function() {
	var envalue=$('#envalue').val().trim();
	var url= "api/setenv/http_proxy";
	$('#response-body-envs').html('Please wait ...');
	var myPOSTData = '{"data":"'+envalue+'"}';
	if ( envalue == "" ) {
		$('#response-body-envs').html('Please enter a value.');
	} else {
		$.ajax({
			type: 'POST',
			url: url,
			contentType: 'application/json',
			data: myPOSTData,
			success: function(sethttpResult) {
				$('#response-body-envs').html("ok");
			},
			error: function(xhr, status, error) {
				console.log(status);
				console.log(error);
				$('#response-body-envs').html("Error");
			},
			dataType: 'json'
		});
	}
});
$('#sethttps-btn').click(function() {
	var envalue=$('#envalue').val().trim();
	var url= "api/setenv/https_proxy";
	$('#response-body-envs').html('Please wait ...');
	var myPOSTData = '{"data":"'+envalue+'"}';
	if ( envalue == "" ) {
		$('#response-body-envs').html('Please enter a value.');
	} else {
		$.ajax({
			type: 'POST',
			url: url,
			contentType: 'application/json',
			data: myPOSTData,
			success: function(sethttpResult) {
				$('#response-body-envs').html("ok");
			},
			error: function(xhr, status, error) {
				console.log(status);
				console.log(error);
				$('#response-body-envs').html("Error");
			},
			dataType: 'json'
		});
	}
});
$('#setnoproxy-btn').click(function() {
	var envalue=$('#envalue').val().trim();
	var url= "api/setenv/no_proxy";
	$('#response-body-envs').html('Please wait ...');
	var myPOSTData = '{"data":"'+envalue+'"}';
	if ( envalue == "" ) {
		$('#response-body-envs').html('Please enter a value.');
	} else {
		$.ajax({
			type: 'POST',
			url: url,
			contentType: 'application/json',
			data: myPOSTData,
			success: function(sethttpResult) {
				$('#response-body-envs').html("ok");
			},
			error: function(xhr, status, error) {
				console.log(status);
				console.log(error);
				$('#response-body-envs').html("Error");
			},
			dataType: 'json'
		});
	}
});
$('#unset-btn').click(function() {
	var url= "api/unsetproxyvars";
	$.ajax({
	type: 'PUT',
	url: url,
	success: function(sethttpResult) {
		$('#response-body-envs').html("ok");
	},
	error: function(xhr, status, error) {
		console.log(status);
		console.log(error);
		$('#response-body-envs').html("Error");
	},
	dataType: 'json'
	});
});
$('#getenv-btn').click(function() {
	var url= "api/getenv";
	$('#response-body-getenv').html('Please wait ...');
	$.ajax({
		type: 'GET',
		url: url,
		success: function(wgetVarsResult) {
		var ret = "<table><tr><th>Key</th><th>Value</th></tr>"
				ret += "<tr><td>http_proxy</td><td>"+wgetVarsResult["http_proxy"]+"</td></tr>";
				ret += "<tr><td>https_proxy</td><td>"+wgetVarsResult["https_proxy"]+"</td></tr>";
		console.log("adding whitespace after every comma so the table does not run off the screen");
		my_no_proxy = wgetVarsResult["no_proxy"].trim().replace(/,/g,", ")
				ret += "<tr><td>no_proxy</td><td>"+my_no_proxy+"</td></tr>";
				ret += "</table>"
		$('#response-body-getenv').html(ret);
	},
	error: function(xhr, status, error) {
			console.log(status);
			console.log(error);
		$('#response-body-getenv').html("Error");
		},
	dataType: 'json'
	});
});
$('#datetime-btn').click(function() {
	var url= "api/datetime"
	$('#response-body-datetime').html('Please wait ...');
	$.ajax({
		type: 'GET',
		url: url,
		success: function(datetimeResult) {
		$('#response-body-datetime').html(datetimeResult['datetimestring']);
	},
	error: function(xhr, status, error) {
			console.log(status);
			console.log(error);
		$('#response-body-datetime').html("Error");
		},
	dataType: 'json'
	});
});

//does that POST textarea hider /shower
var cacheDom = $('#curl-postdata-input');
cacheDom.remove();
function handleCurlRadioClick(myRadio) {
	if (myRadio.value != 'POST') {
		cacheDom.remove();
	} else {
		$('#curl-post-data-textarea').append(cacheDom);
	}
}

var localhost = window.location.hostname
var restResponse = "" ;
restResponse += '<h3>cURL</h3><hr>';
restResponse += 'curl -H "Content-Type: application/json" -d &#39;{"url":"https://www.fiserv.com", "method":"GET"}&#39; "https://' + localhost + '/api/curl"<br>'
restResponse += 'curl -H "Content-Type: application/json" -d &#39;{"url":"https://www.fiserv.com", "method":"GET"}&#39; "https://' + localhost + '/api/curl/&lt;max chars in body&gt;"<br>'
restResponse += '<h3>Traceroute</h3><hr>';
restResponse += 'curl -X GET "https://' + localhost + '/api/traceroute/&lt;host&gt;"<br>'
restResponse += 'curl -X GET "https://' + localhost + '/api/traceroute/&lt;host&gt;/&lt;max hops&gt;"<br>'
restResponse += '<h3>Telnet</h3><hr>';
restResponse += 'curl -X GET "https://' + localhost + '/api/telnet/&lt;host&gt;/&lt;port&gt;"<br>'
restResponse += 'curl -X GET "https://' + localhost + '/api/telnet/&lt;host&gt;/&lt;port&gt;/&lt;timeout&gt;"<br>'
restResponse += '<h3>Get Environmental Vars</h3><hr>';
restResponse += 'curl -X GET "https://' + localhost + '/api/getenv"<br>'
restResponse += '<h3>Set Environmental Vars</h3><hr>';
restResponse += 'curl -H "Content-Type: application/json" -d &#39;{"data":"https://proxyServer:proxyPort"}&#39; "https://' + localhost + '/api/setenv/http_proxy"<br>'
restResponse += 'curl -H "Content-Type: application/json" -d &#39;{"data":"https://proxyServer:proxyPort"}&#39; "https://' + localhost + '/api/setenv/https_proxy"<br>'
restResponse += 'curl -H "Content-Type: application/json" -d &#39;{"data":"https://proxyServer:proxyPort"}&#39; "https://' + localhost + '/api/setenv/no_proxy"<br>'
restResponse += '<h3>Unset Environmental Vars</h3><hr>';
restResponse += 'curl -X PUT "https://' + localhost + '/api/unsetproxyvars"<br>'
restResponse += '<h3>Datetime</h3><hr>';
restResponse += 'curl -X GET "https://' + localhost + '/api/datetime"<br>'
$('#response-body-rest').html(restResponse);
var gitServer;
if (localhost.includes('fiserv')) {
	gitServer = "https://git-enterprise-jc.onefiserv.net/PCF/PlatformTestingApps/canitconnect" ;
} else {
	gitServer = "https://github.com/mrhhug-Fiserv/canitconnect";
}
$('#response-body-git').html(gitServer);
