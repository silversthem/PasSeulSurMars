/*
  Main clientside class
*/

function Game(token, player) {
    /* Attributes */
    this.session_id = token // Game session
    this.player_id  = player // Client player
    /* Textures */
    this.textureBank = {
      'ground':'/textures/ground/ground.png',
      'player':'/textures/players/player.png',
      /* Ressources */
      'ice'  :'/textures/ressources/crystal-icy.png', // frozen water
      'metal':'/textures/ressources/crystal-red.png', // metal
      'om'   :'/textures/ressources/crystal-gold.png', // organic matter
      'nm'   :'/textures/ressources/crystal-green.png' // nuclear matter
    }
    this.texturesToLoad = Object.keys(this.textureBank).length
    /* Tileset attributes */
    this.width  = 25
    this.height = 25
    this.midX   = 12
    this.midY   = 12
    this.tileX  = 32
    this.tileY  = 32
    /* Game dom elements */
    this.canvas = document.getElementById('gameCanvas')
    this.panels = new Panel()
    /* Loading game */
    getRequest('/load/' + token,(rep) => {
      this.game = rep
      this.createEventListeners()
      this.loadTextures()
      var texturesLoaded = setInterval(() => {
        if(this.texturesToLoad == 0) { // All textures are loaded
          clearInterval(texturesLoaded)
          // Starting to draw
          this.canvas.width  = this.width *this.tileX
          this.canvas.height = this.height*this.tileY
          this.draw() // drawing
          // Ticking
          setInterval(() => {
            this.tick()
            let player = this.this_player()
            this.panels.setCurrentCoords(player['x'],player['y'])
          },200)
        }
      },100)
    })

    /* Game methods */

    /* Event listeners */
    this.createEventListeners = () => {
      // Canvas hover
      this.canvas.addEventListener('mousemove',(ms) => {
        var coords = this.getMouseTile(ms)
        this.panels.setCurrentHoverCoords(coords.x,coords.y)
        // ...
      })
      // Canvas Clicks
      this.canvas.addEventListener('click',(ms) => {
        let coords = this.getMouseTile(ms)
        let tileContent = this.readTile(coords.x,coords.y)
        if(tileContent['spots'] == 0) { // Empty tile, move toward it
          this.move(coords.x,coords.y)
        } else { // Focuses on tile
          this.panels.setFocusedActionPanel(tileContent)
        }
      })
    }
    /* Loading textures */
    this.loadTextures = () => {
      for(let key in this.textureBank) {
        let imgsrc = this.textureBank[key]
        this.textureBank[key] = new Image();
        this.textureBank[key].src = imgsrc;
        this.textureBank[key].onload = () => {
          this.texturesToLoad--;
        }
      }
    }
    /* Canvas methods */
    this.draw = () => {
      var context = this.canvas.getContext('2d')
      // drawing base map
      for(let i = 0;i < this.width;i++) {
        for(let j = 0;j < this.height;j++) {
          let p = i*this.width + j
          switch (this.game.map[p]) {
            default:
              context.drawImage(this.textureBank['ground'],i*this.tileX,j*this.tileY,this.tileX,this.tileY)
          }
        }
      }
      // drawing found ressources
      for(let i in this.game.ressources) {
        let rs = this.game.ressources[i]
        if(this.isInBound(rs.x,rs.y)) {
          let c = this.coords2repr(rs.x,rs.y)
          switch (rs.type) {
            case 0: // Water
              context.drawImage(this.textureBank['ice'],0,0,64,128,c[0],c[1],this.tileX,this.tileY)
            break;
          }
        }
      }
      // drawing objects

      // drawing player
      context.drawImage(this.textureBank['player'],0,0,62,67,this.midX*this.tileX,this.midY*this.tileY,this.tileX,this.tileY)
    }
    this.isInBound = (x,y) => {
      if(this.this_player().x - this.midX <= x && this.this_player().x + this.midX >= x) {
        return (this.this_player().y - this.midY <= y && this.this_player().y + this.midY >= y);
      }
      return false;
    }
    /* Tick method */
    this.tick = () => {
      getRequest('/tick/' + this.session_id, (rep) => {
        if(rep['status'] == 1) { // Update
          // @TODO : update
        }
      })
    }
    /* Player methods */
    // Gets this player from the list of players
    this.this_player = () => {
      for(var k in this.game.players) {
        if(this.game.players[k]['id'] == this.player_id) {
          return this.game.players[k]
        }
      }
    }
    // Registers movement
    this.move = (x,y) => {
      postRequest('/update/' + this.session_id, {'x':x,'y':y,'action':'move'}, (rep) => {

      })
    }
    /* Tileset methods */
    // Returns where to draw on canvas from coords
    this.coords2repr = (x,y) => {
      let c = [0,0]
      c[0] = (x - this.this_player().x + this.midX)*this.tileX
      c[1] = (y - this.this_player().y + this.midY)*this.tileY
      return c
    }
    // Returns which tile the mouse is on
    this.getMouseTile = (ms) => {
      var x = parseInt(ms.offsetX/this.tileX)
      var y = parseInt(ms.offsetY/this.tileY)
      var tx = x - this.midX
      var ty = y - this.midY
      return {'x':tx,'y':ty}
    }
    // Reads tile content from coords
    this.readTile = (x,y) => {
      var content = {'spots':0,'ressource':undefined,'object':undefined}
      // Checks ressources
      for(let i in this.game.ressources) {
        if(this.game.ressources[i]['x'] == x && this.game.ressources[i]['y'] == y) {
          content['ressource'] = this.game.ressources[i]
          content['spots'] += 1
        }
      }
      // Checks objects
      for(let i in this.game.objects) {
        if(this.game.objects[i]['x'] == x && this.game.objects[i]['y'] == y) {
          content['object'] = this.game.objects[i]
          content['spots'] += 1
        }
      }
      return content
    }
}
