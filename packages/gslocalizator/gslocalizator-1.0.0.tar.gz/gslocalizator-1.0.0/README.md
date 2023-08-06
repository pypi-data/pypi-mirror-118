
### Quick Start

#### Install
```
pip3 install gslocalizator
```
#### Using
```py
#!/usr/bin/env python
from gslocalizator import GoogleSheetLocalizator as GSLr
from cfg import *


def main():
    with GSLr(GSL_CREDS_FILE, GSL_SPREADSHEET_ID) as gslr:
        gslr.tran(
            from_sheet_range='main!A1:E',
            with_key_column='iOS（IM）Key',
            from_value_column_to_file={
                'zh-Hans': '.datas/ios/strings_main/zh-Hans.lproj/Localizable.strings',
                'zh-Hant': '.datas/ios/strings_main/zh-Hant.lproj/Localizable.strings',
                'en': '.datas/ios/strings_main/en.lproj/Localizable.strings',
                'ja': '.datas/ios/strings_main/ja.lproj/Localizable.strings',
            },
            exclude_headers=['//']
        ).request(
        ).save(format="iOS")


if __name__ == '__main__':
    main()
```

## cell formater

Cell formater used to format cells in the spreadsheet.

for example:

title of key| title of lang1|title of lang2|...
-----|-----|-----|-----
Hello|Hello|您好|hhhh
world|world|世界|wwww

key_formater  only be used to cells that under "title of key".

![key_formater area](docs/key_formater_area.png)

You can custom your formater for keys and cells
```py
def cell_fmter(val: str) -> str:
    return re.sub("\s+", " ", val).strip().replace("%s", "%@").replace("\"", "\\\"")


def key_fmter(val: str) -> str:
    return re.sub("\s+", " ", val).strip().replace("%s", "%@")


def load():
    # ...
    with GSLr(GSL_CREDS_FILE, GSL_SPREADSHEET_ID) as gslr:
        gslr.tran(
            from_sheet_range='bizA!A1:F',
            with_key_column='key',
            from_value_column_to_file={
                'zh-Hans': '.datas/ios/strings_biz_a/zh-Hans.lproj/Localizable.strings',
                'zh-Hant': '.datas/ios/strings_biz_a/zh-Hant.lproj/Localizable.strings',
                'en': '.datas/ios/strings_biz_a/en.lproj/Localizable.strings',
                'ja': '.datas/ios/strings_biz_a/ja.lproj/Localizable.strings',
            },
            exclude_headers=['//'],
            cell_formater=cell_fmter
        ).request(
        ).save(format="iOS")
    # ...
```

```py
# replace "'" to "\'" demo
def cell_fmter(val: str) -> str:
    aVal = re.sub('\w(\')', lambda x: x.group(1), val) # replace "'" to "\'"
    return re.sub("\s+", " ", aVal).strip().replace("%s", "%@").replace("\"", "\\\"")
```

### You can merge diffrent sheets to one file.

Sheet "bizA" and sheet "main" merge to "app/***/strings.xml"

```py

def request_android(gslr: GSLr):
    gslr.reset()
    gslr.tran(
        from_sheet_range='bizA!A1:E',
        with_key_column='key',
        from_value_column_to_file={
            'zh-Hans': '.datas/android/app/values-zh-rCN/strings.xml',
            'zh-Hant': '.datas/android/app/values-zh-rTWj/strings.xml',
            'en': '.datas/android/app/values/strings.xml',
            'ja': '.datas/android/app/values-ja-rJP/strings.xml',
        },
        exclude_headers=['//'],
        cell_formater=cell_fmter,
        key_formater=key_fmter
    ).tran(
        from_sheet_range='main!A1:E',
        with_key_column='iOS（IM）Key',
        from_value_column_to_file={
            'zh-Hans': '.datas/android/app/values-zh-rCN/strings.xml',
            'zh-Hant': '.datas/android/app/values-zh-rTWj/strings.xml',
            'en': '.datas/android/app/values/strings.xml',
            'ja': '.datas/android/app/values-ja-rJP/strings.xml',
        },
        exclude_headers=['//']
    ).request(
    ).save(format="Android")

```

### Or you can write diff sheets to their own files.

Sheet "bizA" save to "strings_biz_a/***/strings.xml"

Sheet "main" save to "strings_main/***/strings.xml"

```py

def request_android(gslr: GSLr):
    gslr.reset()
    gslr.tran(
        from_sheet_range='bizA!A1:E',
        with_key_column='key',
        from_value_column_to_file={
            'zh-Hans': '.datas/android/strings_biz_a/values-zh-rCN/strings.xml',
            'zh-Hant': '.datas/android/strings_biz_a/values-zh-rTWj/strings.xml',
            'en': '.datas/android/strings_biz_a/values/strings.xml',
            'ja': '.datas/android/strings_biz_a/values-ja-rJP/strings.xml',
        },
        exclude_headers=['//'],
        cell_formater=cell_fmter,
        key_formater=key_fmter
    ).tran(
        from_sheet_range='main!A1:E',
        with_key_column='iOS（IM）Key',
        from_value_column_to_file={
            'zh-Hans': '.datas/android/strings_main/values-zh-rCN/strings.xml',
            'zh-Hant': '.datas/android/strings_main/values-zh-rTWj/strings.xml',
            'en': '.datas/android/strings_main/values/strings.xml',
            'ja': '.datas/android/strings_main/values-ja-rJP/strings.xml',
        },
        exclude_headers=['//']
    ).request(
    ).save(format="Android")

```