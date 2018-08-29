function mostCommonMistakeFixer(par) {
	var ret = par.replace("https://", "");
	ret = ret.replace("http://", "");
	return ret.replace("/", "");
}

$('#traceroute-btn').click(function() {
    var traceroutehostname=mostCommonMistakeFixer($('#traceroutehostname').val());
    var url= "api/traceroute/" + traceroutehostname;
    $('#response-body-traceroute').html('Please wait ...');
    $.ajax({
        type: 'GET',
        url: url,
        success: function(tracerouteResult) {
		$('#response-body-traceroute').html('The output is as follows: <br>');
		$('#response-body-traceroute').append('<br>');
		$('#response-body-traceroute').append('<div>');
		$('#response-body-traceroute').append(tracerouteResult.stdout.replace(/(?:\r\n|\r|\n)/g, '<br />'));
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
    var telnethostname=mostCommonMistakeFixer($('#telnethostname').val());
    var telnetport=$('#telnetport').val();
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
$('#wget-btn').click(function() {
    var wgethost=$('#wgethostname').val().trim();
    ////so there is some type of jquery bug that if wgethost contains https and it has a trailing slash, jquery will call http://canitconnect... instead of https://canitconnect.... for some crazy reason. 
    // additionally, i spent waaaaay to much time tracking this one down!
    if (wgethost.slice(-1) === "/") {
    	wgethost = wgethost.substring(0, wgethost.length - 1);
    } 
    var url= "api/wget?url=" + wgethost;
    $('#response-body-wget').html('Please wait ...');
    $.ajax({
        type: 'GET',
        url: url,
        success: function(wgetResult) {
		var ret = "<table>"
                ret += "<tr><td>Response Code</td><td>"+wgetResult["code"]+"</td></tr>";
                ret += "<tr><td>url</td><td>"+wgetResult["url"]+"</td></tr>";
                ret += "<tr><td>Response Headers</td><td>"
		//python api is sending this out as a list
		console.log("adding whitespace after every n characters so the table does not run off the screen");
		wgetResult["headers"].forEach(function(i) {
			ret += i.replace(/(.{100})/g,"$1 ") + "</br>"
		});
		ret += "</td></tr>";
                ret += "<tr><td>Body</td><td>"+wgetResult["body"].replace(/</g,"&lt;").replace(/>/g,"&gt;")+"</td></tr>";
                ret += "</table>"
		$('#response-body-wget').html(ret);
	},
	error: function(xhr, status, error) {
            console.log(status);
            console.log(error);
	    $('#response-body-wget').html("Error");
        },
	dataType: 'json'
    });
});
$('#wgetVars-btn').click(function() {
    var url= "api/wget/vars";
    $('#response-body-wget').html('Please wait ...');
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
		$('#response-body-wget').html(ret);
	},
	error: function(xhr, status, error) {
            console.log(status);
            console.log(error);
	    $('#response-body-wget').html("Error");
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
var localhost = window.location.hostname
var restResponse = 'curl "https://' + localhost + '/api/traceroute/' + localhost + '"<br>'
restResponse += 'curl "https://' + localhost + '/api/traceroute/' + localhost + '/31"<br>'
restResponse += 'curl "https://' + localhost + '/api/telnet/' + localhost + '/443"<br>'
restResponse += 'curl "https://' + localhost + '/api/telnet/' + localhost + '/443/8"<br>'
restResponse += 'curl "https://' + localhost + '/api/wget?url=https://' + localhost + '"<br>'
restResponse += 'curl "https://' + localhost + '/api/wget/501/?url=https://' + localhost + '"<br>'
restResponse += 'curl "https://' + localhost + '/api/wget/vars<br>'
restResponse += 'curl "https://' + localhost + '/api/datetime"<br>'
$('#response-body-rest').html(restResponse);
