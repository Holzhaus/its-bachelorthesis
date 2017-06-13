#!/usr/bin/env python3
import csv
import json

infile = 'results/results.json'
with open(infile, mode='r') as f:
    data = json.load(f)

testcases = set()
converters = set()
results = {}

for entry in data:
    basename, testcase, converter = (
            entry[x] for x in ('Basename', 'Testcase', 'Converter'))

    testcases.add((basename, testcase))
    converters.add(converter)
    if testcase not in results:
        results[testcase] = {}
    results[testcase][converter] = entry['Result']

testcases = sorted(testcases, key=lambda x: x[0])
converters = sorted(converters)
categories = {
    'basic': ('basic',),
    'complex': ('complex',),
    'chars': ('chars',),
    'sec': ('fsa', 'dos', 'ssrf'),
}
categories.update({
    'all': tuple(item for sublist in categories.values() for item in sublist),
})

outfile = 'results-%s.csv'
for catname, catprefixes in categories.items():
    with open(outfile % catname, mode='w') as f:
        writer = csv.DictWriter(f, fieldnames=['Index', 'Testcase']+converters)
        writer.writeheader()
        for i, tctuple in enumerate(testcases, start=1):
            basename, testcase = tctuple
            prefix = basename.partition('-')[0]
            if prefix in catprefixes:
                writer.writerow(dict(
                    **{'Index': i, 'Testcase': testcase},
                    **results[testcase]
                ))
