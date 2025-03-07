from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class MOU(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    pdf_url = models.URLField()
    signature_url = models.URLField()
    start_date = models.DateField()
    end_date = models.DateField()
    renewal_score = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('expired', 'Expired')])

class Clause(models.Model):
    mou = models.ForeignKey(MOU, on_delete=models.CASCADE, related_name="clauses")
    clause_text = models.TextField()
    clause_type = models.CharField(max_length=50)
    risk_level = models.CharField(max_length=10, choices=[('low', 'Low'), ('high', 'High')])
