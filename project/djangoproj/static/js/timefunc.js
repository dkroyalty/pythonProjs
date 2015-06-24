
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
