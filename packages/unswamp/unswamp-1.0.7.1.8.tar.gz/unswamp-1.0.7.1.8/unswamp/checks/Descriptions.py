class Descriptions:
    _check_descriptions = {
        "CheckTableColumnsExist": "A check of type '{name}' checks if all provided columns {table_columns} do exist in the dataset the check will be applied on.",
        "CheckTableRowRange": "A check of type '{name}' checks if the number of rows in the provided dataset is between '{min_rows}' and '{max_rows}' (e.g. rows >= {min_rows} and rows <= {max_rows})."
    }

    @staticmethod
    def get_check_description(check_name, data):
        desc = None
        if check_name in Descriptions._check_descriptions:
            try:
                desc = Descriptions._check_descriptions[check_name]
                desc = desc.format(**data)
            except KeyError:
                "this can happen if not all needed properties are initialized!"
                pass
        return desc
