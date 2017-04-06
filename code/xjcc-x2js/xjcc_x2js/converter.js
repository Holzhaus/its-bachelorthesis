let X2JS = require('x2js')

let to_xml = process.argv.includes("-d") || process.argv.includes("--decode")

process.stdin.setEncoding('utf8');
process.stdin.on('readable', () => {
    let chunk = process.stdin.read();
    if (chunk !== null) {
        let x2js = new X2JS()
        if (to_xml) {
            process.stdout.write(x2js.js2xml(JSON.parse(chunk)));
        } else {
            process.stdout.write(JSON.stringify(x2js.xml2js(chunk)));
        }
    }
});
