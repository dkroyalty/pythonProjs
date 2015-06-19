
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
