#!/usr/bin/env node
const fs = require("fs")
const path = require("path")
const vm = require("vm")
const xmldom = require("xmldom")

/* Create fake browser context by using methods from xmldom module */
const ctx = {
    "DOMParser": xmldom.DOMParser,
    "document": (new xmldom.DOMParser()).parseFromString("<x/>", "text/xml"),
    "window": {
        "DOMParser": xmldom.DOMParser,
        "XMLSerializer": xmldom.XMLSerializer
    }
};

/* Run code in fake browser context */
let filename = require.resolve("jsonml-tools/jsonml-xml.js")
let code = fs.readFileSync(filename, "utf-8");
vm.runInNewContext(code, ctx);

let to_xml = process.argv.includes("-d") || process.argv.includes("--decode");

process.stdin.setEncoding("utf8");
process.stdin.on("readable", () => {
    let chunk = process.stdin.read();
    if (chunk !== null) {
        if (to_xml) {
            process.stdout.write(ctx.JsonML.toXMLText(JSON.parse(chunk)));
        } else {
            process.stdout.write(JSON.stringify(ctx.JsonML.fromXMLText(chunk)));
        }
    }
});
