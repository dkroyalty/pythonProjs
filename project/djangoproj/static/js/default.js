
function redirectError()
{
    window.location.href = '/error/';
}

function prefixZero(val, minlen) {
    var len = val.toString().length;
    while(len < minlen) {
        val = "0" + val;
        len++;
    }
    return val;
}

function getNowDatetime()
{
    objDate = new Date();
    var year = objDate.getFullYear();
    var month = objDate.getMonth()+1;
    var date = objDate.getDate();
    var hours = objDate.getHours();
    var minutes = objDate.getMinutes();
    var seconds = objDate.getSeconds();
    var retval = "";
    retval += prefixZero(year, 4) + "-";
    retval += prefixZero(month, 2) + "-";
    retval += prefixZero(date, 2) + " ";
    retval += prefixZero(hours, 2) + ":";
    retval += prefixZero(minutes, 2)+":";
    retval += prefixZero(seconds, 2);
    return retval;
}

function setElementContent(elemid, content)
{
    var element = document.getElementById(elemid);
    if (element) {
        console.debug("element " + elemid + " : " + content);
        element.innerHTML = content;
    } else {
        console.debug("not exist element: " + elemid);
    }
}