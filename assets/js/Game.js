/*
  Main clientside class
*/

function Game(token, player) {
    /* Attributes */
    this.game = {} // Game content
    this.session_id = token // Game session
    this.player_id  = player // Client player
    // Game Panel
    this.panels = new Panel()
    // Game canvas
    this.canvas = new GameCanvas('gameCanvas',
      () => {return this.thisPlayer()}, // Returns current player data
      () => {return this.game}) // Returns all other game data
    /* Loading game */
    getRequest('/load/' + token,(rep) => {
      this.game = rep
      this.canvas.loadTextures()
      var texturesLoaded = setInterval(() => {
        if(this.canvas.texturesToLoad == 0) { // All textures are loaded
          clearInterval(texturesLoaded)
          // Ticking
          setInterval(() => {
            this.tick()
            let player = this.thisPlayer()
            this.panels.setCurrentCoords(player)
          },200)
        }
      },100)
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
      let tileContent = this.readTile(toward)
      if(tileContent['spots'] == 0) { // Empty tile, move toward it
        this.move(toward)
      } else { // Focuses on tile
        this.panels.setFocusedActionPanel(tileContent)
      }
    }

    /* Tick method */

    // Updates game
    this.tick = () => {
      getRequest('/tick/' + this.session_id, (rep) => {
        if(rep['status'] == 1) { // Update
          // Update players
          this.game.players = rep.players
          // Update map
          this.game.map = rep.map
          // Update ressources

          // Update objects

        }
      })
    }

    /* Game methods */

    // Returns tile content, if any
    this.readTile = (tile) => {
      // ...
      return {'spots':0}
    }

    /* Player methods */

    // Gets this player from the list of players
    this.thisPlayer = () => {
      for(var k in this.game.players) {
        if(this.game.players[k]['id'] == this.player_id) {
          return this.game.players[k]
        }
      }
    }
    // Returns tile coords relative to player coords
    this.thisTile = (coords) => {
      return {
        'x':coords.x + this.thisPlayer().x,
        'y':coords.y + this.thisPlayer().y}
    }
    // Registers movement
    this.move = (coords) => {
      postRequest('/update/' + this.session_id, {'x':coords.x,'y':coords.y,'action':'move'}, (rep) => {

      })
    }
}
