class Descriptions:
    _check_descriptions = {
        "CheckTableColumnsExist": "A check of type '{name}' checks if all provided columns {table_columns} do exist in the dataset the check will be applied on.",
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
