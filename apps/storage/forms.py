from django.forms.models import ModelForm
from apps.storage.models import FileStorage

class FileStorageForm(ModelForm):

    class Meta:
        model = FileStorage
        fields = ('name', 'file')
