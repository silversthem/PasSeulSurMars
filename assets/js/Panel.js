/*
  Game DOM class, mostly handles display
*/

function Panel() {
  this.coordsPanel = document.getElementById('coordsPanel')
  this.hoverCoordsPanel = document.getElementById('hoverCoordsPanel')
  this.focusedActionPanel = document.getElementById('focusedActionPanel')
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
}
