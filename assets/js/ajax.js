function postRequest(action,token,callback) {
    var http = new XMLHttpRequest();
    var url = '/update/' + token;
    var params = "";
    for(var k in Object.keys(action)) {
        params += '' + k + '=' + action[k];
    }
    params = params.slice(0, params.length-1);
    console.log(params);
    http.open('POST', url, true);
    http.send(params);
    http.onreadystatechange = function() {
      if(this.readyState == 4 && this.status == 200) {
        callback(eval('(' + http.responseText + ')'))
      }
    };
}

function getRequest(url, callback) {
    var http = new XMLHttpRequest();
    http.open('GET', url, true);
    http.send();
    http.onreadystatechange = function() {
      if(this.readyState == 4 && this.status == 200) {
        callback(eval('(' + http.responseText + ')'))
      }
    }
}
