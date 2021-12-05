import os
import mimetypes
import arrow

def file_type(key):
    additional_file_types = {
        '.md': 'text/markdown'
    }

    file_info = os.path.splitext(key)
    file_extension = file_info[1]
    try:
        return mimetypes.types_map[file_extension]
    except KeyError:
        filetype = 'Unknown'
        if file_info[0].startswith('.') and file_extension == '':
            filetype = 'text'

        if file_extension in additional_file_types.keys():
            filetype = additional_file_types[file_extension]

        return filetype

def datetime_format(date_str):
    # arrow_date = arrow.get(date_str, tzinfo="local")
    arrow_date = arrow.get(date_str, tzinfo="-03:00")
    # print(arrow_date.format("DD-MM-YYYY HH:mm:ss"))
    dt = arrow.get(date_str)
    return dt.humanize()

def encode_key(self, key):
    '''replace bar slash (/) in && => %26%26'''
    encoded_key = key.replace('/','&&')
    return encoded_key

def decode_key(self, key):
    decoded_key = key.replace('&&','/')
    return decoded_key