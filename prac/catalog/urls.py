from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("books/", views.BookListView.as_view(), name="books"),
    path(r"^book/(?P<pk>\d+)$", views.BookDetailView.as_view(), name='book-detail'),
    path("authors/", views.AuthorListView.as_view(), name="authors"),
    path(r"^author/(?P<pk>\w+)$", views.AuthorDetailView.as_view(), name='author-detail'),
    path("mybooks/", views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]