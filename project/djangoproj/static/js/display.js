
function switchDispContent(dispid, dispContent) {
    var elem = document.getElementById(dispid);
    console.debug("switch "+dispid+" origin :"+elem.innerHTML);
    elem.innerHTML = dispContent;
    console.debug("switch "+dispid+" display :"+dispContent);
}

function switchDisp(dispid, dispstyle) {
    var elem = document.getElementById(dispid);
    elem.style.display = dispstyle;
    console.debug("switch "+dispid+" display :"+dispstyle);
}
