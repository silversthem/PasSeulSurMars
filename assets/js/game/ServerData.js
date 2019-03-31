function ServerData() {
  /* Attributes */

  this.sid = undefined
  this.pid = undefined
  // server data
  this.map = []
  this.players = []
  this.ressources = []
  this.objects = []
  this.player = {}

  /* Methods */

  // callback to when server sent load data
  this.onloaded = () => {}
  // updates game data
  this.update = (data) => {
      if('load' in data && data['load'] == 1) { // loading game data
        console.log('> game loaded !')
        this.load(data) // fills game data
        this.onloaded()
      } else { // update game
        if('tick' in data) { // updates game data from tick
          this.tick(data)
        }
      }
  }

  // Loads from server data
  this.load = (data) => {
    this.map = data.map
    this.players = data.players
    this.ressources = data.ressources
    this.objects = data.objects
    this.initPlayer()
  }

  // updates from tick data
  this.tick = (data) => {

  }

  //
  this.initPlayer = () => {
    for(let i = 0;i < this.players.length;i++) {
      if(this.players[i].id == this.pid) {
        this.player = this.players[i]
      }
    }
  }

  //
  this.updatePlayer = () => {
    for(let i = 0;i < this.players.length;i++) {
      if(this.players[i].id == this.pid) {
        this.updatePlayerData(this.players[i])
      }
    }
  }

  //
  this.updatePlayerData = (pldata) => {

  }
}
