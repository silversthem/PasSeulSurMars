/*
  Game Canvas object representation
*/

function GameCanvas(id,playerDataModelCallback,gameDataModelCallback) {
  this.getPlayer = playerDataModelCallback
  this.getData   = gameDataModelCallback
  /* Textures */
  this.textureBank = {
    /* Tiles */
    'ground':'/textures/ground/ground.png',
    /* Player */
    'player':'/textures/players/player.png',
    /* Ressources */
    'ice'  :'/textures/ressources/crystal-icy.png', // frozen water
    'metal':'/textures/ressources/crystal-red.png', // metal
    'om'   :'/textures/ressources/crystal-gold.png', // organic matter
    'nm'   :'/textures/ressources/crystal-green.png' // nuclear matter
  }
  this.texturesToLoad = Object.keys(this.textureBank).length
  /* Tileset attributes */
  this.mid    = {'x':12,'y':12}
  this.tile   = {'x':32,'y':32,'w':25,'h':25}
  /* Game dom elements */
  this.canvas = document.getElementById(id)
  this.canvas.width  = this.tile.w * this.tile.x
  this.canvas.height = this.tile.h * this.tile.y
  /* Event callbacks */
  this.click = {0:(tile) => {},1:(tile) => {}}
  this.hover = (tile) => {}
  /* Event listeners */
  this.canvas.addEventListener('mousemove',(ms) => {
    let coords = this.getMouseTile(ms)
    this.hover(coords)
  })
  this.canvas.addEventListener('click',(ms) => {
    let coords = this.getMouseTile(ms)
    this.click[0](coords)
  })

  /* Methods */

  // Loads textures
  this.loadTextures = () => {
    for(let key in this.textureBank) {
      let imgsrc = this.textureBank[key]
      this.textureBank[key] = new Image()
      this.textureBank[key].src = imgsrc
      this.textureBank[key].onload = () => {
        this.texturesToLoad--
      }
    }
  }

  /* Canvas methods */

  // Main drawing cycle
  this.run = () => {
    setInterval(() => {
      let pldata = this.getPlayer()
      let dData  = this.getData()
      if(pldata !== undefined && dData !== undefined) {
        this.draw(pldata,dData)
      }
    },40) // 25 Frames a second
  }

  // Draws game on canvas
  this.draw = (player,game) => {
    var context = this.canvas.getContext('2d')
    // drawing base map
    for(let i = 0;i < this.tile.w;i++) {
      for(let j = 0;j < this.tile.h;j++) {
        let p = i*this.tile.w + j
        switch (game.map[p]) {
          default:
            context.drawImage(this.textureBank['ground'],i*this.tile.x,j*this.tile.y,this.tile.x,this.tile.y)
        }
      }
    }
    // drawing found ressources
    for(let i in game.ressources) {
      let rs = game.ressources[i]
      if(this.isInBound(player,rs.x,rs.y)) {
        let c = this.coords2repr(player,rs.x,rs.y)
        switch (rs.type) {
          case 0: // Water
            context.drawImage(this.textureBank['ice'],0,0,64,128,c.x,c.y,this.tile.x,this.tile.y)
          break;
          case 1: // Metal
            context.drawImage(this.textureBank['metal'],0,0,64,128,c.x,c.y,this.tile.x,this.tile.y)
          break;
          case 2: // Organic matter
            context.drawImage(this.textureBank['om'],0,0,64,128,c.x,c.y,this.tile.x,this.tile.y)
          break;
          case 3: // Nuclear matter
            context.drawImage(this.textureBank['nm'],0,0,64,128,c.x,c.y,this.tile.x,this.tile.y)
          break;
        }
      }
    }
    // drawing objects

    // drawing player
    context.drawImage(this.textureBank['player'],0,0,62,67,this.mid.x*this.tile.x,this.mid.y*this.tile.y,this.tile.x,this.tile.y)
  }

  /* Tileset methods */

  // Returns if object/ressource is in canvas bounds
  this.isInBound = (center,x,y) => {
    if(center.x - this.mid.x <= x && center.x + this.mid.x >= x) {
      return (center.y - this.mid.y <= y && center.y + this.mid.y >= y);
    }
    return false;
  }
  // Returns where to draw on canvas from coords
  this.coords2repr = (center,x,y) => {
    return {
      'x':(x - center.x + this.mid.x)*this.tile.x,
      'y':(y - center.y + this.mid.y)*this.tile.y
    }
  }
  // Returns which tile the mouse is on
  this.getMouseTile = (ms) => {
    var x = parseInt(ms.offsetX/this.tile.x)
    var y = parseInt(ms.offsetY/this.tile.y)
    var tx = x - this.mid.x
    var ty = y - this.mid.y
    return {'x':tx,'y':ty}
  }
}
