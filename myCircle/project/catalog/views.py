from django.shortcuts import render
from django.views import generic
# Create your views here.

from .models import Book, Author, BookInstance, Genre

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

    #REnder the HTML template index.html with the data ni the context variable.
    return render(request,'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_avaliable':num_instances_avaliable,'num_authors':num_authors},
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
