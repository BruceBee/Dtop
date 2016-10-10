from django.forms import ModelForm
from models import *

class DnsForm(ModelForm):
	class Meta:
		model = DnsInfo
		fields = '__all__'