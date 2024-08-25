const data = document.currentScript.dataset
const counter_div = document.querySelector("counter")
let counter = 5

setInterval(function () {
  counter_div.text_content = counter
  if (counter == 0) {
    window.location.href = data.redirectUrl
  }
  counter--
}, 1000)
