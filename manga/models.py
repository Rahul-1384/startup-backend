from django.db import models
from django.conf import settings

class Manga(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to="manga_covers/")
    pdf_file = models.FileField(upload_to="manga_pdfs/", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="uploaded_mangas")

    def is_free(self):
        return self.price == 0.00

    def __str__(self):
        return self.title

class Review(models.Model):
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # 1 to 5 stars
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.manga.title} ({self.rating}/5)"
