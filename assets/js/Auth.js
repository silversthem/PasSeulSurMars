var formData = {}

function getAuthSocket(cookie,serveraddr,authPart,callback) {
  var sock = new WebSocket(serveraddr)
  this.successCallback = callback
  // Sending Auth
  sock.onopen = (event) => {
    let ss,lg,pw = cookie.getFields('session','login','password')
    // Auth from cookie
    if(ss != undefined && lg != undefined && pw != undefined) {
      sock.send(JSON.stringify({'login':lg,'password':pw,'session':ss}))
      // renew cookie
    } else { // Auth from authPart
      // Adding right actions to buttons
      document.getElementById('loginButton').onclick = () => { // login action
        formData = readForm('auth')
        sock.send(JSON.stringify(formData))
      }
      document.getElementById('registerButton').onclick = () => { // register action
        formData = readForm('register')
        formData['register'] = 1
        sock.send(JSON.stringify(formData))
      }
      document.getElementById('registerNewButton').onclick = () => { // register & create new session action
        formData = readForm('registerNew')
        formData['register'] = 1
        formData['newSession'] = 1
        sock.send(JSON.stringify(formData))
      }
    }
  }
  // Auth Reception
  sock.onmessage = (event) => {
    let rep = JSON.parse(event.data)
    if(('auth' in rep && rep['auth'] == 1) || ('register' in rep && rep['register'] == 1)) {
      let sessionid = ('session' in formData) ? formData['session'] :
                      ('session' in rep) ? rep['session'] : cookie.get('session'); // either from form, rep or cookie
      let pid = rep['pid'] // get pid from rep
      document.getElementById(authPart).style.display = 'none' // deleting authPart
      // @TODO renewing cookie
      this.successCallback(sessionid,pid) // calling callback -> game can start
    } else {
      // auth failed
      console.log('Failed to auth')
    }
  }
  return sock
}
