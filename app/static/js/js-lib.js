function log() {
    console.log.apply(console, arguments)
}

function element(sel) {
    return document.querySelector(sel)
}

function time(timestamp) {
    var d = new Date(timestamp*1000)
    return d.toLocaleString()
}

function ajax(method, type, path, data, responseCallback) {
    var r = new XMLHttpRequest()

    r.open(method, path, true)
    r.setRequestHeader('Content-Type', type)
    r.onreadystatechange = function() {
        if(r.readyState === 4) {
            responseCallback(r.response)
        }
    }
    data = JSON.stringify(data)

    r.send(data)
}

function replaceNewLineCharacter(s) {
    return replaceAll(replaceAll(replaceAll(s,"\r\n","<br>"),"\n","<br>"),"\r","<br>")
}

function replaceAll(s, search, replacement) {
    return s.replace(new RegExp(search, 'g'), replacement)
}
