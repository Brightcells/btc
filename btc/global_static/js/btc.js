function visit(_url, sid, url){
    //window.open(url);
	leftTimeObj = $(".limit ." + sid + ".red");
	leftTimeObj.html($(".limit ." + sid + ".red").next().html());

	$.ajax({
		type: "post",
		url: _url,
		data: {siteid: sid},
		success: function(json){
            // do nothing no matter what server response
		}
	});
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

/**
 * @description control the back topimg's display
 * 
 * @param
 * 
 * @return
 */
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

function hasClass(ele,cls) {
  return ele.className.match(new RegExp('(\\s|^)' + cls + '(\\s|$)'));
}
 
function addClass(ele,cls) {
  if (!this.hasClass(ele,cls)) ele.className += " " + cls;
}
 
function removeClass(ele,cls) {
  if (hasClass(ele,cls)) {
    var reg = new RegExp('(\\s|^)' + cls + '(\\s|$)');
    ele.className = ele.className.replace(reg, ' ');
  }
}

function controlbg() {
	bObj = document.getElementById("bodyer");
	fObj = document.getElementById("footer");
	
	if(hasClass(bObj, "hide")) {
		removeClass(bObj, "hide");
		removeClass(fObj, "hide");
	} else {
		addClass(bObj, "hide");
		addClass(fObj, "hide");
	}
};

/**
 * @description add link for url when string contains url
 * 
 * @param
 * 
 * @return {String} replaced string
 */
/*
	ref: http://www.zhangxinxu.com/wordpress/2010/04/javascript%E5%AE%9E%E7%8E%B0http%E5%9C%B0%E5%9D%80%E8%87%AA%E5%8A%A8%E6%A3%80%E6%B5%8B%E5%B9%B6%E6%B7%BB%E5%8A%A0url%E9%93%BE%E6%8E%A5/
*/
String.prototype.httpHtml = function(){
	var reg = /(http:\/\/|https:\/\/)((\w|=|\?|\.|\/|&|-)+)/g;
	return this.replace(reg, '<a href="$1$2"target="_blank" >$1$2</a>');
};

!function ($) {
	$(function () {
		var $window = $(window);

		// Disable certain links in docs
		$("section [href^=#]").click(function (e) {
			e.preventDefault();
		});

		// side bar
		$(".bs-docs-sidenav").affix({offset:{top:function () {
			return $window.width() <= 980 ? 290 : 210;
		}, bottom:270}});
	});
}(window.jQuery);

/**
 * @description alter the site's left time, one minute the num minus one
 * 
 * @param
 * 
 * @return
 */
function alterLeftTime(){
	$(".limit .red").each(function(){
	    var newLeftTime = parseInt($(this).html())-1;
		if (newLeftTime >= 0) {
			$(this).html(parseInt($(this).html())-1);
		} else {
			// do nothing
		}
	});
	$(".alert").addClass("hidden");
}