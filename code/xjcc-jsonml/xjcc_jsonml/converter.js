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
};


/* Run code in fake browser context */
var filename;
if (!!~process.argv.indexOf("--patched")) {
    filename = require.resolve("jsonml-tools-patched/jsonml-xml.js");
} else {
    filename = require.resolve("jsonml-tools/jsonml-xml.js");
}

var code = fs.readFileSync(filename, "utf-8");
vm.runInNewContext(code, ctx);

xjcc.process_input(function(data, encoding) {
    if (xjcc.to_xml()) {
        return ctx.JsonML.toXMLText(JSON.parse(data));
    } else {
        return JSON.stringify(ctx.JsonML.fromXMLText(data));
    }
});
