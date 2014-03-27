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

 
function GameManager(size, InputManager, Actuator) {
  this.size         = size; // Size of the grid
  this.inputManager = new InputManager;
  this.actuator     = new Actuator;

  this.running      = true;
  
  this.setup();
  
  obj = this;
  var i = setInterval(function() {
    if (obj.running) {
      _direction = _videotape.substr(0, 1);
	  _videotape = _videotape.substr(1);
	  obj.move(parseInt(_direction));
	}
	if (this.win && this.over) 
    	clearInterval(i);
  }, 1000); 

  this.inputManager.on('run', function() {
    if (this.running) {
      this.running = false;
      this.actuator.setRunButton('继续');
    } else {
      this.running = true;
      //this.run()
      this.actuator.setRunButton('暂停');
    }
  }.bind(this));

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
  this.grid.addStartTiles();

  //this.ai           = new AI(this.grid);

  this.score        = 0;
  this.over         = false;
  this.won          = false;

  // Update the actuator
  this.actuate(0);
};


// Sends the updated grid to the actuator
GameManager.prototype.actuate = function (flag) {
  this.actuator.actuate(this.grid, {
    score: this.score,
    over:  this.over,
    won:   this.won
  });
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
