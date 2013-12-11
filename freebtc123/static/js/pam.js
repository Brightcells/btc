/** 
 * @fileOverview pam.js which to simply deal with picture\audio\movie 
 * @author HQM
 * @date 2013/06/27
 * @e-mail qiminis0801@gmail.com
 * @github https://github.com/HQMIS
 * @version 0.0.1 
 */

/**
 * Global Variable
 */
var imgIndex = 0; // the index of the picList

/**
 * now the list is directly written in pam.js the final goal is get the list
 * from server
 */
var url = "http://121.199.46.162/work/pam/";
/* picture list on server */
var picList = [ url + "picture/tyr.jpg", url + "picture/xm.jpg",
		url + "picture/jyf.jpg", url + "picture/ly.jpg" ];

/**
 * ########## ########## ########## ########## ########## ########## ##########
 * ########## ########## ########## ########## ########## ########## ##########
 * 
 * the global function used for all feature
 * 
 * ########## ########## ########## ########## ########## ########## ##########
 * ########## ########## ########## ########## ########## ########## ##########
 */

/**
 * @description check the browser you are using
 * 
 * @param
 * 
 * @return {Object} Sys
 */
function browserCheck() {
	/* check what browser you are using */
	var Sys = {};
	var ua = navigator.userAgent.toLowerCase();
	var s;

	(s = ua.match(/msie ([\d.]+)/)) ? Sys.ie = s[1] : (s = ua
			.match(/firefox\/([\d.]+)/)) ? Sys.firefox = s[1] : (s = ua
			.match(/chrome\/([\d.]+)/)) ? Sys.chrome = s[1] : (s = ua
			.match(/opera.([\d.]+)/)) ? Sys.opera = s[1] : (s = ua
			.match(/version\/([\d.]+).*safari/)) ? Sys.safari = s[1] : 0;

	return Sys;
}

/**
 * ########## ########## ########## ########## ########## ########## ##########
 * ########## ########## ########## ########## ########## ########## ##########
 * 
 * the three function below is for picture
 * 
 * ########## ########## ########## ########## ########## ########## ##########
 * ########## ########## ########## ########## ########## ########## ##########
 */

/**
 * @description control to set background use picture
 * 
 * @param {int}
 *            _bg_mode 0 - diy resource(Array) 1 - use server's resource(String)
 * @param {Array
 *            or Int} _bg_res Array - path of diy resource Int - show background
 *            _bg_mode, 0 for just one image, 1 for slide image
 * @param {int}
 *            _bg_time the interval time of the timer, unit is millisecond(毫秒)
 * @return {null} null
 */
function _bg(_bg_mode, _bg_res, _bg_time) {
	/**
	 * when _bg_mode equals 1, we should use server's picture else when _bg_mode
	 * equals 0, we should use diy picture
	 */
	if (1 == _bg_mode) {
		if (1 == _bg_res) { // order to set picture on server in the list as
			// background
			/* set a timer, to set background every interval time */
			var timeId = window.setInterval("slideSetBackground(picList)",
					_bg_time);
			slideSetBackground(picList);
		} else { // set one picture as background
			var slideIndex = parseInt(Math.random() * picList.length);
			setBackground(picList.slice(slideIndex, slideIndex + 1));
		}
	} else {
		picList = _bg_res;
		
		if (1 == picList.length) {
			/*
			 * the length of the array is 1, direct set the picture index which
			 * index is 0 as background
			 */
			setBackground(picList[0]);
		} else {
			/* set a timer, to set background every interval time */
			var timeId = window.setInterval("slideSetBackground(picList)",
					_bg_time);
			slideSetBackground(picList);
		}
	}
}

/**
 * @description slide to set background use picture
 * 
 * @param {Array}
 *            _bg_res the picture list to be set as background
 * @return {null} null
 */
function slideSetBackground(_bg_res) {
	// alert(imgIndex);
	var bgImg = _bg_res[imgIndex++];
	// alert(imgIndex);
	/* judge the index of the picture to be set as background */
	if (imgIndex >= _bg_res.length) {
		imgIndex = 0;
	}
	setBackground(bgImg);
}

/**
 * @description set background use picture
 * 
 * @param {String}
 *            _bg_res the picture to be set as background
 * @return {null} null
 */
function setBackground(_bg_res) {
	/* Judge whether the img tag whose id is _bgImg exists or not */
	var _bgImg = document.getElementById("_bgImg");
	if (_bgImg) {
		_bgImg.src = _bg_res;
	} else {
		/* create div && set id\className && append to body */
		var _bgDiv = document.createElement("div");
		_bgDiv.id = "bgDiv";
		_bgDiv.className = "bgDiv";
		var object = document.body.appendChild(_bgDiv);

		/* create img && set src && append to div above */
		var _bgImg = document.createElement("img");
		_bgImg.id = "_bgImg";
		_bgImg.src = _bg_res;
		var object = _bgDiv.appendChild(_bgImg);
	}
}

/**
 * ########## ########## ########## ########## ########## ########## ##########
 * ########## ########## ########## ########## ########## ########## ##########
 * 
 * the three function below is for audio
 * 
 * ########## ########## ########## ########## ########## ########## ##########
 * ########## ########## ########## ########## ########## ########## ##########
 */

