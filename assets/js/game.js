function Game(map, player, ressource, token) {
    this.token = token;
    this.map = map;
    this.player = player;
    this.ressource = ressource;

    this.width = 25;
    this.height = 25;

    this.tileX = 32;
    this.tileY = 32;

    this.build = ""; //building type

    this.createEventListeners = function() {
        var that = this;
        addEventListener('keydown', function(event) {
            if(event.keyCode == 37) { //left key
                rep = sendPostCode({'move':'left'}, that.token);
                if (rep["can"] == 1) that.player['x'] -= 1;
            } else if(event.keyCode == 39) { //right key
                rep = sendPostCode({'move':'right'}, that.token);
                if (rep["can"] == 1) that.player['x'] += 1;
            } else if(event.keyCode == 40) { //down key
                rep = sendPostCode({'move':'down'}, that.token);
                if (rep["can"] == 1) that.player['y'] += 1;
            } else if (event.keyCode == 38) { //up key
                rep = sendPostCode({'move':'up'}, that.token);
                if (rep["can"] == 1) that.player['y'] -= 1;
            }
        });

        addEventListener('mousedown', function(event) {
            if (event.keyCode == 0) {
                coord = psoToCoord(event.clientX, event.clientY);
                rep = sendPostCode({'construct':that.build, 'x':coord[0], 'y':coord[1]}, that.token);
                that.map[coord[1]*25 + coord[0]] = rep;
            }
            // } else if (event.keyCode == 2) {
            //     x, y = posToCoord(event.clientX, event.clientY);
            //     rep = sendPostCode({'destruct':that.build, 'x':x, 'y':y});
            // }
        });
        that.draw();
    }

    this.posToCoord = function(userX, userY) {
        var coordX = 0, coordY = 0;

        var screenW = this.width * this.tileX;
        for (var x = 0; x < screenW; x += this.tileX) {
            if (userX > x) coordX = x / this.tileX;
        }

        var screenH = this.height * this.tileY;
        for (var y = 0; y < screenH; y -= this.tileY) {
            if (userY > y) coordY = y / this.tileY;
        }

        return [coordX, coordY];
    }

    this.tick = function() {
        rep = sendGetCode(this.token, 1);

        for(var i = 0; i< 25*25; i++) {
            if (typeof this.map[i] == "object") {
                for (var b in rep) {
                    if (this.map[i]["id"] == b["id"]) {
                        this.map[i] = b;
                        break;
                    }
                }
            }
        }

        draw();
    }

    this.getNearPipes = function(i) {
        var bType = this.map[i]["type"];
        var res = [];
        if (typeof that.map[i+1] == "object" && that.map[i+1]["type"] == bType) {
            res.push({"sign":"plus", "value":1});
        } else if (typeof that.map[i-1] == "object" && that.map[i-1]["type"] == bType) {
            res.push({"sign":"minus", "value":1});
        } else if (typeof that.map[i+25] == "object" && that.map[i+25]["type"] == bType) {
            res.push({"sign":"plus", "value":25});
        } else if (typeof that.map[i-25] == "object" && that.map[i-25]["type"] == bType) {
            res.push({"sign":"minus", "value":25});
        }
        return res;
    }

    this.draw = function() {
            var canvas = document.getElementById("game");
            canvas.width = this.width * this.tileX;
            canvas.height = this.height * this.tileY;

            var wait = true;
            var that = this;
            var i = 0;

            var imgGround = new Image();
            imgGround.src = "../textures/Mars.png";
            imgGround.onload = function() {
                for(var x = 0;x < 25;x++) {
                    for(var y = 0;y < 25;y++) {
                        var i = y*25 + x;
                        if (that.map[i] == 0) {
                            canvas.getContext("2d").drawImage(imgGround, x*32, y*32, 32, 32);
                        }
                    }
                }
            }
            var imgGround1 = new Image();
            imgGround1.src = "../textures/MineRocks.png";
            imgGround1.onload = function() {
                for(var x = 0;x < 25;x++) {
                    for(var y = 0;y < 25;y++) {
                        var i = y*25 + x;
                        if (that.map[i] == 1) {
                            canvas.getContext("2d").drawImage(imgGround1, x*32, y*32, 32, 32);
                        }
                    }
                }
            }
            var imgGround2 = new Image();
            imgGround2.src = "../textures/RedRubble.png";
            imgGround2.onload = function() {
                for(var x = 0;x < 25;x++) {
                    for(var y = 0;y < 25;y++) {
                        var i = y*25 + x;
                        if (that.map[i] == 2) {
                            canvas.getContext("2d").drawImage(imgGround2, x*32, y*32, 32, 32);
                        }
                    }
                }
            }

            var imgPipe = new Image();
            imgPipe.src = "../textures/copper.jpeg";
            imgPipe.onload = function() {
                for(var x = 0;x < 25;x++) {
                    for(var y = 0;y < 25;y++) {
                        var i = y*25 + x;
                        if (typeof(that.map[i]) == "object" && that.map[i]["type"] == 1) {
                            canvas.getContext("2d").drawImage(imgPipe, x*32, y*32, 32, 32);
                        }
                    }
                }
            }

            var imgCable = new Image();
            imgCable.src = "../textures/cable.jpg";
            imgCable.onload = function() {
                for(var x = 0;x < 25;x++) {
                    for(var y = 0;y < 25;y++) {
                        var i = y*25 + x;
                        if (typeof(that.map[i]) == "object" && that.map[i]["type"] == 2) {
                            canvas.getContext("2d").drawImage(imgCable, x*32, y*32, 32, 32);
                        }
                    }
                }
            }


            var imgShelter = new Image();
            imgShelter.src = "../textures/shelter.png";
            imgShelter.onload = function() {
                for(var x = 0;x < 25;x++) {
                    for(var y = 0;y < 25;y++) {
                        var i = y*25 + x;
                        if (typeof(that.map[i]) == "object" && (that.map[i]["type"] == 10 || that.map[i]["type"] == 11)) {
                            canvas.getContext("2d").drawImage(imgShelter, x*32, y*32, 32, 32);
                        }
                    }
                }
            }

            var imgGenerator = new Image();
            imgGenerator.src = "../textures/generateur.png";
            imgGenerator.onload = function() {
                for(var x = 0;x < 25;x++) {
                    for(var y = 0;y < 25;y++) {
                        var i = y*25 + x;
                        if (typeof(that.map[i]) == "object" && that.map[i]["type"] == 4) {
                            canvas.getContext("2d").drawImage(imgGenerator, x*32, y*32, 32, 32);
                        }
                    }
                }
            }

            var imgSolar = new Image();
            imgSolar.src = "../textures/solarpanel.jpg";
            imgSolar.onload = function() {
                for(var x = 0;x < 25;x++) {
                    for(var y = 0;y < 25;y++) {
                        var i = y*25 + x;
                        if (typeof(that.map[i]) == "object" && that.map[i] == 5) {
                            canvas.getContext("2d").drawImage(imgSolar, x*32, y*32, 32, 32);
                        }
                    }
                }
            }

            var imgTank = new Image();
            imgTank.src = "../textures/tank.png";
            imgTank.onload = function() {
                for(var x = 0;x < 25;x++) {
                    for(var y = 0;y < 25;y++) {
                        var i = y*25 + x;
                        if (typeof(that.map[i]) == "object" && that.map[i]["type"] == 6) {
                            canvas.getContext("2d").drawImage(imgTank, x*32, y*32, 32, 32);
                        }
                    }
                }
            }

            var imgSerre = new Image();
            imgSerre.src = "../textures/serre.png";
            imgSerre.onload = function() {
                for(var x = 0;x < 25;x++) {
                    for(var y = 0;y < 25;y++) {
                        var i = y*25 + x;
                        if (typeof(that.map[i]) == "object" && that.map[i] == 7) {
                            canvas.getContext("2d").drawImage(imgSerre, x*32, y*32, 32, 32);
                        }
                    }
                }
            }

            var imgRaffinerie = new Image();
            imgRaffinerie.src = "../textures/rafinerie.png";
            imgRaffinerie.onload = function() {
                for(var x = 0;x < 25;x++) {
                    for(var y = 0;y < 25;y++) {
                        var i = y*25 + x;
                        if (typeof(that.map[i]) == "object" && that.map[i] == 8) {
                            canvas.getContext("2d").drawImage(imgRaffinerie, x*32, y*32, 32, 32);
                        }
                    }
                }
            }

            var imgOxygene = new Image();
            imgOxygene.src = "../textures/spritegenerator.png";
            imgOxygene.onload = function() {
                for(var x = 0;x < 25;x++) {
                    for(var y = 0;y < 25;y++) {
                        var i = y*25 + x;
                        if (typeof(that.map[i]) == "object" && that.map[i] == 3) {
                            canvas.getContext("2d").drawImage(imgOxygene, x*32, y*32, 32, 32);
                        }
                    }
                }
            }

            var imgDrill = new Image();
            imgDrill.src = "../textures/spritegenerator.png";
            imgDrill.onload = function() {
                for(var x = 0;x < 25;x++) {
                    for(var y = 0;y < 25;y++) {
                        var i = y*25 + x;
                        if (typeof(that.map[i]) == "object" && that.map[i] == 9) {
                            canvas.getContext("2d").drawImage(imgOxygene, x*32, y*32, 32, 32);
                        }
                    }
                }
            }

            var imgPlayer = new Image();
            imgPlayer.src = "../textures/spritejoueur.png";
            imgPlayer.onload = function() {
                console.log(that);
                canvas.getContext("2d").drawImage(imgPlayer, that.player["x"]*32, that.player["y"]*32, 32,32);
            }


        }
    }
