function copy(t) {
  var i = document.createElement("input");
  i.style.display = "none";
  i.value = t;
  document.body.appendChild(i);
  i.select();
  i.setSelectionRange(0, 99999);
  navigator.clipboard.writeText(i.value);
  i.remove();
}
function after(str, txt) {
  return str.split(txt)[1];
}
function before(str, txt) {
  return str.split(txt)[0];
}
function checkJoin(m) {
  if (m.includes("[CHAT] Welcome to VanillaMC")) {
    vanillaCraft();
  }
}
let clog = console.info;
console.info = function (msg) {
  checkJoin(msg);
};
function vanillaCraft() {
  document.getElementById("fcvanilla").style.display = 'flex';
  console.info = function (msg) {
    checkMsg(msg);
    clog(msg);
  };
  function next5(x) {
    return Math.ceil(x / 5) * 5;
  }
  function checkMsg(m) {
    if (m.includes("The first person to calculate")) {
      let mathtoast = document.getElementById("fcvmanswer");
      let prob = before(after(m, "to calculate"), "wins $");
      mathtoast.innerHTML = "Answer: " + eval(prob);
      copy(eval(prob));
    }
    if (m.includes('seconds!')){
      let mathtoast = document.getElementById("fcvmanswer");
      mathtoast.innerHTML='No question';
    }
  }
  function quizTime(){
    let quiztoast = document.getElementById('fcvquiztime');
    const d = new Date();
    let min = d.getMinutes();
    let sec = d.getSeconds();
    function checkMin(){
      if (min % 5 === 0){
        return min+1;
      } else {
        return min;
      }
    }
    let mc=Math.ceil(checkMin() / 5) * 300;
    let mv=min*60;
    let ms=mv+sec;
    let tl=mc-ms+30;
    quiztoast.innerHTML='~' + tl + 's until quiz';
    console.log(tl + ' seconds until quiz');
  }
  let quizint = setInterval(() => quizTime(), 1000);

}
