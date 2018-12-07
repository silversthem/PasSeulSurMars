function sendPostCode(action,token) {
    var http = new XMLHttpRequest();
    var url = 'update/' + token;
    var params = "";
    for(var k in Object.keys(action)) {
        params += k.toString() + '=' + action[k].toString();
    }
    params = params.slice(0, params.length-1);
    console.log(params);
    http.open('POST', url, true);
    http.send(params);
}

function sendGetCode(token, time) {
    var http = new XMLHttpRequest();
    var url = 'tick/' + token + '/1';
    // var params = "";
    // for(var k in Object.keys(action)) {
    //     params += k.toString() + '=' + action[k].toString();
    // }
    // params = params.slice(0, params.length-1);
    // console.log(params);
    http.open('GET', url, true);
    http.send();
}
