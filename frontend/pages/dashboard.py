from api_client.dashboard_client import DashboardClient
def load_dashboard(token): return DashboardClient(token).summary()
