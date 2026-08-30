from api_client.dashboard_client import DashboardClient
def load_analytics(token, name): return DashboardClient(token).analytics(name)
