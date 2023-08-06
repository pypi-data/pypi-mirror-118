"""
The list of ingredient choices is quite large, so this module provides lazy loaded widgets which help 
reducing loading times.
"""

from django import forms


class LazyWidget():
    """ 
    Base class for lazy loaded, choice based widgets.

    offloads option generation to the client, relies on correct endpoint setup.

    """
    
    template_name="dj_ingredient_field/lazy_choice.html"

    def __init__(self, lazy_endpoint, attrs=None):
        """ Creates a new LazyWidget

            Args:
                lazy_endpoint (str): the relative or absolute url which retrieves json choices (corresponding to the underlying choices) in the following format: { values: [...[<db value>, <user readable value>]...]}
                attrs: the attributes to pass down to the widget html. Defaults to None.
        """

        # lazy endpoint should provide all of the option values as json
        self.lazy_endpoint = lazy_endpoint

        if attrs == None:
            attrs = {}
        
        attrs.update({
            "lazy_url": lazy_endpoint
        })

        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['value'] = value
        context['widget']['checked_attribute'] = list(self.checked_attribute.keys())[0] 
        context['widget']['allow_multiple_selected'] = self.allow_multiple_selected 
        return context

    class Media:
        js = ('dj_ingredient_field/js/lazy_dropdown.js',)

class LazySelectWidget(LazyWidget,forms.widgets.Select):
    """ 
        Single option selection widget corresponding exactly to `Select` from django widgets.
        Example usage (requires dj_ingredient_field.urls to be included into your urls somewhere)::

            from django import forms
            from dj_ingredient_field.widgets import LazySelectWidget
            from django.urls import reverse_lazy

            class IngredientQuantityAdminForm(forms.ModelForm):
                class Meta:
                    model = IngredientQuantity
                    widgets = {
                        'ingredient': LazySelectWidget(reverse_lazy('dj_ingredient_field:ingredients'))
                    }
                    fields = '__all__' # required for Django 3.x

    """
    pass

class LazySelectMultipleWidget(LazyWidget,forms.widgets.SelectMultiple):
    """
    WIP
    """
    pass