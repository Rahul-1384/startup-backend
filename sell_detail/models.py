from django.db import models
from django.utils.timezone import now
from account.models import User
import uuid

class ActiveSellDetailManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class SellDetail(models.Model):
    class ConditionChoices(models.TextChoices):
       BEST = 'best', 'Best'
       BETTER = 'better', 'Better'
       GOOD = 'good', 'Good'

    class CategoryChoices(models.TextChoices):
        CLASS_4_8 = 'class_4_8', 'Class 4-8'
        CLASS_9_12 = 'class_9_12', 'Class 9-12'
        REFERENCE = 'reference', 'Reference'
        COMPETITIVE = 'competitive', 'Competitive'
        CHILDRENS_BOOK = "childrens_book", "Children's Book"

    class BoardChoices(models.TextChoices):
        CBSE = 'CBSE', 'CBSE'
        ICSE = 'ICSE', 'ICSE'
        UP = 'UP', 'UP'

    class SubjectChoices(models.TextChoices):
        MATHS = 'Maths', 'Maths'
        ENGLISH = 'English', 'English'
        PHYSICS = 'Physics', 'Physics'
        CHEMISTRY = 'Chemistry', 'Chemistry'
        BIOLOGY = 'Biology', 'Biology'
        HISTORY = 'History', 'History'
        GEOGRAPHY = 'Geography', 'Geography'
        POLITICAL_SCIENCE = 'Political Science', 'Political Science'
        ECONOMICS = 'Economics', 'Economics'
        CIVICS = 'Civics', 'Civics'
        HINDI = 'Hindi', 'Hindi'
        BUSINESS_STUDY = 'Business Study', 'Business Study'
        SANSKRIT = 'Sanskrit', 'Sanskrit'
        ACCOUNTS = 'Accounts', 'Accounts'
        OTHERS = 'Others', 'Others'

    class LanguageChoices(models.TextChoices):
        HINDI = 'Hindi', 'Hindi'
        ENGLISH = 'English', 'English'

    book_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sell_details')
    book_title = models.CharField(max_length=100)
    book_author = models.CharField(max_length=50)
    book_quantity = models.PositiveIntegerField()
    book_AI_price = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)
    sale_count = models.PositiveIntegerField(default=0)
    book_edition = models.CharField(max_length=50, null=True, blank=True)
    book_isbn = models.CharField(max_length=13, unique=True, null=True)
    verified = models.BooleanField(default=False)
    # Updated Fields with Choices
    boards = models.CharField(
        max_length=10, choices=BoardChoices.choices, default=BoardChoices.CBSE
    )
    subject = models.CharField(
        max_length=20, choices=SubjectChoices.choices, default=SubjectChoices.MATHS
    )
    language = models.CharField(
        max_length=10, choices=LanguageChoices.choices, default=LanguageChoices.ENGLISH
    )
    condition = models.CharField(
        max_length=10, choices=ConditionChoices.choices, default=ConditionChoices.GOOD
    )
    category = models.CharField(
        max_length=20, choices=CategoryChoices.choices, default=CategoryChoices.REFERENCE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = ActiveSellDetailManager()
    all_objects = models.Manager()

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = now()
        self.save()

    def __str__(self):
        return f"{self.book_title} by {self.book_author}"

class BookPhoto(models.Model):
    sell_detail = models.ForeignKey(SellDetail, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='book_photos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.sell_detail.book_title}"

class SellOrder(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buy_orders")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sell_orders")
    book = models.ForeignKey(SellDetail, on_delete=models.CASCADE, related_name="sell_orders")
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.book.book_title} ({self.order_status})"
