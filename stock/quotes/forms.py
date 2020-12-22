# Create a form for stock portfolio

# import forms system for django
from django import forms
from .models import Stock
from .models import ChartStock
# create class for stock form
class StockForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ["ticker"] # python list
class ChartForm(forms.ModelForm):
    class Meta:
        model=ChartStock
        fields=['ticker']
