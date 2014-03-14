/** 
 * @fileOverview  
 * @author 
 * @date 
 * @e-mail 
 * @github 
 * @version 
 * @change log
 *     modified by HQM - change English to Chinese
 *                     - ajax post grid to server to save as videotape
 */

 
 function sleep(seconds) {
    this.date = Math.round(new Date().getTime()/1000);
    while(1) {
        if(Math.round(new Date().getTime()/1000) - this.date >= seconds) break;
    }
    return true;
}

 
function GameManager(size, InputManager, Actuator, grids) {
  this.size         = size; // Size of the grid
  //this.inputManager = new InputManager;
  this.actuator     = new Actuator;

  //this.running      = false;
  
  this.setup();
  
  glen = grids.length;
  
  num = 0;
  obj = this
  var i = setInterval(function() {
	obj.grid.toGrid(grids[num]);
	obj.actuate(-1);
	num++;
    if (num > glen)
        clearInterval(i);
  }, 2000);
  
  
  /* this.inputManager.on("move", this.move.bind(this));
  this.inputManager.on("restart", this.restart.bind(this));

  this.inputManager.on('think', function() {
    var best = this.ai.getBest();
    this.actuator.showHint(best.move);
  }.bind(this)); */


  /* this.inputManager.on('run', function() {
    if (this.running) {
      this.running = false;
      this.actuator.setRunButton('自动');
    } else {
      this.running = true;
      this.run()
      this.actuator.setRunButton('停止');
    }
  }.bind(this)); */

  //this.setup();
}

// Restart the game
GameManager.prototype.restart = function () {
  this.actuator.restart();
  this.setup();
};

// Set up the game
GameManager.prototype.setup = function () {
  this.grid         = new Grid(this.size);
  //this.grid.addStartTiles();

  //this.ai           = new AI(this.grid);

  this.score        = 0;
  this.over         = false;
  this.won          = false;

  // Update the actuator
  //this.actuate(0);
};


// Sends the updated grid to the actuator
GameManager.prototype.actuate = function (flag) {
  this.actuator.actuate(this.grid, {
    score: this.score,
    over:  this.over,
    won:   this.won
  });

  if (-1 == flag) {
    // do nothing
  } else {
	gridString = this.grid.toString();
	
	// ajax post grid to server to save as videotape
	$.ajax({
		type: "post",
		url: "/Lab/game-2048-videotape",
		data: {_grid: gridString, _flag: flag},
		dataType: "json",
		success: function(json){
			console.log('>>> '+json['msg']);
		}
	});  
  }
};

// makes a given move and updates state
GameManager.prototype.move = function(direction) {
  var result = this.grid.move(direction);
  this.score += result.score;

  if (!result.won) {
    if (result.moved) {
      this.grid.computerMove();
    }

  } else {
    this.won = true;
  }

  if (!this.grid.movesAvailable()) {
    this.over = true; // Game over!
  }

  this.actuate(1);
}

// moves continuously until game is over
GameManager.prototype.run = function() {
  var best = this.ai.getBest();
  this.move(best.move);
  var timeout = animationDelay;
  if (this.running && !this.over && !this.won) {
    var self = this;
    setTimeout(function(){
      self.run();
    }, timeout);
  }
}
