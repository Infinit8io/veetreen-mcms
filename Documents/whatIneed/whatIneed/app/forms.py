from django.forms import ModelForm, TextInput, Textarea, inlineformset_factory, DateTimeInput, NumberInput, \
    ModelChoiceField, DateTimeField

from app.models import Event, Item, UserBringItem


class EventForm(ModelForm):
    date_time = DateTimeField(
        widget=DateTimeInput(attrs={'type': "datetime-local"}),
        input_formats=[
            '%Y-%m-%dT%H:%M'
        ]
    )

    class Meta:
        model = Event
        fields = (
            "name",
            "date_time",
            "description",
            "address"
        )
        widgets = {
            'name': TextInput(attrs={'placeholder': "Barbecue on the roof"}),
            'description': Textarea(attrs={'placeholder': "The best barbecue of the year is back again!"}),
            'address': TextInput(attrs={'placeholder': "Type the address"}),
        }


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = (
            "name",
            "qty",
            "unit",
            "category"
        )
        widgets = {
            'name': TextInput(attrs={'placeholder': "Name"}),
            'qty': NumberInput(attrs={'placeholder': "Qty to bring", "step": "0.5"}),
            'unit': TextInput(attrs={'placeholder': "unit (ex. bottles)"})
        }


ItemFormSet = inlineformset_factory(
    model=Item,
    parent_model=Event,
    form=ItemForm,
    extra=1
)
