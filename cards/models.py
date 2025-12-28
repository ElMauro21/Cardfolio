from django.db import models

# Create your models here.

class Card(models.Model):
    name = models.CharField(max_length=255)
    scryfall_id = models.CharField(max_length=50, unique=True)
    set_code = models.CharField(max_length=10)
    set_name = models.CharField(max_length=100)
    rarity = models.CharField(max_length=50)
    collector_number = models.CharField(max_length=20)
    finish = models.CharField(
        max_length=20,
        choices=[("nonfoil", "Non-Foil"), ("foil", "Foil")]
    )
    image_url = models.URLField()
    price_usd = models.DecimalField(
        max_digits=10,decimal_places=2,null=True,blank=True
    )
    price_eur = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.set_code})"