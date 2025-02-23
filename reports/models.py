from django.db import models
from assets.models import Property
# models do app reports

class Report(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    @classmethod
    def generate_asset_summary(cls):
        """Create a summary report of all assets"""
        content = f"Total Assets: {Property.objects.count()}\n"
        content += f"Assets in Maintenance: {Property.objects.filter(maintenance__status='In Maintenance').count()}"
        report = cls.objects.create(
            title="Asset Summary Report",
            content=content
        )
        return report