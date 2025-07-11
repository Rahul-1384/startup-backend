from django.db import models
from account.models import User  # Assuming your User model is in 'account' app
from django.core.exceptions import PermissionDenied

class UploadBook(models.Model):
    class ConditionChoices(models.TextChoices):
        GOOD = 'Good'
        BETTER = 'Better'
        BEST = 'Best'
    
    class CategoryChoices(models.TextChoices):
        CLASS_4_8 = 'Class 4-8'
        CLASS_9_12 = 'Class 9-12'
        REFERENCE_BOOK = 'Reference Book'
        CHILDREN_BOOK = 'Children Book'
        COMPETITION_BOOK = 'Competition Book'
        OTHER = 'Other'
    
    class SubjectChoices(models.TextChoices):
        SCIENCE = 'Science'
        COMMERCE = 'Commerce'
        HUMANITIES = 'Humanities'
        MATHEMATICS = 'Mathematics'
        ENGLISH = 'English'
        HINDI = 'Hindi'
        OTHER = 'Other'
    
    class CompetitiveExamChoices(models.TextChoices):
        NEET = 'NEET'
        JEE = 'JEE'
        AIIMS = 'AIIMS'
        UPSC = 'UPSC'
        SSC = 'SSC'
        GATE = 'GATE'
        CAT = 'CAT'
        OTHER = 'Other'
    
    class BoardsChoices(models.TextChoices):
        CBSE = 'CBSE'
        ICSE = 'ICSE'
        ISC = 'ISC'
        OTHER = 'Other'
    
    class LanguageChoices(models.TextChoices):
        ENGLISH = 'English'
        HINDI = 'Hindi'
        OTHER = 'Other'
    
    class Status(models.TextChoices):
        PENDING = 'Pending'
        APPROVED = 'Approved'
        REJECTED = 'Rejected'
        SOLD = 'Sold'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_books')  # Linking to the User model
    book_title = models.CharField(max_length=255)
    book_author = models.CharField(max_length=255)
    book_description = models.TextField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(
        max_length=10,
        choices=ConditionChoices.choices,
        default=ConditionChoices.GOOD
    )
    category = models.CharField(
        max_length=20,
        choices=CategoryChoices.choices,
        default=CategoryChoices.OTHER
    )
    subject = models.CharField(
        max_length=20,
        choices=SubjectChoices.choices,
        default=SubjectChoices.OTHER
    )
    competitive_exam = models.CharField(
        max_length=20,
        choices=CompetitiveExamChoices.choices,
        default=CompetitiveExamChoices.OTHER
    )
    boards = models.CharField(
        max_length=20,
        choices=BoardsChoices.choices,
        default=BoardsChoices.OTHER
    )
    language = models.CharField(
        max_length=20,
        choices=LanguageChoices.choices,
        default=LanguageChoices.OTHER
    )
    book_images = models.ImageField(upload_to='book_images/', null=True, blank=True)
    
    # Admin-only fields
    final_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    admin_notes = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.book_title} by {self.book_author}"
    
    def save(self, *args, **kwargs):
        # If you have access to the request object, you can check if user is admin
        # This would need to be passed in from the view
        user = kwargs.pop('user', None)
        if user and not user.is_staff:
            # Store the original values
            if self.pk:
                original = UploadBook.objects.get(pk=self.pk)
                # If a non-admin is trying to change admin-only fields, revert them
                if original.final_price != self.final_price or original.discount != self.discount:
                    self.final_price = original.final_price
                    self.discount = original.discount
        
        super().save(*args, **kwargs)