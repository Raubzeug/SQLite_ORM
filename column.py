class Column():
    """I mention here only two data types to reduce code volume"""
    def __init__(self, data_type, req=False, pk=False):
        if data_type.upper() not in ('INTEGER', 'TEXT'):
            raise TypeError("column type may be 'INTEGER', 'TEXT'")
        else:
            self.data_type = data_type.upper()
        self.req = 'NOT NULL' if req else ''
        self.pk = 'PRIMARY KEY' if pk else ''

    def __str__(self):
        """this is made to simplify representation in Model class"""
        repr = self.data_type
        if self.req:
            repr += ' ' + self.req
        if self.pk:
            repr += ' ' + self.pk
        return repr