from django import forms
from .models import personaldetails,Additional,otsdata,Dataupload,SMSDetails

class personalForm(forms.ModelForm):
    class Meta:
        model = personaldetails
        fields = '__all__'

class additionalForm(forms.ModelForm):
    class Meta:
        model = Additional
        fields = '__all__'

class otsdataForm(forms.ModelForm):
    class Meta:
        model = otsdata
        fields = '__all__'


class DataUploadForm(forms.ModelForm):
    campion = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
    listid = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
    listname = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
    files = forms.FileField(max_length=200,widget=forms.FileInput(attrs={'class':'form-control'}))

    class Meta:
        model = Dataupload
        fields = '__all__'
class SmsUploadForm(forms.ModelForm):
      class Meta:
        model = SMSDetails
        fields = '__all__'