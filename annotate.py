from annotatelib.models import get_model_path_info_map

ANNOTATION_INDICATOR = "====== Schema information"


def write_to_file(model_path, config_path='pynnotate.json', **kwargs):
    path_info_map = get_model_path_info_map(model_path, config_path, **kwargs)
    for model_file in path_info_map.keys():
        add_data_to_file(model_file, path_info_map[model_file])


def add_data_to_file(model_file, model_data):
    with open(model_file, "r+") as f:
        content = f.read()
        f.seek(0, 0)
        model_data_string = format_data(model_data)
        if content.startswith(model_data_string):
            return
        f.write(model_data_string + content)


def format_data(model_data):
    columns = model_data['columns']
    start_string = "#" + ANNOTATION_INDICATOR + "\n"
    max_name_len = max_name_length(list(map(lambda c: c[0], columns.items())))
    columns_string = ''
    for _, column in columns.items():
        columns_string += format_column(column, max_name_len)
    return start_string + columns_string + "\n"


def max_name_length(names):
    return len(max(names))


def format_column(column_hash, max_name_length):
    column_type = column_hash['type']
    if column_hash['length']:
        column_type += '(' + column_hash['length'] + ')'
    notnull = ''
    if column_hash['notnull']:
        notnull = 'not null'
    default = ''
    if column_hash['default']:
        default = 'default(' + column_hash['default'] + ')'
    pk = ''
    if column_hash['pk']:
        pk = 'primary_key'
    template = "# {:<" + str(max_name_length + 2) + "}{:<15}{:<10}{:<10}{:<10}"
    return template.format(column_hash['name'],
                           column_type, notnull, default, pk).strip() + "\n"
