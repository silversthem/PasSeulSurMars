// Merges b into a recursively
function merge_dicts(a,b) {
  Object.keys(b).forEach((k) => {
    if(k in a && typeof a[k] === "object" && typeof b[k] === "object") {
      a[k] = merge_dicts(a[k],b[k])
    } else {
      a[k] = b[k]
    }
  })
  return a
}

/*
  Represents server side data in the game
*/

function ServerData(pid) {
  /* Attributes */
  this.pid = pid
  /* Server Data */
  this.map = []
  this.players = []
  this.ressources = []
  this.objects = []
  this.player = {}

  // Loads initial data from server
  this.load = (data) => {
    this.update(data)
  }

  // Updates server from new json data
  this.update = (data) => {
    this.map = data.map
    this.update_players(data.players)
    this.ressources = merge_dicts(this.ressources,data.ressources)
    this.objects = merge_dicts(this.objects,data.objects)
    // Adding shortcut for current client player
    for(let i in this.players) {
      if(this.players[i]['id'] == this.pid) {
        this.player = this.players[i]
      }
    }
  }

  /* Data Fetching */

  // Returns ressources/objects/players in coords, if any
  this.inCoords = (coords) => {
    let res = {'length':0}
    // Searching in ressources
    this.ressources.forEach((rs) => {
      if(rs.x == coords.x && rs.y == coords.y) {
        res['ressource'] = rs
        res.length += 1
      }
    })
    // Searching in objects
    this.objects.forEach((obj) => {
      if(obj.x == coords.x && obj.y == coords.y) {
        res['object'] = obj
        res.length += 1
      }
    })
    // Searching in players
    this.players.forEach((pl) => {
      if(pl.x == coords.x && pl.y == coords.y) {
        res['player'] = pl
        res.length += 1
      }
    })
    return res
  }

  /* Update specific */

  // Updates player data to keep server/client coherence
  this.update_players = (pldata) => {
    if(pldata.length != this.players.length) { // De-synced, client absorbs server values
      this.players = pldata
      return
    }
    for(let i in pldata) { // Syncing client and server
      if(pldata[i]['id'] == this.players[i]['id']) {
        this.players[i]['data'] = merge_dicts(this.players[i]['data'],pldata[i]['data'])
      }
    }
  }
}
