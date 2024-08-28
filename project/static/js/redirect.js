const data = document.getElementsByClassName("url")[0]
const counter_div = document.getElementsByClassName("counter")[0]
let counter = 4
let redirect_timer = setInterval(function () {
  counter_div.textContent = counter
  if (counter == 0) {
    window.location.href = data.href
  }
  counter--
}, 1000)

const cancel_btn = document.getElementsByClassName("cancel")[0]
cancel_btn.addEventListener("click", function () {
  clearInterval(redirect_timer)
  counter_div.textContent = "cancelled"
  cancel_btn.disabled = true
})
