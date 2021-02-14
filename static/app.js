function getSelectValues(select) {
    var result = [];
    var options = select && select.options;
    var opt;

    for (var i = 0, iLen = options.length; i < iLen; i++) {
        opt = options[i];

        if (opt.selected) {
            result.push(opt.value || opt.text);
        }
    }
    return result;
}

function searchtags(f) {
    event.preventDefault();
    var sel = document.getElementsByTagName('select')[0];
    var t = getSelectValues(sel)
    console.log(t)

    var cards = document.getElementsByClassName("card-body");
    console.log(cards)

    // for (card of cards) {
    //     card.parentElement.classList.remove("card");
    //     card.style.visibility = "hidden";
    // }
    var res = document.getElementById("result")
    for (card of cards) {
        for (var i = 2; i < card.children.length - 3; i++) {
            console.log(card.children[i].textContent)
            for (stag of t) {
                if (stag == card.children[i].textContent) {
                    console.log(stag)
                    res.append(card.parentElement.parentElement)
                    // card.style.visibility = "visible";
                    // card.parentElement.classList.add("card");
                    break;
                }
            }
        }
    }

    res.parentElement.style.display = "block";
    console.log(cards)
}

function submit(event) {
    event.preventDefault();
}