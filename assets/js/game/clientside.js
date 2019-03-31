/*
  Client side update functions
*/

// Moves a player clientside
function movePlayer(player) {
  let data = player.data
  if(data.online && data.inMotion && player.data.clientTicks > 0) {
    let dx = data.toward.x - player.x
    let dy = data.toward.y - player.y
    dx = (dx > 0) ? 1 : (dx == 0) ? 0 : -1
    dy = (dy > 0) ? 1 : (dy == 0) ? 0 : -1
    player.x += dx
    player.y += dy
    player.data.clientTicks--;
  }
}
