from django.db import models


class Organization(models.Model):
    """
    Socle transverse — Business Architecture Chapitre 6.2.
    Prépare le multi-tenant (P8, différé) sans l'activer : une seule
    instance existe pour le MVP, mais toutes les autres entités y sont
    déjà rattachées via ForeignKey, garantissant une migration future
    sans réécriture (Architecture Vision, conformité P8).
    """

    name = models.CharField(max_length=200)
    country = models.CharField(max_length=2, default="TG")  # ISO 3166-1 alpha-2
    timezone = models.CharField(max_length=50, default="Africa/Lome")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Organisation"
        verbose_name_plural = "Organisations"

    def __str__(self):
        return self.name
