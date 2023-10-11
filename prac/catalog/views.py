from datetime import datetime, timedelta

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# from django.http import Http404

from catalog.models import *
from catalog.forms import RenewBookForm

# Create your views here.

# Django starts finding templates at '/templates' directory
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.count()

    num_instances_availables = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_availables': num_instances_availables,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

# def book_detail_view(request, primary_key):
#     book = get_object_or_404(Book, pk=primary_key)
#     return render(request, 'catalog/book_detail.html', context={'book': book})

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )

class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    permission_required = (
        "catalog.can_mark_returned",
    )

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # POST method -> process form data
    if request.method == "POST":
        form = RenewBookForm(request.POST)

        # check all generice codes & clean_<> methods
        if form.is_valid():
            book_instance.due_back = form.cleaned_data["renewal_date"]
            book_instance.save()

            return HttpResponseRedirect(reverse("all-borrowed"))
    else:
        proposal_renewal_date = date.today() + timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposal_renewal_date})

    context = {
        "form": form,
        "book_instance": book_instance,
    }
    return render(request, "catalog/book_renew_librarian.html", context)