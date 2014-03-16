animationDelay = 150;
minSearchTime = 100;
videotape = "";

// Wait till the browser is ready to render the game (avoids glitches)
window.requestAnimationFrame(function () {
  var manager = new GameManager(4, KeyboardInputManager, HTMLActuator);
});
