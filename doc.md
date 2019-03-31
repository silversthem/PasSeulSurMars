# Database

...

# Data

...

# Paquets

Paquets are sent/received in json format

## Auth Related

- Auth :
  * Clients sends :
      `{"login":...,"password":...,"session":...}`
  * Receives on success :
      `{"auth":1,"pid":...}`
  * Receives on failure :
      `{"auth":statusCode}`
- Register :
  * Clients sends :
    `{"login":...,"password":...,"session":...,"register":1}`
  * Receives on success :
    `{"register":1,"session":...,"pid":...}`
  * Receives on failure :
    `{"register":statusCode}`
- Registering & Creating a new session :
  * Clients sends :
    `{"login":...,"password":...,"register":1,"newSession":1}`
  * Receives on success :
    `{"register":1,"session":...,"pid":...}`
  * Receives on failure :
    `{"register":statusCode}`

## Game Related

- Loading the game from server
  * Clients sends :
    `{"load":1}`
  * Receives on success :
    `{"load":1, ...}`
    Client received a json object containing all data needed for the game to load up
  * Receives on failure :
    `{"status":statusCode}`
- Game Cycle Update ( ~ 5 times a second)
  * Client receives :
    `{tick:n, ...}`
    Client received all data the server deemed appropriate to keep them synced
- Client plays the game
  * Client sends :
    `{"action":...}`
  * Client receives :
    `{"action":...,"status":statusCode, ...}`
    (1 on success)

#### Client Commands (playing the game)
- Moving player
  * `{"action":"move","toward":{"x":...,"y":...}}`
- Building Object
  * `{"action":"build","coords":{"x":...,"y":...},"type":...}`
- Destroying Object
  * `{"action":"destroy","id":...}`


#### Server Updates (json fields)
These are the fields that can be found in a server response json object :
- Map : `"map"` a json array representing the 25x25 grid centered around the player
- Ressources : `"ressources"` a json array representing each ressources in the game as a json object
- Objects : `"objects"` same, but for objects
- Players : `"players"` same, but for players

##### Client specific values, and sync
Client only updates `"data"` field of the json objects, the rest is client handled for 'seemless' sync.

# Config

Game config files can be found in assets/config

...
