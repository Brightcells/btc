function visit(_url, sid, url){
    window.open(url);
	$.ajax({
		type: "post",
		url: _url,
		data: {siteid: sid},
		success: function(json){
            // do nothing no matter what server response
		}
	});
	event.preventDefault();
}

function myLikeFavAjax(_iObj, _spanObj, _url, _data){
	/* http://stackoverflow.com/questions/2360625/add-class-to-an-element */
	var iObj = _iObj;
	var spanObj = _spanObj;
		
	iObj.classList.add("clicked");
	$.ajax({
		type: "post",
		url: _url,
		data: _data,
		success: function(json){
			jsonObj = eval ("(" + json + ")");
			num = jsonObj['errorCode'];
			if(num in {'200200': '', '300200': ''}){
			    iObj.classList.add("icon-white", "done");
			    spanObj.text(parseInt(spanObj.text())+1);
			}else if(num in {'200202': '', '300202': ''}){
				iObj.classList.remove("icon-white", "done");
			    spanObj.text(parseInt(spanObj.text())-1);
			}
		}
	});
	event.preventDefault();
	iObj.classList.remove("clicked");	
}

/**
 * @description check the browser you are using
 * 
 * @param
 * 
 * @return {Object} Sys
 */
function browserCheck() {
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

window.onscroll = function () {
    var scrHeight = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;
    if (scrHeight >= 250) {
    	document.getElementById("backtop").style.display = "block";
    } else {
    	document.getElementById("backtop").style.display = "none";
    }
};

function backtop() {
    scroll(0, 0);
};