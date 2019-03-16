/*
  Main clientside class
*/

function Game(token, player) {
    /* Properties */
    this.tickrate = {'server':200,'client':40}
    this.tickrateRatio = this.tickrate.server/this.tickrate.client
    /* Attributes */
    this.game = new ServerData(player) // Game content
    this.session_id = token // Game session
    this.player_id  = player // Client player
    // Game Panel
    this.panels = new Panel()
    // Game canvas
    this.canvas = new GameCanvas('gameCanvas',
      () => {return this.game.player}, // Returns current player data
      () => {return this.game}) // Returns all other game data
    /* Loading game */
    getRequest('/load/' + token,(rep) => {
      this.game.update(rep)
      this.canvas.loadTextures()
      var texturesLoaded = setInterval(() => {
        if(this.canvas.texturesToLoad == 0) { // All textures are loaded
          clearInterval(texturesLoaded)
          // Server updates 5 times a second
          setInterval(() => {
            this.tick()
          },this.tickrate.server)
          // Client updates 20 times a second
          setInterval(() => {
            this.client_tick(this.game.player)
          },this.tickrate.client)
          // Starts Canvas
          this.canvas.run()
        }
      },50)
    })

    /* Game methods */

    /* Event listeners */
    // Default hover action
    this.canvas.hover = (coords) => {
      let toward = this.thisTile(coords)
      this.panels.setCurrentHoverCoords(toward)
    }
    // Default left click
    this.canvas.click[0] = (coords) => {
      let toward = this.thisTile(coords)
      let tileContent = this.game.inCoords(toward)
      if(tileContent.length == 0) { // Empty tile, move toward it
        this.move(toward)
      } else { // Focuses on tile
        this.panels.setFocusedActionPanel(tileContent)
      }
    }

    /* Tick method */

    // Updates game from server
    this.tick = () => {
      getRequest('/tick/' + this.session_id, (rep) => {
        if(rep['status'] == 1) { // Updates
          this.game.update(rep)
        }
      })
      this.game.player.data.clientTicks = this.tickrateRatio // Each server tick gives x new client ticks
    }

    // Updates game from client
    this.client_tick = () => {
      // Updates players in map clientside
      this.game.players.forEach((pl) => {
        movePlayer(pl)
      })
      // Sets current player coord
      this.panels.setCurrentCoords(this.game.player)
    }

    /* Game methods */

    /* Player methods */

    // Returns tile coords relative to player coords
    this.thisTile = (coords) => {
      return {
        'x':coords.x + this.game.player.x,
        'y':coords.y + this.game.player.y}
    }
    // Registers movement
    this.move = (coords) => {
      postRequest('/update/' + this.session_id, {'x':coords.x,'y':coords.y,'action':'move'}, (rep) => {
        if(rep.status == '1') { // Valid motion
          this.game.player.data.inMotion = true
          this.game.player.data.toward = coords
        }
      })
    }
}
