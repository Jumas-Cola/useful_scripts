// Работает на многих сайтах, кнопка на скачивание появляется внизу страницы.
var l = 0;
var mas_elem = document.querySelectorAll('video');
for (var i = 0; i < mas_elem.length; i++) {
  if (mas_elem[i].hasAttribute("src")) {
    if (mas_elem[i].getAttribute("src").indexOf("http") != -1) {
      l = mas_elem[i].getAttribute("src");
      break;
    }
  }
}
if (l == 0) {
  mas_elem = document.querySelectorAll('video source');
  for (var i = 0; i < mas_elem.length; i++) {
    if (mas_elem[i].hasAttribute("src")) {
      if (mas_elem[i].getAttribute("src").indexOf("http") != -1) {
        l = mas_elem[i].getAttribute("src");
        break;
      }
    }
  }
}
if (l == 0) {
  mas_elem = document.querySelectorAll('source');
  for (var i = 0; i < mas_elem.length; i++) {
    if (mas_elem[i].hasAttribute("src")) {
      if (mas_elem[i].getAttribute("src").indexOf("http") != -1) {
        l = mas_elem[i].getAttribute("src");
        break;
      }
    }
  }
}
if (l == 0) {
  alert("NotFound");
} else {
  var newlink = document.createElement('a');
  newlink.setAttribute('target', '_blank');
  newlink.setAttribute('href', l);
  newlink.click();
}
