import string

formatter = string.Formatter()


class Dummy(object):
    def __getattr__(self, attr):
        return self

    def __getitem__(self, item):
        return self


dummy = Dummy()


class Template(object):
    """Abstract base class for lazy string templates.

    A template is a symbolic string with interpolated free variables;
    for example, the template T("lambda {args}: {body}") has free
    variables {"args", "body"}, and can be rendered in the environment
    {"args": "x", "body": "x + x"} to produce "lambda x: x + x".  Free
    variables may be positional or named.  Templates may be
    concatenated with other templates, or formatted with other
    templates as arguments, producing a new template.

    Derived classes must provide free_count (a dict counting the
    number of occurrences of each free variable) and render_parts.
    """

    def free(self):
        """Return the set of free variables in this template."""

        return set(self.free_count)

    def render_parts(self, args, kwargs, auto_arg_index):
        """Render this template in an environment containing non-template
        values for all of its free variables.

        The output is a sequence of parts, each of which is either a
        string to be appended to the output, or a tuple (template,
        args, kwargs, auto_arg_index) representing a recursive call to
        render.
        """

        raise NotImplementedError

    def render_string(self, args, kwargs, auto_arg_index):
        """Render this template in an environment containing non-template
        values for all of its free variables as a string.
        """

        out = []
        stack = [iter(self.render_parts(args, kwargs, auto_arg_index))]
        while stack:
            for item in stack[-1]:
                if isinstance(item, tuple):
                    stack.append(iter(item[0].render_parts(*item[1:])))
                    break
                else:
                    out.append(item)
            else:
                stack.pop()
        return "".join(out)

    def close(self):
        """Render this template as a string, assuming it has no free
        variables."""

        return self.render_string([], {}, 0)

    def format(self, *args, **kwargs):
        """Specialize this template by providing values (which may be
        templates) for some or all of its free variables, producing a
        new template.

        For example, T("{a} + {b}").format(b=T("{c} + {d}")) is a
        template behaving like T("{a} + {c} + {d}").

        Warning: providing multiple values that are templates with
        automatic positional variables, as in
            T("{a} {a}").format(a=T("{}"))
            T("{a} {b}").format(a=T("{}"), b=T("{}"))
        may lead to counterintuitive (read: wrong) results.
        """

        return Format(self, args, kwargs, 0)

    def join(self, others):
        """Concatenate others (which may be templates), separated by this
        template.
        """

        args = []
        first = True
        for other in others:
            if first:
                first = False
            else:
                args.append(self)
            args.append(other)
        return Concat(args)

    def __add__(self, other):
        """Concatenate on the left with another value (which may be a
        template).
        """

        return Concat([self, other])

    def __radd__(self, other):
        """Concatenate on the right with another value (which may be a
        template)."""

        return Concat([other, self])

    def __str__(self):
        raise TypeError("cannot convert Template to str")


class T(Template):
    """A template constructed from a PEP 3101 style format string."""

    def __init__(self, template_str):
        self.template_str = template_str
        self.free_count = {}
        for literal_text, field_name, format_spec, conversion in formatter.parse(
            self.template_str
        ):
            if field_name is not None:
                obj, arg_used = formatter.get_field(field_name, dummy, dummy)
                self.free_count[arg_used] = self.free_count.get(arg_used, 0) + 1
                if format_spec:
                    format_spec_t = T(format_spec)
                    for key, count in format_spec_t.free_count.items():
                        self.free_count[key] = self.free_count.get(key, 0) + count

    def render_parts(self, args, kwargs, auto_arg_index):
        out = []
        for literal_text, field_name, format_spec, conversion in formatter.parse(
            self.template_str
        ):
            if literal_text:
                out.append(literal_text)
            if field_name is not None:
                if field_name == "":
                    obj = args[auto_arg_index]
                    auto_arg_index += 1
                else:
                    obj, arg_used = formatter.get_field(field_name, args, kwargs)
                if (conversion or format_spec) and isinstance(obj, Template):
                    obj = obj.render_string(args, kwargs, auto_arg_index)
                    auto_arg_index += obj.free_count.get("", 0)
                if isinstance(obj, Template):
                    out.append((obj, args, kwargs, auto_arg_index))
                    auto_arg_index += obj.free_count.get("", 0)
                else:
                    obj = formatter.convert_field(obj, conversion)
                    if format_spec:
                        format_spec_t = T(format_spec)
                        format_spec = format_spec_t.render_string(
                            args, kwargs, auto_arg_index
                        )
                        auto_arg_index += format_spec_t.free_count.get("", 0)
                    out.append(formatter.format_field(obj, format_spec))
        return out

    def __repr__(self):
        return "T(%r)" % (self.template_str,)


class Format(Template):
    """A template constructed by calling .format() on another template."""

    def __init__(self, template, args, kwargs, auto_arg_index):
        self.template = template
        self.args = args
        self.kwargs = kwargs
        self.auto_arg_index = auto_arg_index
        self.free_count = {}
        for key, count in self.template.free_count.items():
            if key == "":
                for i in range(auto_arg_index, auto_arg_index + count):
                    if isinstance(args[i], Template):
                        for key1, count1 in args[i].free_count.items():
                            self.free_count[key1] = (
                                self.free_count.get(key1, 0) + count1
                            )
            elif isinstance(key, (int, long)):
                if isinstance(args[key], Template):
                    for key1, count1 in args[key].free_count.items():
                        self.free_count[key1] = (
                            self.free_count.get(key1, 0) + count * count1
                        )
            elif key in kwargs:
                if isinstance(kwargs[key], Template):
                    for key1, count1 in kwargs[key].free_count.items():
                        self.free_count[key1] = (
                            self.free_count.get(key1, 0) + count * count1
                        )
            else:
                self.free_count[key] = self.free_count.get(key, 0) + count

    def render_parts(self, args, kwargs, auto_arg_index):
        formatted_args = [
            Format(arg, args, kwargs, auto_arg_index)
            if isinstance(arg, Template)
            else arg
            for arg in self.args
        ]
        formatted_kwargs = kwargs.copy()
        formatted_kwargs.update(
            (
                key,
                Format(arg, args, kwargs, auto_arg_index)
                if isinstance(arg, Template)
                else arg,
            )
            for key, arg in self.kwargs.items()
        )
        return [(self.template, formatted_args, formatted_kwargs, self.auto_arg_index)]

    def __repr__(self):
        return "Format(%r, %r, %r, %r)" % (
            self.template,
            self.args,
            self.kwargs,
            self.auto_arg_index,
        )


class Concat(Template):
    """A template constructed by concatenating a sequence of templates."""

    def __init__(self, ts):
        self.ts = ts
        self.free_count = {}
        for t in ts:
            if isinstance(t, Template):
                for key, count in t.free_count.items():
                    self.free_count[key] = self.free_count.get(key, 0) + count

    def render_parts(self, args, kwargs, auto_arg_index):
        out = []
        for t in self.ts:
            if isinstance(t, Template):
                out.append((t, args, kwargs, auto_arg_index))
                auto_arg_index += t.free_count.get("", 0)
            else:
                out.append(t)
        return out

    def __repr__(self):
        return "Concat(%r)" % (self.ts,)
