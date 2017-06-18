const X2JS = require('x2js')
const xjcc = require('xjcc')

xjcc.process_input(function(data, encoding) {
    var x2js = new X2JS({
        "stripWhitespaces": false,
        "skipEmptyTextNodesForObj": false
    })
    if (xjcc.to_xml()) {
        return x2js.js2xml(JSON.parse(data));
    } else {
        return JSON.stringify(x2js.xml2js(data));
    }
});
