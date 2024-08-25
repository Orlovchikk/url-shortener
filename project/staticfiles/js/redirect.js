const data = document.getElementsByClassName("url")[0]
const counter_div = document.getElementsByClassName("counter")[0]
let counter = 4

setInterval(function () {
  counter_div.textContent = counter
  if (counter == 0) {
    window.location.href = data.href
  }
  counter--
}, 1000)
