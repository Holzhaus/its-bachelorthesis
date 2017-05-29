/**
 * XJCC module for NodeJS
 *
 * Provides helper functions for NodeJS converter plugins
 */
const logger = new console.Console(process.stderr);
const data_size_threshold = 100 * 1024;

let to_xml = function(args=process.argv) {
    return args.includes("-d") || args.includes("--decode");
}

let process_input = function(callback, inputstream=process.stdin, outputstream=process.stdout, encoding="utf-8") {
    process.stdin.setEncoding(encoding);
    let data = "";
    inputstream.on("readable", function() {
        let chunk;
        while (chunk = process.stdin.read()) {
            data += chunk;
            logger.info("Input read: %d chars / %d bytes (last chunk: %d chars / %d bytes)",
                        data.length, Buffer.byteLength(data, encoding),
                        chunk.length, Buffer.byteLength(chunk, encoding));
        }
    });
    inputstream.on("end", function () {
        let data_bytes = Buffer.byteLength(data, encoding);
        logger.info("Total input read: %d chars / %d bytes", data.length, data_bytes);
        if (data_bytes >= data_size_threshold) {
            logger.warn("Input is quite big, this may take a while...");
        }
        let output = callback(data, encoding);
        if (outputstream !== null) {
            outputstream.write(output);
        }
    });
}

module.exports = {
    "logger": logger,
    "to_xml": to_xml,
    "process_input": process_input
}
