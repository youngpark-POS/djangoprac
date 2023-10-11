from datetime import date

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Book genre")

    def __str__(self) -> str:
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey("author", on_delete=models.SET_NULL, null=True)
    language = models.ForeignKey("Language", on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, default="")
    isbn = models.CharField("ISBN", max_length=13)
    genre = models.ManyToManyField(Genre, help_text="Select genres for this book")

    def __str__(self):
        return self.title

    def get_abs_url(self):
        return reverse("book-detail", args=[str(self.id)])
    
    def display_genre(self):
        return ", ".join(genre.name for genre in self.genre.all()[:5])
    
    display_genre.short_description = "Genre"
    
class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book")
    book = models.ForeignKey("Book", on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', "On loan"),
        ('a', "Available"),
        ('r', "Reserved"),
    )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text="Loan availability",
    )
    class Meta:
        ordering = ["due_back"]
        permissions = (
            ("can_mark_returned", "Set book as returned"),
        )

    def __str__(self):
        return f"{self.id} ({self.book.title})"
    
    @property
    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back)
    
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["date_of_birth", "date_of_death"]
    def get_abs_url(self):
        return reverse('author-detail', args=[str(self.id)])
    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
class Language(models.Model):
    lang = models.CharField(max_length=100)

    def __str__(self):
        return self.lang