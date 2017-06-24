#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import statistics
import sys
import json
import ijson
import terminaltables
sys.setrecursionlimit(10000)

parser = ijson.parse(sys.stdin)

EVENTS = [
    'null',
    'boolean',
    'number',
    'string',
    'map_key',
    'start_map',
    'end_map',
    'start_array',
    'end_array',
]

EVENT_DATATYPE = {
    'null': 'null',
    'boolean': 'boolean',
    'number': 'number',
    'string': 'string',
    'array': 'start_array',
    'map': 'start_map',
    'map key string': 'map_key',
}

CONTAINER_ARRAY = 0
CONTAINER_MAP = 1

stats = {event: 0 for event in EVENTS}

maxdepth = 0
keys_per_map = []
items_per_array = []

current_container_elemcount = []
current_container = []
for prefix, event, value in parser:
    stats[event] += 1
    if event in ('end_map', 'end_array'):
        maxdepth = max(len(current_container), maxdepth)
        if current_container.pop() == CONTAINER_MAP:
            keys_per_map.append(current_container_elemcount.pop())
        else:
            items_per_array.append(current_container_elemcount.pop())
    elif event == 'map_key':
        current_container_elemcount[-1] += 1
    else:
        if current_container and current_container[-1] == CONTAINER_ARRAY:
            current_container_elemcount[-1] += 1
        if event == 'start_map':
            current_container.append(CONTAINER_MAP)
            current_container_elemcount.append(0)
        elif event == 'start_array':
            current_container.append(CONTAINER_ARRAY)
            current_container_elemcount.append(0)
total_values = sum(stats[key] for key in EVENT_DATATYPE.values())

table_data = []
for datatype, key in EVENT_DATATYPE.items():
    table_data.append(('number of %ss' % datatype, stats[key]))
table_data.append(('Total number of values', total_values))

table_data.append(('', ''))
try:
    mean_keys_per_map = statistics.mean(keys_per_map)
except statistics.StatisticsError:
    mean_keys_per_map = 0
try:
    median_keys_per_map = statistics.median(keys_per_map)
except statistics.StatisticsError:
    median_keys_per_map = 0

table_data.append(('Total number of map keys', sum(keys_per_map)))
table_data.append(('Most keys in a single map', max(keys_per_map, default=0)))
table_data.append(('Average keys per map', mean_keys_per_map))
table_data.append(('Median keys per map', median_keys_per_map))

table_data.append(('', ''))
try:
    mean_items_per_array = statistics.mean(items_per_array)
except statistics.StatisticsError:
    mean_items_per_array = 0
try:
    median_items_per_array = statistics.median(items_per_array)
except statistics.StatisticsError:
    median_items_per_array = 0

table_data.append(('Total number of array items', sum(items_per_array)))
table_data.append(('Most items in a single array', max(items_per_array, default=0)))
table_data.append(('Average items per Array', mean_items_per_array))
table_data.append(('Median items per Array', median_items_per_array))

table_data.append(('', ''))

table_data.append(('Maximum nesting depth', maxdepth))

if '--json' in sys.argv:
    print(json.dumps(dict(tpl for tpl in table_data if tpl != ('', ''))))
else:
    table_instance = terminaltables.PorcelainTable(table_data)
    table_instance.inner_heading_row_border = False
    table_instance.justify_columns[1] = 'right'
    print(table_instance.table)
