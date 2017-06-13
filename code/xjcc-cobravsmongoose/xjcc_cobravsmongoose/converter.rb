#!/usr/bin/env ruby
gem 'cobravsmongoose', '=0.0.2'
require 'cobravsmongoose'
if ARGV.include? '-d' or ARGV.include? '--decode' then
    puts CobraVsMongoose.json_to_xml(STDIN.read)
else
    # Remove XML declaration (otherwise every single testcase would fail)
    xmldata = STDIN.read.gsub(/<\?xml(\s[^(\?>)]+)?\?>/i, '')
    puts CobraVsMongoose.xml_to_json(xmldata)
end
