
window.onload = function() {
    var x=document.getElementsByClassName("row_dark");
    var i;
    for (i = 0; i < x.length; i++) {
        var ligne=x[i].parentNode;
        while (ligne.tagName !== "TR") {ligne=ligne.parentNode;}
        ligne.style.backgroundColor = "#e2f5ff";
    }

    x=document.getElementsByClassName("row_light");
    for (i = 0; i < x.length; i++) {
        var ligne=x[i].parentNode;
        while (ligne.tagName !== "TR") {ligne=ligne.parentNode;}
        ligne.style.backgroundColor = "white";
    }

}
