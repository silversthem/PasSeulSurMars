/*
  Main clientside class
*/

function Game(token, player) {
    /* Attributes */
    this.session_id = token; // Game session
    this.player_id  = player; // Client player
    /* Textures */
    this.textureBank = {'ground':'/textures/ground.png','player':'/textures/player.png'}
    this.texturesToLoad = 2
    /* Tileset attributes */
    this.width  = 25;
    this.height = 25;
    this.tileX  = 32;
    this.tileY  = 32;
    /* Game dom elements */
    this.canvas = document.getElementById('gameCanvas')
    /* Loading game */
    getRequest('/load/' + token,(rep) => {
      this.game = rep
      this.createEventListeners()
      this.loadTextures()
      var texturesLoaded = setInterval(() => {
        if(this.texturesToLoad == 0) { // All textures are loaded
          clearInterval(texturesLoaded)
          // Starting to draw
          this.canvas.width = this.width*this.tileX
          this.canvas.height = this.height*this.tileY
          this.draw() // drawing
        }
      },100)
    })
    /* Event listeners */
    this.createEventListeners = () => {
        // Keyboard
        addEventListener('keydown', (event) => {
            if(event.keyCode == 37) { //left key

            } else if(event.keyCode == 39) { //right key

            } else if(event.keyCode == 40) { //down key

            } else if (event.keyCode == 38) { //up key

            }
        });
        // Canvas Clicks
        this.canvas.addEventListener('click',(ms) => {

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
      // drawing objects

      // drawing player
    }
    /* Tick method */
    this.tick = () => {

    }
}
