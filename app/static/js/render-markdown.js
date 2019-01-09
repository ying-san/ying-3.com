function renderMarkdown () {
    var t = element('#id-title')
    var c = element('#id-content')
    var mt = marked(t.innerHTML)
    var mc = marked(c.innerHTML)

    t.innerHTML = mt
    c.innerHTML = mc
}

function __main() {
    renderMarkdown()
}

__main()