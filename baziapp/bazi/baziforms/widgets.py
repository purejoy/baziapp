# -*- coding: utf-8 -*-
from django.forms.util import flatatt
from django.forms.widgets import DateTimeInput, Select, Widget
from django.utils import translation
from django.utils.safestring import mark_safe
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode
from itertools import chain

try:
    import json
except ImportError:
    from django.utils import simplejson as json
try:
    from django.utils.encoding import force_unicode as force_text
except ImportError:  # python3
    from django.utils.encoding import force_text

class SelectPicker(Widget):
    allow_multiple_selected = False

    html_template = '''
        <div%(div_attrs)s>
            &nbsp;&nbsp;&nbsp;&nbsp
            <span class="selectpicker">
              <span%(icon_attrs)s></span>
            </span>
            &nbsp;&nbsp
        '''

    js_template = '''
        <script type="text/javascript">
            $(function(){$("#%(picker_id)s").selectpicker(%(options)s);});
        </script>
        '''

    def __init__(self, attrs=None, choices=(), options=None, div_attrs=None, icon_attrs=None):
        if not icon_attrs:
            icon_attrs = {'class': 'glyphicon glyphicon-calendar'}
        if not div_attrs:
            div_attrs = {'class': 'input-group select'}
        super(SelectPicker, self).__init__(attrs)
        # choices can be any iterable, but we may need to render this widget
        # multiple times. Thus, collapse it into a list so it can be consumed
        # more than once.
        self.choices = list(choices)
        if 'id' not in attrs:
            self.attrs['id'] = 'selectpicker1'     
        self.div_attrs = div_attrs and div_attrs.copy() or {}
        self.icon_attrs = icon_attrs and icon_attrs.copy() or {}
        if options == False:  # datetimepicker will not be initalized only when options is False
            self.options = False
        else:
            self.options = options and options.copy() or {}


    def render(self, name, value, attrs=None, choices=()):

        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<select%s>' % flatatt(final_attrs)]
        options = self.render_options(choices, [value])
        if options:
            output.append(options)
        output.append(u'</select>')
        output.append(u'</div>')
        
        picker_id = conditional_escape(self.attrs['id'])
        div_attrs = dict([(key, conditional_escape(val)) for key, val in self.div_attrs.items()])  # python2.6 compatible
        icon_attrs = dict([(key, conditional_escape(val)) for key, val in self.icon_attrs.items()])
        html = self.html_template % dict(div_attrs=flatatt(div_attrs),
                                         icon_attrs=flatatt(icon_attrs))

        html += u'\n'.join(output)
        if self.options:
            #self.options['language'] = translation.get_language()
            js = self.js_template % dict(picker_id=picker_id,
                                         options=json.dumps(self.options or {}))
        else:
            js = ''

        #return mark_safe(u'\n'.join(output))
        return mark_safe(force_text(html + js))
        

    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_unicode(option_value)
        if option_value in selected_choices:
            selected_html = u' selected="selected"'
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''

        strtmp = escape(option_value)

        if strtmp not in self.icon_attrs:
            opt_icon = ""
        else:
            opt_icon = self.icon_attrs[strtmp]
            
        return u'<option data-icon="%s" value="%s"%s>%s</option>' % (
            escape(opt_icon),escape(option_value), selected_html,
            conditional_escape(force_unicode(option_label)))

    def render_options(self, choices, selected_choices):
        # Normalize to strings.
        selected_choices = set(force_unicode(v) for v in selected_choices)
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(u'<optgroup label="%s">' % escape(force_unicode(option_value)))
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
                output.append(u'</optgroup>')
            else:
                output.append(self.render_option(selected_choices, option_value, option_label))
        return u'\n'.join(output)
    
    

    


