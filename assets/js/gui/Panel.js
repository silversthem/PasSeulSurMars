/*
  Game DOM class, mostly handles display
*/

function Panel() {

  /* DOM elements */

  this.coordsPanel = document.getElementById('coordsPanel')
  this.hoverCoordsPanel = document.getElementById('hoverCoordsPanel')
  this.focusedActionPanel = document.getElementById('focusedActionPanel')
  this.otherActionsListPanel = document.getElementById('otherActionsListPanel')

  /* Methods */

  // Updates current player coords display
  this.setCurrentCoords = (coords) => {
    this.coordsPanel.innerHTML = '(' + coords.x + ' ; ' + coords.y + ')'
  }

  // Updates current hovered position
  this.setCurrentHoverCoords = (coords) => {
    this.hoverCoordsPanel.innerHTML = '(' + coords.x + ' ; ' + coords.y + ')'
  }

  // Updates focused action panel
  this.setFocusedActionPanel = (content) => {

  }

  // Updates client player related panels
  this.updatePlayerPanels = (player) => {

  }

  // Updates current action list from client player
  this.updateActionListPanel = (player) => {

  }
}
