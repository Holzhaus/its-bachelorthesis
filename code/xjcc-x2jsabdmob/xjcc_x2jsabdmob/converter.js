#!/usr/bin/env node
const fs = require("fs")
const path = require("path")
const vm = require("vm")
const xmldom = require("xmldom")
const xjcc = require("xjcc");

/* Create fake browser context by using methods from xmldom module */
const ctx = {
    "DOMParser": xmldom.DOMParser,
    "document": (new xmldom.DOMParser()).parseFromString("<x/>", "text/xml"),
    "window": {
        "DOMParser": xmldom.DOMParser,
        "XMLSerializer": xmldom.XMLSerializer,
        "console": xjcc.logger,
    },
    // Hacky as hell
    "Object": Object,
    "Array": Array,
    "Date": Date,
    "Function": Function,
    "RegExp": RegExp,
};

/* Run code in fake browser context */
var filename = require.resolve("x2js-abdmob/xml2json.js");
var code = fs.readFileSync(filename, "utf-8");
vm.runInNewContext(code, ctx);

xjcc.process_input(function(data, encoding) {
    var x2js = new ctx.X2JS({
        "stripWhitespaces": false
    })
    if (xjcc.to_xml()) {
        return x2js.json2xml_str(JSON.parse(data));
    } else {
        return JSON.stringify(x2js.xml_str2json(data));
    }
});
