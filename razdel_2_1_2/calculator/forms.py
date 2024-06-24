from django.forms import ModelForm, TextInput, ModelChoiceField

from .models import Proposal, Deflator


class ProposalForm(ModelForm):
    year = ModelChoiceField(
        queryset=Deflator.objects.all(),
        label='Год',
        empty_label=None,
        to_field_name='year_id'
    )

    class Meta:
        model = Proposal
        fields = ['INN', 'inc_per_quartal', 'ins_prem', 'trade_fee_paid', 'year']
        widgets = {
            'INN': TextInput(attrs={'type': 'number'})
        }
