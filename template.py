import string

def escape(s):
    return s.template if isinstance(s, T) else s.replace('{', '{{').replace('}', '}}')

class Variable(object):
    def __init__(self, name):
        self.name = name

    def __getattr__(self, attr):
        return Variable(self.name + '.' + attr)

    def __getitem__(self, item):
        return Variable('{}[{}]'.format(self.name, item))

class PartialFormatter(string.Formatter):
    def parse(self, format_string):
        return ((escape(literal_text), field_name, format_spec, conversion)
                for literal_text, field_name, format_spec, conversion in
                super(PartialFormatter, self).parse(format_string))

    def vformat(self, format_string, args, kwargs):
        return super(PartialFormatter, self).vformat(
            format_string, iter(args), kwargs.copy())

    def get_value(self, key, args, kwargs):
        if key == '':
            return next(args)
        else:
            return kwargs.setdefault(key, Variable(key))

    def convert_field(self, value, conversion):
        if isinstance(value, Variable) and conversion is not None:
            return Variable(value.name + '!' + conversion)
        return super(PartialFormatter, self).convert_field(value, conversion)

    def format_field(self, value, format_spec):
        if isinstance(value, T):
            assert format_spec == ''
            return value.template
        elif isinstance(value, Variable):
            return '{{{}{}}}'.format(value.name, format_spec and ':' + format_spec)
        else:
            return escape(format(value, format_spec))

    def free(self, format_string):
        d = {}
        super(PartialFormatter, self).vformat(format_string, iter([]), d)
        return d.iterkeys()

formatter = PartialFormatter()

class T(object):
    def __init__(self, template):
        self.template = template

    def free(self):
        return formatter.free(self.template)

    def format(self, *args, **kwargs):
        return T(formatter.vformat(self.template, args, kwargs))

    def close(self):
        return self.template.format()

    def join(self, others):
        return T(self.template.join(map(escape, others)))

    def __add__(self, other):
        return T(self.template + escape(other))

    def __radd__(self, other):
        return T(escape(other) + self.template)

    def __str__(self):
        raise TypeError('cannot convert T to str')

    def __repr__(self):
        return 'T({!r})'.format(self.template)
