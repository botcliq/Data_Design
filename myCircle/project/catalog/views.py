from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import datetime
from django.views.generic.edit import CreateView,UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.

from .models import Book, Author, BookInstance, Genre
from .forms import RenewBookForm

def index(request):
    """
    View function for home page site
    """

    # Generate counts for home page of site.
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    #Avaliable Books (status = 'a')
    num_instances_avaliable = BookInstance.objects.filter(status__exact='a').count()
    num_authors= Author.objects.count() # THe 'all() is implied by default'

    num_visits = request.session.get('num_visits',0)
    request.session['num_visits'] = num_visits+1

    #REnder the HTML template index.html with the data ni the context variable.
    return render(request,'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_avaliable':num_instances_avaliable,'num_authors':num_authors,'num_visits':num_visits},
    )

class BookListView(generic.ListView):
    model = Book
    #context_object_name = 'my_book_list'  # your own name for the list as a template variable.
    #queryset = Book.objects.filter(title__icontains='war')[:5] #Get 5 books containing the title war
    template_name = 'book_list.html' #Specify your own template name/location

class BookDetailView(generic.DetailView):
    model = Book
    paginate_by = 10

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author
    paginate_by = 10

class LoanedBookByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on load to current user.
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            return HttpResponseRedirect(reverse('my-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial = {'renewal_date': proposed_renewal_date,})
    return render(request, 'catalog/book_renew_librarian.html',{'form':form,'bookinst':book_inst})    

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death':'None',}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
