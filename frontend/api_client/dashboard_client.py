from .base_client import APIClient
class DashboardClient(APIClient):
    def summary(self): return self.get('dashboard/summary/')
    def recent_activity(self): return self.get('dashboard/recent-activity/')
    def analytics(self, name): return self.get(f'analytics/{name}/')
