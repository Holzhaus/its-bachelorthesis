/**
 * XJCC module for NodeJS
 *
 * Provides helper functions for NodeJS converter plugins
 */
const logger = new console.Console(process.stderr);
const data_size_threshold = 100 * 1024;

const to_xml = function(args) {
    args = (args == null ? process.argv : args);
    return !!(~args.indexOf("-d")) || (~args.indexOf("--decode"));
}

const process_input = function(callback, inputstream, outputstream, encoding) {
    inputstream = (inputstream == null ? process.stdin : inputstream);
    outputstream = (outputstream == null ? process.stdout : outputstream);
    encoding = (encoding == null ? "utf-8" : encoding);
    process.stdin.setEncoding(encoding);
    var data = "";
    inputstream.on("readable", function() {
        var chunk;
        while (chunk = process.stdin.read()) {
            data += chunk;
            logger.info("Input read: %d chars / %d bytes (last chunk: %d chars / %d bytes)",
                        data.length, Buffer.byteLength(data, encoding),
                        chunk.length, Buffer.byteLength(chunk, encoding));
        }
    });
    inputstream.on("end", function () {
        var data_bytes = Buffer.byteLength(data, encoding);
        logger.info("Total input read: %d chars / %d bytes", data.length, data_bytes);
        if (data_bytes >= data_size_threshold) {
            logger.warn("Input is quite big, this may take a while...");
        }
        var output = callback(data, encoding);
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
