function five(){
  window.location.replace("https://itsfoxdev.github.io/FoxClient/5/");
}

function eight(){
  window.location.replace("https://itsfoxdev.github.io/FoxClient/8/");
}

function loadAnim(){
  var l = document.getElementById('animi');
  var t = document.getElementById('animt');
  var c = document.getElementById('animc');
  setTimeout(function(){l.style.scale=1}, 10);
  setTimeout(function(){t.style.width="302px"}, 510);
  setTimeout(function(){c.style.height="0px"}, 2000);
}
loadAnim();
