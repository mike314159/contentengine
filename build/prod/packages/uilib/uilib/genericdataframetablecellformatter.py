
import datetime


class GenericDataframeTableCellFormatter:
    """
    formats = {
        'score': 'percent',
        'total': 'int',
    }
    """

    def __init__(self, formats):
        self.formats = formats

    def format_int(value):
        try:
            return "%d" % (value)
        except:
            return value

    def format_date(value):
        if value is None:
            return ""
        
        if type(value) == int:
            value = datetime.datetime.fromtimestamp(value)
            return value.strftime("%Y-%m-%d")
        
        try:
            return value.strftime("%Y-%m-%d")
        except:
            return ""

    def format_datetime(value):
        if value is None:
            return ""
        
        if type(value) == int:
            value = datetime.datetime.fromtimestamp(value)
            s = value.strftime("%Y-%m-%d %I:%M %p")
            #s = s.replace(" ", "&nbsp;")
            #print("s: '%s'", s)
            return s
        
        try:
            return value.strftime("%Y-%m-%d")
        except:
            return ""



    def format_title(value):
        if type(value) == str:
            value = value.replace("_", " ")
            return value.title()
        else:
            return value

    def format(self, col_name, value):

        if col_name not in self.formats.keys():
            return value
        fmt = self.formats[col_name]
        if fmt == "percent":
            return "%s %0.2f" % ("%", value)
        elif fmt == "int":
            return GenericDataframeTableCellFormatter.format_int(value)
        elif fmt == "date":
            value = GenericDataframeTableCellFormatter.format_date(value)
        elif fmt == "datetime":
            value = GenericDataframeTableCellFormatter.format_datetime(value)
        elif fmt == "title":
            value = GenericDataframeTableCellFormatter.format_title(value)
        return value
