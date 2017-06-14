#!/usr/bin/env python3
import csv
import json
import sys

data = json.load(sys.stdin)

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

num_successes = {}
outfile = 'results-%s.csv'
for catname, catprefixes in categories.items():
    filename = outfile % catname
    print('Writing file: %s' % filename)
    with open(filename, mode='w') as f:
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
                for converter, result in results[testcase].items():
                    success = 1 if result == 'OK' else 0
                    if converter not in num_successes:
                        num_successes[converter] = 0
                    num_successes[converter] += success
        if num_successes:
            writer.writerow(dict(
                **{'Index': '', 'Testcase': 'Gesamt'},
                **num_successes
            ))

