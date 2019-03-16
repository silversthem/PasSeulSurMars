function postRequest(url,action,callback) {
    var http = new XMLHttpRequest()
    var params = ""
    for(var k in action) {
        params += k + '=' + action[k] + '&'
    }
    params = params.slice(0, params.length-1)
    http.open('POST', url, true)
    http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded')
    http.send(params)
    http.onreadystatechange = function() {
      if(this.readyState == 4 && this.status == 200) {
        callback(eval('('+ JSON.parse(http.responseText) +')'))
      }
    }
}

function getRequest(url, callback) {
    var http = new XMLHttpRequest()
    http.open('GET', url, true)
    http.send()
    http.onreadystatechange = function() {
      if(this.readyState == 4 && this.status == 200) {
        callback(eval('(' + http.responseText + ')'))
      }
    }
}
