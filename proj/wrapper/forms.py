from django import forms

class OurForm(forms.Form):
    x = forms.CharField(label='charfield name', max_length=100)