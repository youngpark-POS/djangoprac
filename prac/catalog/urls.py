from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("books/", views.BookListView.as_view(), name="books"),
    path("book/<uuid:pk>/", views.BookDetailView.as_view(), name='book-detail'),
    path("authors/", views.AuthorListView.as_view(), name="authors"),
    path("author/<uuid:pk>/", views.AuthorDetailView.as_view(), name='author-detail'),
    path("mybooks/", views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path("borrowed/", views.LoanedBooksAllListView.as_view(), name='all-borrowed'),
    path("book/<uuid:pk>/renew/", views.renew_book_librarian, name="renew-book-librarian"),
]