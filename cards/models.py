from django.db import models

# Create your models here.

class Card(models.Model):
    FINISH_CHOICES = [
        ("foil", "Foil"),
        ("nonfoil", "Non-Foil"),
    ]
    name = models.CharField(max_length=255)
    scryfall_id = models.CharField(max_length=50)
    finish = models.CharField(
        max_length=10,
        choices=FINISH_CHOICES
    )
    set_code = models.CharField(max_length=10)
    set_name = models.CharField(max_length=100)
    rarity = models.CharField(max_length=50)
    collector_number = models.CharField(max_length=20)
    image_url = models.URLField()
    price_usd = models.DecimalField(
        max_digits=10,decimal_places=2,null=True,blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["scryfall_id", "finish"],
                name="unique_card_printing"
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.set_code})"