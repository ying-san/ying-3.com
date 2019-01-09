function apiDoAuth(form, callback) {
    var path = '/api/auth'
    ajax('POST', 'application/json', path, form, callback)
}

function reloadJavaScript() {
    var old = element("#id-js-journal-upload")
    var src = old.src
    delete old

    var script = document.createElement('script')
    script.type= 'text/javascript';
    script.src= src
    log(script)
    document.body.appendChild(script);
}

function doAuthByKeyFile(f) {
    var form = {
       key: f.target.result,
    }

    apiDoAuth(form, function(r) {
        document.documentElement.innerHTML = r
        reloadJavaScript()
    })
}

function bindEventKeyFileSelect() {
    var onKeyFileSelected = function() {
        var f = this.files[0]
        var r = new FileReader();
        r.onload = doAuthByKeyFile

        r.readAsText(f);
    }
    var p = element('#id-praetorian')

    p.addEventListener('change', onKeyFileSelected, false)
}

function bindEvent() {
    bindEventKeyFileSelect()
}

function _main() {
    bindEvent()
}

_main()