/**
 * @description control to broadcast audio
 * 
 * @param {int}
 *            _audio_mode 0 - diy resource(Array) 1 - use server's
 *            resource(String)
 * @param {Array
 *            or Int} _audio_res Array - path of diy resource Int - broadcast
 *            _audio_mode, 0 for single replay, 1 for more replay
 * @return {null} null
 */
function _audio(_audio_mode, _audio_res) {
	var Sys = browserCheck();

	/**
	 * when _audio_mode equals 1, we should use server's audio else when
	 * _audio_mode equals 0, we should use diy audio
	 */
	if (1 == _audio_mode) {
		/* audio list on server */
		var audioList = [ url + "audio/snq", url + "audio/qg", url + "audio/xy" ];

		if (Sys.ie && parseInt(Sys.ie.split(".")[0]) < 9) {
			_audio_IE(audioList);
		} else {
			if (1 == _audio_res) { // order play the audio on server
				broadcastList(audioList);
			} else { // order play the audio on server
				var slideIndex = parseInt(Math.random() * audioList.length);
				broadcastList(audioList.slice(slideIndex, slideIndex + 1));
			}
		}
	} else {
		/**
		 * if statement deal with the browser which not support html5's audio
		 * tag else statement deal with the browser that support html5's audio
		 * tag
		 */
		if (Sys.ie && parseInt(Sys.ie.split(".")[0]) < 9) {
			_audio_IE(_audio_res);
		} else {
			broadcastList(_audio_res);
		}
	}
}

/**
 * @description broadcast audio by list
 * 
 * @param {String}
 *            _audio_res the audio list to be broadcast
 * @return {null} null
 */
function broadcastList(_audio_res) {
	/* audioIndex is the index of resource array */
	var audioIndex = 0;
	/* create audio */
	var _audio = document.createElement("audio");

	/**
	 * judge the audio and deal with if auido is null or not can play, show the
	 * notice else deal with the request
	 */
	if (_audio != null && _audio.canPlayType) {
		/* append audio to body */
		var object = document.body.appendChild(_audio);

		/* broadcat _audio_res[i] through audio */
		broadcast(_audio, _audio_res[audioIndex++]);

		/* add the callback function addEventListener to audio's object */
		_audio.addEventListener('ended', function() {
			/* judge the index of the audio to be broadcast */
			if (audioIndex >= _audio_res.length) {
				audioIndex = 0;
			}

			/* broadcat _audio_res[i] through audio */
			broadcast(_audio, _audio_res[audioIndex++]);
		}, false);
	} else {
		var _notice = document.createElement("div");
		_notice.innerText = "您现在使用的浏览器不支持audio标签";
		var object = document.body.appendChild(_notice);
	}
}

/**
 * @description broadcast audio
 * 
 * @param {object}
 *            _audio the object create by document.createElement("audio")
 * @param {String}
 *            _audio_res the audio to be broadcast
 * @return {null} null
 */
function broadcast(_audio, _audio_res) {
	/* set id\controls\preload\autoplay\className */
	_audio.id = "_audio";
	_audio.controls = "controls";
	_audio.preload = "auto";
	_audio.autoplay = "autoplay";
	_audio.className = "audio";

	/*
	 * judge the browser you are using whether support audio which is ogg format
	 * or not && select the suitable format's audio to be broadcast
	 */
	if (_audio.canPlayType("audio/ogg")) {
		_audio.src = _audio_res + ".ogg";
	} else if (_audio.canPlayType("audio/mpeg")) {
		_audio.src = _audio_res + ".mp3";
	}
}

/**
 * @description broadcast audio for ie version below 9
 * 
 * @param {Array}
 *            _audio_res Array - path of _audio_res to be broadcast
 * @return {null} null
 */
function _audio_IE(_audio_res) {
	/* create div && append to body */
	var _notice = document.createElement("div");
	var object = document.body.appendChild(_notice);

	/*
	 * create a && set id\href\onclick\innerText\className && append to div
	 * above
	 */
	var _switch = document.createElement("a");
	_notice.appendChild(_switch);
	_switch.id = "_switch";
	_switch.href = "javascript:void(0);";
	_switch.onclick = function(stop) {
		var _bgsound = document.getElementById("_bgsound");
		/* judge the text of the _switch and deal with */
		if ("关闭背景音乐" == document.getElementById("_switch").innerHTML) {
			_bgsound.src = "";
			_switch.innerText = "打开背景音乐";
		} else {
			_bgsound.src = _audio_res[0] + ".mp3";
			_switch.innerText = "关闭背景音乐";
		}
	};
	_switch.innerText = "关闭背景音乐";
	_switch.className = "switch";

	/* create bgsound && set id\src\loop && append to body */
	var _bgsound = document.createElement("bgsound");
	_bgsound.id = "_bgsound";
	_bgsound.src = _audio_res[0] + ".mp3";
	_bgsound.loop = -1;
	var object = document.body.appendChild(_bgsound);
}

