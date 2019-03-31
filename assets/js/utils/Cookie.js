const expiredCookie = 'expires=Thu, 01 Jan 1970 00:00:00 UTC'

function Cookie() {
  this.defaultExpirationDate = undefined
  // Returns cookie data as a dict
  this.data = () => {
    let r = {}
    document.cookie.split(';').forEach((field) => {
      let kv = field.split('=')
      let k = kv[0].trim()
      let v = kv.slice(1).join('=')
      r[k] = v
    })
    return r
  }
  // Sets a cookie key/value pair
  this.set = (key,val,exp = undefined) => {
    document.cookie = key + '=' + val // @TODO : handle expiration parameter
  }
  // Returns a key value from a cookie
  this.get = (key) => {
    return this.data()[key]
  }
  // Returns key values as a dict
  this.getFields = (...keys) => {
    let d = this.data()
    let r = {}
    keys.forEach((k) => {
      r[k] = d[k]
    })
    return r
  }
  // Renews (sets later expiration date) cookie
  this.renew = (date,...fields) => {
    // @TODO
  }
  // Deletes a value from a cookie
  this.unset = (key) => {
    document.cookie = key + '= ;' + expiredCookie
  }
  // Deletes all values from a cookie
  this.delete = () => {
    // @TODO
  }
}
