class StreamData:
    def create(self, fields, lst_values):
        if len(fields) != len(lst_values):
            return False
        for i, field in enumerate(fields):
            setattr(self, field, lst_values[i])
        return True

class StreamReader:
    FIELDS = ('id', 'title', 'pages')
