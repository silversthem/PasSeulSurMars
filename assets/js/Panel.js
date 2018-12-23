/*
  Game DOM class, mostly handles display
*/

function Panel() {
  this.coordsPanel = document.getElementById('coordsPanel')
  this.hoverCoordsPanel = document.getElementById('hoverCoordsPanel')
  this.focusedActionPanel = document.getElementById('focusedActionPanel')
  // Updates current player coords display
  this.setCurrentCoords = (x,y) => {
    this.coordsPanel.innerHTML = '(' + x + ' ; ' + y + ')'
  }
  // Updates current hovered position
  this.setCurrentHoverCoords = (x,y) => {
    this.hoverCoordsPanel.innerHTML = '(' + x + ' ; ' + y + ')'
  }
  // Updates focused action panel
  this.setFocusedActionPanel = (content) => {

  }
}
