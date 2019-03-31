var cookie = new Cookie()
var datasent = undefined

function auth(formid) {
  let data = readForm(formid)
  datasent = data
  socket.send(JSON.stringify(data))
}

function register(formid) {
    let data = readForm(formid)
    datasent = data
    data['register'] = 1
    socket.send(JSON.stringify(data))
}

function registerInNewSession(formid) {
    let data = readForm(formid)
    datasent = data
    data['register'] = 1
    data['newSession'] = 1
    console.log(data)
    socket.send(JSON.stringify(data))
}

function checkAuth(data) {
  // Checks result
  if(data.auth == 1 || data.register == 1) {
    // Creates cookie
    cookie.set('login',datasent.login)
    cookie.set('password',datasent.password)
    // If created new session, getting session id from data as well
    if('session' in data) { // data returned session id
      datasent.session = data.session
    }
    cookie.set('session',datasent.session)
    // Redirect to game page
    window.location.replace('session/' + datasent.session)
  } else {
    console.log("Auth Failed")
  }
}
