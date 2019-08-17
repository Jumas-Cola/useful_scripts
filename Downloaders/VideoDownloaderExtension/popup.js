document.addEventListener('DOMContentLoaded', function() {
    var checkPageButton = document.getElementById('DownL');
    checkPageButton.addEventListener('click', function() {
        chrome.tabs.executeScript(null, {file: "contentscript.js"});
    }, false);
}, false);
