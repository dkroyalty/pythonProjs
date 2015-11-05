
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

function setItemSelectOption(itemJsData)
{
    console.debug("receive item js: "+itemJsData);
    var eachItemArr = itemJsData.split('|');
    for(var i=0; i<eachItemArr.length; i++){
        console.debug("build item js: "+eachItemArr[i]);
        var itemdata = eachItemArr[i].split(',');
        setElemSelected("select_type_"+itemdata[0], itemdata[1])
        setElemSelected("select_status_"+itemdata[0], itemdata[2])
    }
}

function setElemSelected(elemid, selectcond) {
    console.debug("set elem "+elemid+" -> "+selectcond);
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