class DateTimePicker(DateTimeInput):
    class Media:
        class JsFiles(object):
            def __iter__(self):
                #yield 'bootstrap3_datetime/js/moment.min.js'
                #yield 'bootstrap3_datetime/js/bootstrap-datetimepicker.min.js'
                lang = translation.get_language()
                if lang:
                    lang = lang.lower()
                    #There is language name that length>2 *or* contains uppercase.
                    lang_map = {
                        'ar-ma': 'ar-ma',
                        'en-au': 'en-au',
                        'en-ca': 'en-ca',
                        'en-gb': 'en-gb',
                        'en-us': 'en-us',
                        'fa-ir': 'fa-ir',
                        'fr-ca': 'fr-ca',
                        'ms-my': 'ms-my',
                        'pt-br': 'bt-BR',
                        'rs-latin': 'rs-latin',
                        'tzm-la': 'tzm-la',
                        'tzm': 'tzm',
                        'zh-cn': 'zh-CN',
                        'zh-tw': 'zh-TW',
                        'zh-hk': 'zh-TW',
                    }
                    if len(lang) > 2:
                        lang = lang_map.get(lang, 'en-us')
                    if lang not in ('en', 'en-us'):
                        yield 'bootstrap3_datetime/js/locales/bootstrap-datetimepicker.%s.js' % (lang)

        #js = JsFiles()
        css = {'': ('css/glyphicons.css',),}

    # http://momentjs.com/docs/#/parsing/string-format/
    # http://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
    format_map = (('DDD', r'%j'),
                  ('DD', r'%d'),
                  ('MMMM', r'%B'),
                  ('MMM', r'%b'),
                  ('MM', r'%m'),
                  ('YYYY', r'%Y'),
                  ('YY', r'%y'),
                  ('HH', r'%H'),
                  ('hh', r'%I'),
                  ('mm', r'%M'),
                  ('ss', r'%S'),
                  ('a', r'%p'),
                  ('ZZ', r'%z'),
    )

    @classmethod
    def conv_datetime_format_py2js(cls, format):
        for js, py in cls.format_map:
            format = format.replace(py, js)
        return format

    @classmethod
    def conv_datetime_format_js2py(cls, format):
        for js, py in cls.format_map:
            format = format.replace(js, py)
        return format

    html_template = '''
        <div%(div_attrs)s>
            <span class="input-group-addon">
                <span%(icon_attrs)s></span>
            </span>
            <input%(input_attrs)s/>
        </div>'''

    js_template = '''
        <script type="text/javascript">
            $(function(){$("#%(picker_id)s").datetimepicker(%(options)s);});
        </script>
        '''

    def __init__(self, attrs=None, format=None, options=None, div_attrs=None, icon_attrs=None):
        if not icon_attrs:
            icon_attrs = {'class': 'glyphicon glyphicon-calendar'}
        if not div_attrs:
            div_attrs = {'class': 'input-group date'}
        if format is None and options and options.get('format'):
            format = self.conv_datetime_format_js2py(options.get('format'))
        super(DateTimePicker, self).__init__(attrs, format)
        if 'class' not in self.attrs:
            self.attrs['class'] = 'form-control'
        self.div_attrs = div_attrs and div_attrs.copy() or {}
        self.icon_attrs = icon_attrs and icon_attrs.copy() or {}
        self.picker_id = self.div_attrs.get('id') or None
        if options == False:  # datetimepicker will not be initalized only when options is False
            self.options = False
        else:
            self.options = options and options.copy() or {}
            if format and not self.options.get('format') and not self.attrs.get('date-format'):
                self.options['format'] = self.conv_datetime_format_py2js(format)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        input_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            input_attrs['value'] = force_text(self._format_value(value))
        input_attrs = dict([(key, conditional_escape(val)) for key, val in input_attrs.items()])  # python2.6 compatible
        if not self.picker_id:
             self.picker_id = (input_attrs.get('id', '') +
                               '_pickers').replace(' ', '_')
        self.div_attrs['id'] = self.picker_id
        picker_id = conditional_escape(self.picker_id)
        div_attrs = dict(
            [(key, conditional_escape(val)) for key, val in self.div_attrs.items()])  # python2.6 compatible
        icon_attrs = dict([(key, conditional_escape(val)) for key, val in self.icon_attrs.items()])
        html = self.html_template % dict(div_attrs=flatatt(div_attrs),
                                         input_attrs=flatatt(input_attrs),
                                         icon_attrs=flatatt(icon_attrs))
        if self.options:
            #self.options['language'] = translation.get_language()
            js = self.js_template % dict(picker_id=picker_id,
                                         options=json.dumps(self.options or {}))
        else:
            js = ''
        return mark_safe(force_text(html + js))
