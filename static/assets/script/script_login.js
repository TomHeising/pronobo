var x = document.getElementById("hands");
var y = document.getElementById("animcon");
function closeye() {
  y.style.backgroundImage =
    "url(https://raw.githubusercontent.com/naaficodes/Monkey-Login/master/images/monkey_pwd.gif)";
  x.style.marginTop = "0%";
}
function openeye() {
  y.style.backgroundImage =
    "url(https://raw.githubusercontent.com/naaficodes/Monkey-Login/master/images/monkey.gif)";
  x.style.marginTop = "110%";
}

document.getElementById("pwdbar").addEventListener("focus", function () {
  closeye();
});