/**
 * ########## ########## ########## ########## ########## ########## ##########
 * ########## ########## ########## ########## ########## ########## ##########
 * 
 * the three function below is for movie(video)
 * 
 * ########## ########## ########## ########## ########## ########## ##########
 * ########## ########## ########## ########## ########## ########## ##########
 */

/**
 * @description control to set movie(video) as background whichi just is
 *              broadcast movie without controls
 * 
 * @param {int}
 *            _movie_mode 0 - diy resource(Array) 1 - use server's
 *            resource(String)
 * @param {Array
 *            or Int} _movie_res Array - path of diy resource Int - broadcast
 *            _movie_mode, 0 for single replay, 1 for more replay
 * @return {null} null
 */
function _movie(_movie_mode, _movie_res) {
	var Sys = browserCheck();

	/**
	 * when _movie_mode equals 1, we should use server's audio else when
	 * _movie_mode equals 0, we should use diy audio
	 */
	if (1 == _movie_mode) {
		/* video list on server */
		var videoList = [ url + "movie/movie", url + "movie/xwqzzhxcp" ];

		if (Sys.ie && parseInt(Sys.ie.split(".")[0]) < 9) {
			_movie_IE(_movie_res);
		} else {
			if (1 == _movie_res) { // order play the movie(video) on server
				broadcastSetList(videoList);
			} else { // order play the audio on server
				var slideIndex = parseInt(Math.random() * videoList.length);
				broadcastSetList(videoList.slice(slideIndex, slideIndex + 1));
			}
		}
	} else {
		/**
		 * if statement deal with the browser which not support html5's video
		 * tag else statement deal with the browser that support html5's video
		 * tag
		 */
		if (Sys.ie && parseInt(Sys.ie.split(".")[0]) < 9) {
			_movie_IE(_movie_res);
		} else {
			broadcastSetList(_movie_res);
		}
	}
}

/**
 * @description set movie(video) as background whichi just is broadcast movie
 *              without controls by list
 * 
 * @param {String}
 *            _movie_res the video list to be broadcast
 * @return {null} null
 */
function broadcastSetList(_movie_res) {
	/* videoIndex is the index of resource array */
	var videoIndex = 0;
	/* create video */
	var _video = document.createElement("video");

	/**
	 * judge the vedio and deal with if vedio is null or not can play, show the
	 * notice else deal with the request
	 */
	if (_video != null && _video.canPlayType) {
		/* append _movieDiv to body */
		var _movieDiv = document.createElement("div");
		_movieDiv.className = "movieDiv";
		var object = document.body.appendChild(_movieDiv);

		/* append video to body */
		var object = _movieDiv.appendChild(_video);

		/* broadcat _movie_res[i] through video */
		broadcastSet(_video, _movie_res[videoIndex++]);

		/* add the callback function addEventListener to video's object */
		_video.addEventListener('ended', function() {
			/* judge the index of the video to be broadcast */
			if (videoIndex >= _movie_res.length) {
				videoIndex = 0;
			}

			/* broadcat _movie_res[i] through video */
			broadcastSet(_video, _movie_res[videoIndex++]);
		}, false);
	} else {
		var _notice = document.createElement("div");
		_notice.innerText = "您现在使用的浏览器不支持video标签";
		var object = document.body.appendChild(_notice);
	}
}

/**
 * @description set movie(video) as background whichi just is broadcast movie
 *              without controls
 * 
 * @param {object}
 *            _movie the object create by document.createElement("movie")
 * @param {String}
 *            _movie_res the movie to be broadcast
 * @return {null} null
 */
function broadcastSet(_movie, _movie_res) {
	/* set id\controls\preload\autoplay\className */
	_movie.id = "_movie";
	// _movie.controls = "controls";
	_movie.preload = "auto";
	_movie.autoplay = "autoplay";
	// _movie.className = "video";

	/*
	 * judge the browser you are using whether support audio which is ogg format
	 * or not && select the suitable format's audio to be broadcast
	 * 
	 * mp4 is much smaller than ogv, so make mp4 header
	 */
	if (_movie.canPlayType("video/mp4")) {
		_movie.src = _movie_res + ".mp4";
	} else if (_movie.canPlayType("video/ogg")) {
		_movie.src = _movie_res + ".ogv";
	} else if (_movie.canPlayType("video/webM")) {
		_movie.src = _movie_res + ".webm";
	}
}

/**
 * @description set movie(video) as background whichi just is broadcast movie
 *              without controls for ie version below 9
 * 
 * @param {Array}
 *            _movie_res Array - path of _movie_res to be set
 * @return {null} null
 */
function _movie_IE(_movie_res) {
	/* create div && append to body */
	var _notice = document.createElement("div");
	_notice.className = "ieMovieDiv";
	var object = document.body.appendChild(_notice);

	/* create embed && set id\src\loop && append to div _notice */
	var _embed = document.createElement("embed");
	_embed.id = "_embed";
	_embed.src = _movie_res[0] + ".avi";
	_embed.autostart = true;
	_embed.loop = true;
	_embed.className = "ieEmbed";
	var object = _notice.appendChild(_embed);
}