from django.urls import path
from .views import SummaryView, RecentActivityView, MachineStatusView, MachinesPerClientView, ServiceActivityView, InventoryOverviewView
urlpatterns = [path('dashboard/summary/', SummaryView.as_view()), path('dashboard/recent-activity/', RecentActivityView.as_view()), path('analytics/machine-status/', MachineStatusView.as_view()), path('analytics/machines-per-client/', MachinesPerClientView.as_view()), path('analytics/service-activity/', ServiceActivityView.as_view()), path('analytics/inventory-overview/', InventoryOverviewView.as_view())]
