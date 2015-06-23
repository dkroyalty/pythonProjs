
function switchClassNameActive(elemid, classname) {
    var re = /active/;
    var prevname = document.getElementById(elemid).className;
    var testexist = re.test(prevname);
    var usename = testexist ? classname : classname+" active";
    document.getElementById(elemid).className = usename;
}

function switchDisplayMenu() {
    console.debug("execute switchDisplayMenu");
    switchClassNameActive("menubutton", "menu-button");
    switchClassNameActive("menucontent", "nav-menu-on");
}

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
    objDate=new Date();
    var year=objDate.getFullYear();
    var month=objDate.getMonth()+1;
    var date=objDate.getDate();
    var hours=objDate.getHours();
    var minutes=objDate.getMinutes();
    var seconds=objDate.getSeconds();
    var retval = "";
    retval += prefixZero(year, 4) + "-";
    retval += prefixZero(month, 2) + "-";
    retval += prefixZero(date, 2) + " ";
    retval += prefixZero(hours, 2) + ":";
    retval += prefixZero(minutes, 2)+":";
    retval += prefixZero(seconds, 2);
    return retval;
}

function timeCount(elemid)
{
    function valueTime() {
        setElementContent(elemid, "当前时间 " + getNowDatetime());
        setTimeout(valueTime, 1000);
    }
    setTimeout(valueTime, 1000);
}

function startCounting(elemid, counttime, url, step)
{
    var counter = counttime;
    setElementContent(elemid, counter.toString()+"秒后自动跳转回首页...");
    function countDown() {
        if (counter > 0) {
            console.debug("counter: " + counter.toString());
            counter -= step;
            setElementContent(elemid, counter.toString()+"秒后自动跳转回首页...");
            setTimeout(countDown, 1000);
        } else {
            window.location.href = url;
        }
    }
    setTimeout(countDown, 1000);
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