$('#traceroute-btn').click(function() {
    var traceroutehostname=$('#traceroutehostname').val();
    var url="/api/traceroute/" + traceroutehostname;
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
            console.log(error);
	    $('#response-body-traceroute').html('Error');
        },
	dataType: 'json'
    });
});
$('#telnet-btn').click(function() {
    var telnethostname=$('#telnethostname').val();
    var telnetport=$('#telnetport').val();
    var url="/api/telnet/" + telnethostname + "/" + telnetport;
    $('#response-body-telnet').html('Please wait ...');
    $.ajax({
        type: 'GET',
        url: url,
        success: function(telnetResult) {
		if(0 != telnetResult["return"]) {
			$('#response-body-telnet').html('<font color="#a94442">Failed</font>');
		} else {
			$('#response-body-telnet').html('<font color="#3c763d">Success</font>');
		}
	},
	error: function(xhr, status, error) {
            console.log(error);
	    $('#response-body-telnet').html("Error");
        },
	dataType: 'json'
    });
});
