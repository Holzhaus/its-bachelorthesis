let JXON = require('jxon')
let xjcc = require('xjcc')

xjcc.process_input(function(data, encoding) {
    if (xjcc.to_xml()) {
        return JXON.jsToString(JSON.parse(data));
    } else {
        return JSON.stringify(JXON.stringToJs(data));
    }
});
