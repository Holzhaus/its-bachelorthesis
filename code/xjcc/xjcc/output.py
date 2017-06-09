# -*- coding: utf-8 -*-
import os
import os.path
import csv
import io
import json
import terminaltables


class OutputTable(object):
    def __init__(self, fieldnames):
        self.fieldnames = fieldnames
        self.data = []

    def add(self, row):
        missing_fieldnames = set(self.fieldnames) - set(row.keys())
        if missing_fieldnames:
            raise ValueError('Missing Fieldnames: %s',
                             ''.join(missing_fieldnames))
        else:
            self.data.append(row)

    def get_data(self, sort_key=None):
        if sort_key is not None:
            return sorted(self.data, key=sort_key)
        else:
            return self.data

    def to_csv(self, **kwargs):
        csvfile = io.StringIO()
        writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
        writer.writeheader()
        writer.writerows(self.get_data(**kwargs))
        output = csvfile.getvalue()
        csvfile.close()
        return output

    def to_json(self, **kwargs):
        return json.dumps(self.get_data(**kwargs), sort_keys=True, indent=2)

    def to_text(self, title=None, **kwargs):
        table_data = [self.fieldnames] + [
            [row[key] for key in self.fieldnames]
            for row in self.get_data(**kwargs)
        ]

        table_instance = terminaltables.AsciiTable(table_data, title=title)
        return table_instance.table

    def output(self, fmt='text', title=None, **kwargs):
        if fmt == 'text':
            data = self.to_text(title=title, **kwargs)
        elif fmt == 'json':
            data = self.to_json(**kwargs)
        elif fmt == 'csv':
            data = self.to_csv(**kwargs)
        else:
            raise ValueError('Unknown output format \'%s\'!' % fmt)
        return data


def write_results(testresult, output_root):
    path = os.path.join(output_root, testresult.converter.name)
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    if testresult.json_output is not None:
        json_file = os.path.join(path, '%s.json' % testresult.test.shortname)
        with open(json_file, mode='wb') as f:
            f.write(testresult.json_output)

    if testresult.xml_output is not None:
        xml_file = os.path.join(path, '%s.xml' % testresult.test.shortname)
        with open(xml_file, mode='wb') as f:
            f.write(testresult.xml_output)
