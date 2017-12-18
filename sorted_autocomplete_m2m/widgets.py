from itertools import chain
from django import forms
from django.urls import reverse_lazy
from django.forms import Media
from django.template import Context
from django.template.loader import get_template
from django.utils.encoding import force_text
from django.utils.html import conditional_escape
from sortedm2m.forms import SortedMultipleChoiceField, SortedCheckboxSelectMultiple

__author__ = 'snake'


class SuperSortWidget(SortedCheckboxSelectMultiple):
    class Media:
        js = (
            'sortedm2m/jquery-ui.js',
            'sorted-autocomplete-m2m/js/m2m.js',
        )
        css = {'screen': (
            'sortedm2m/widget.css',
            'sorted-autocomplete-m2m/css/m2m.css',
        )}

    def __init__(self, url_name, **kwargs):
        super().__init__(**kwargs)
        self.autocomplete_url = reverse_lazy(url_name)

    def filter_unselected_choices(self, value):
        if value is None:
            self.choices.queryset = self.choices.queryset.none()
        else:
            self.choices.queryset = self.choices.queryset.filter(pk__in=value)

    def render(self, name, value, attrs=None, choices=()):
        self.filter_unselected_choices(value)
        selected, unselected = self._render(name, value, attrs, choices)
        return get_template('sorted-autocomplete-m2m/m2m.html').render({
            'autocomplete_id': '%s_autocomplete' % attrs['id'],
            'autocomplete_url': self.autocomplete_url,
            'selected': selected,
            'unselected': unselected,
            'name': name,
        })

    @property
    def media(self):
        definition = getattr(self, 'Media', None)
        if definition:
            return Media(definition)
        return Media()

    def _render(self, name, value, attrs=None, choices=()):
        """
        Fork of original render() that returns lists selected, unselected
        instead of a rendered response.
        """
        if value is None:
            value = ()
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)

        # Normalize to strings
        str_values = [force_text(v) for v in value]

        selected = []
        unselected = []

        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = ' for="%s"' % conditional_escape(final_attrs['id'])
            else:
                label_for = ''

            cb = forms.CheckboxInput(final_attrs, check_test=lambda v: v in str_values)
            option_value = force_text(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_text(option_label))
            item = {'label_for': label_for, 'rendered_cb': rendered_cb, 'option_label': option_label,
                    'option_value': option_value}
            if option_value in str_values:
                selected.append(item)
            else:
                unselected.append(item)

        ordered = []
        for value in str_values:
            for select in selected:
                if value == select['option_value']:
                    ordered.append(select)
        selected = ordered
        return selected, unselected


class SuperSortField(SortedMultipleChoiceField):
    widget = SuperSortWidget