from django.urls import path

from . import views


app_name = 'calculator'

urlpatterns = [
    path('', views.index, name='index'),
    path('new_calculation/', views.ProposalCreateView.as_view(), name='create'),
    path('new_calculation/result/', views.TradeFeeCalculationView.as_view(), name='result'),
    path('history/', views.ProposalHistoryView.as_view(), name='proposal_history'),
    path('generate-file/', views.generate_and_download_file, name='generate_file'),
]
