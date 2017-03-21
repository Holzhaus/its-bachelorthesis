let JXON = require('jxon')

let to_xml = process.argv.includes("-d") || process.argv.includes("--decode")

process.stdin.setEncoding('utf8');
process.stdin.on('readable', () => {
    let chunk = process.stdin.read();
    if (chunk !== null) {
        if (to_xml) {
            process.stdout.write(JXON.jsToString(JSON.parse(chunk)));
        } else {
            process.stdout.write(JSON.stringify(JXON.stringToJs(chunk)));
        }
    }
});
