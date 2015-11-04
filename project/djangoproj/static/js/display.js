
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

function setMultiSelected(elemids, setvalues) {
    var elemarr=elemids.split(',');
    var valuearr=setvalues.split(',');
    if (elemarr.length != valuearr.length) {
        return;
    }
    for (var i = elemarr.length - 1; i >= 0; i--) {
        console.debug(elemarr[i]+" -> "+valuearr[i]);
        setElemSelected(elemarr[i], valuearr[i]);
    };
}

function setElemSelected(elemid, selectcond) {
    var opts = document.getElementById(elemid);
    if(selectcond != ""){
        for(var i=0; i<opts.options.length; i++){
            if(selectcond==opts.options[i].value){
                opts.options[i].selected = 'selected';
                break;
            }
        }
    }
}