from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, display_genre  
# Register your models here.

#Define the admin class

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name','date_of_birth','date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth','date_of_death')]
# Register the admin class with the associated model
#admin.site.register(Book)
admin.site.register(Author, AuthorAdmin)

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author')
    inlines = [BooksInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
   list_display = ('book','status','borrower','due_back','id')
   list_filter = ('status','due_back')

#class BooksInstanceInline(admin.TabularInline):
#    model = BookInstance 

admin.site.register(Genre)
