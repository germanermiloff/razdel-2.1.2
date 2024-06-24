import os
from math import ceil

from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, ListView
from django.urls import reverse_lazy
from django.http import HttpResponse

from .models import Proposal, RateType
from .forms import ProposalForm
from .constants import LOWER_BOUND, UPPER_BOUND


def index(request):
    template = 'calculator/index.html'
    return render(request, template)


class ProposalCreateView(CreateView):
    model = Proposal
    form_class = ProposalForm
    template_name = 'calculator/new_calculation.html'
    success_url = reverse_lazy('calculator:result')

    def form_valid(self, form):
        proposal = form.save(commit=False)

        income = form.cleaned_data['inc_per_quartal']

        selected_year = form.cleaned_data['year']
        deflator = selected_year.deflator

        limit_1 = LOWER_BOUND * deflator
        limit_2 = UPPER_BOUND * deflator

        if income < limit_1:
            proposal.tax_rate = RateType.objects.get(rate_id=1)
        elif limit_1 < income < limit_2:
            proposal.tax_rate = RateType.objects.get(rate_id=2)

        tax_amount = ceil(proposal.inc_per_quartal * proposal.tax_rate.rate)
        insurance_premium = proposal.ins_prem
        trade_fee_paid = proposal.trade_fee_paid

        trade_fee = min(tax_amount - insurance_premium, trade_fee_paid)
        
        proposal.tax_amount = tax_amount
        proposal.trade_fee = trade_fee

        proposal.save()
        return redirect(self.success_url)


class TradeFeeCalculationView(TemplateView):
    template_name = 'calculator/result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        last_proposal = Proposal.objects.latest('id')

        tax_amount = last_proposal.tax_amount
        insurance_premium = last_proposal.ins_prem
        trade_fee_paid = last_proposal.trade_fee_paid
        trade_fee = last_proposal.trade_fee

        context = {
            'tax_amount': tax_amount,
            'insurance_premium': insurance_premium,
            'trade_fee_paid': trade_fee_paid,
            'trade_fee': trade_fee
        }
        return context


class ProposalHistoryView(ListView):
    model = Proposal
    template_name = 'calculator/proposal_history.html'
    context_object_name = 'proposals'
    paginate_by = 10


def generate_and_download_file(request):
    try:
        last_proposal = Proposal.objects.latest('id')

        data = {    
            'ИНН': last_proposal.INN,
            'Доход за квартал': last_proposal.inc_per_quartal,
            'Страховые взносы': last_proposal.ins_prem,
            'Фактически уплаченная сумма торгового сбора': last_proposal.trade_fee_paid,
            'Сумма уплаченного торгового сбора': last_proposal.trade_fee,
            'Год': last_proposal.year.year_id,
            'Ставка по налогу': last_proposal.tax_rate.rate,
            'Сумма исчисленного налога': last_proposal.tax_amount,
        }
        # Определяем путь к файлу template.txt
        template_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template.txt')

        # Открываем файл шаблона и считываем его содержимое
        with open(template_file_path, 'r') as template_file:
            template_content = template_file.read()

        # Заменяем заполнители в шаблоне на данные
        filled_content = template_content.format(**data)

        response = HttpResponse(filled_content, content_type='application/txt')

        response['Content-Disposition'] = 'attachment; filename="filled_proposal.txt"'

        return response

    except Proposal.DoesNotExist:
        return HttpResponse("Ошибка: Объект Proposal не найден")
