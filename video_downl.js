// Работает на многих сайтах, кнопка на скачивание появляется внизу страницы.
var div = document.createElement('div');
var l=0;
var mas_elem = document.querySelectorAll('video');
for (var i = 0; i < mas_elem.length; i++) {
   if (mas_elem[i].hasAttribute("src")) {
   		if (mas_elem[i].getAttribute("src").indexOf("http")!=-1) {
   			l = mas_elem[i].getAttribute("src");
   			break;
   		}
	}
}
if (l==0) {
	mas_elem = document.querySelectorAll('video source');
	for (var i = 0; i < mas_elem.length; i++) {
	   if (mas_elem[i].hasAttribute("src")) {
	   		if (mas_elem[i].getAttribute("src").indexOf("http")!=-1) {
	   			l = mas_elem[i].getAttribute("src");
	   			break;
	   		}
		}
	}
}
if (l==0) {
	mas_elem = document.querySelectorAll('source');
	for (var i = 0; i < mas_elem.length; i++) {
	   if (mas_elem[i].hasAttribute("src")) {
	   		if (mas_elem[i].getAttribute("src").indexOf("http")!=-1) {
	   			l = mas_elem[i].getAttribute("src");
	   			break;
	   		}
		}
	}
}
if (l==0) {
	alert("NotFound");
} else {
div.innerHTML = '<a href='+l+' target="_blank"><button style="position:absolute; margin-top:5%; margin-bottom:5%; margin-left:50%; background-color: #2fd47b;height: 35px;border-radius: 50px;color: #fff;font-size: 15px;font-weight: 700;line-height: 30px;align-items: center;border: none;padding-top: 2px; padding-left:1rem; padding-right:1rem; z-index: 999999;">Скачать</button></a>';
document.body.appendChild(div);
}
