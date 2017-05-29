let X2JS = require('x2js')
let xjcc = require('xjcc')

xjcc.process_input(function(data, encoding) {
    let x2js = new X2JS()
    if (xjcc.to_xml()) {
        return x2js.js2xml(JSON.parse(data));
    } else {
        return JSON.stringify(x2js.xml2js(data));
    }
});
