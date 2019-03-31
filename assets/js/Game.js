var cookie = new Cookie()

function Game(serveraddr,authGUI,gameGUI) {
  // game gui is hidden by default until user is authentified (id : GAME)
  this.gameGUI = document.getElementById(gameGUI)
  this.gameGUI.style.display = 'none'
  // auth gui is active by default (id : AUTH)
  /* Auth user */
  this.socket = getAuthSocket(cookie,"ws://" + serveraddr,'AUTH',(sessionid,pid) => {
    this.gameData.sid = sessionid // sets session id
    this.gameData.pid = pid // sets player id
    // Socket response handling method
    this.socket.onmessage = (event) => {
      let data = JSON.parse(event.data)
      this.handleResponse(data)
    }
    this.socket.send('{"load":1}') // asks server for initial game data
  })

  /* Attributes */

  // Client panels handler
  this.gamePanel = new Panel()
  // Client canvas handler
  this.gameCanvas = new GameCanvas('gameCanvas',() => this.gameData.player,() => this.gameData)
  // Server data handler
  this.gameData = new ServerData()

  // Called when game is successfully loaded
  this.gameData.onloaded = () => {
    this.gameGUI.style.display = 'inline' // Display game gui
    this.gameCanvas.callOnTextureLoaded(() => {
      setInterval(() => { // client update interval 25 times a second
        this.client_tick()
      },40)
      // @TODO : set canvas click & hover function
      this.gameCanvas.run() // Starts canvas
    })
  }

  /* Game Methods */

  /* Mouse Actions */

  // default left click action (move player)
  // default hover action (get tile info)
  // build left click
  // destroy left click

  /* Methods */

  // Called every tick to update data clientside
  // Client ticks are more frequents and kept in sync by server ticks
  this.client_tick = () => {

  }

  // handles server response
  this.handleResponse = (data) => {
    this.gameData.update(data)
  }
}
