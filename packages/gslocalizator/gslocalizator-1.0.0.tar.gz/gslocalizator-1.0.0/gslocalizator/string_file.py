from typing import Dict, Optional, List, TypeVar
from ezutils.files import writelines
import os


class _StringRow:

    def __init__(self, k: str, v: str, is_android_formatted_false):
        self.k = k
        self.v = v
        self.is_android_formatted_false = is_android_formatted_false

    def __eq__(self, o: object) -> bool:
        return o.k == self.k

    def __hash__(self):
        return hash(self.k)


T = TypeVar('T', bound='StringFile')


class StringFile:

    def __init__(self, column_title: str, filename_to_save: str):
        self.filename = filename_to_save
        self.column_title = column_title
        self.column_index = -1
        self.rows = []  # [[key1, value1],[key2, value2], ...]

    def __eq__(self, o: object) -> bool:
        return o.filename == self.filename

    def __hash__(self):
        return hash(self.filename)

    def update_column_index(self, title_row: List[str], key_col_idx: int):
        index = 0
        title_without_key = []
        title_without_key.extend(title_row[:key_col_idx])
        title_without_key.extend(title_row[key_col_idx+1:])

        for title in title_without_key:
            if self.column_title == title:
                self.column_index = index
                return
            index += 1

    def add_row(self, key_of_row, value, is_android_formatted_false=False):
        if key_of_row == None or len(key_of_row) == 0:
            return

        item = _StringRow(key_of_row, value, is_android_formatted_false)
        if item in self.rows:
            # replace row with item
            self.rows = [item if item == row else row for row in self.rows]
        else:
            self.rows.append(item)

    def android_formatted_false(self, row):
        for cell in row:
            if cell.find('formatted=false') >= 0:
                return True
        return False

    def _rows_to_save(self, format: str):
        if format == "iOS":
            rows_to_save = ["// AUTO-GENERATED"]
            rows_to_save.extend(
                list(
                    map(lambda row: f'"{row.k}" = "{row.v}";', self.rows))
            )
            return rows_to_save

        if format == "Android":
            rows_to_save = [
                '<?xml version="1.0" encoding="utf-8"?>',
                '<!-- AUTO-GENERATED  -->'
                '', '<resources>'
            ]

            rows_to_save.extend(
                list(
                    map(lambda row:
                        f'  <string name="{row.k}" formatted="false">{row.v}</string>'
                        if row.is_android_formatted_false
                        else f'  <string name="{row.k}">{row.v}</string>', self.rows))

            )
            rows_to_save.extend(
                ['</resources>']
            )
            return rows_to_save

        if format == "Flutter":
            rows_to_save = ['{']
            rows_to_save.extend(
                list(map(lambda row: f'    "{row.k}":"{row.v}",', self.rows)))
            rows_to_save.extend(
                ['}']
            )
            return rows_to_save

        ex = Exception('Not supported')
        raise ex

    def save(self, format: str):
        out_dir, filename = os.path.split(self.filename)
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)

        print(f'{len(self.rows)} records -> {self.filename}')
        writelines(self._rows_to_save(format), self.filename)

    def merge_file(self, file_to_be_merge: T) -> T:
        for row in file_to_be_merge.rows:
            self.add_row(row.k, row.v, row.is_android_formatted_false)
        return self
