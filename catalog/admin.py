from django.contrib import admin
from .models import Author, Genre, BookInstance, Book, Language


# admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)


class BookInline(admin.StackedInline):
	model = Book
	extra = 0

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
	list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
	fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
	inlines = [BookInline]


class BookInstanceInline(admin.TabularInline):
	model = BookInstance
	extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'display_genre')
	inlines = [BookInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
	list_display = ('id', 'book', 'status', 'borrower', 'due_back')
	list_filter = ('status', 'due_back')
	fieldsets = (
	    (None, {
	        'fields': ('book','imprint', 'id')
	    }),
	    ('Availability', {
	        'fields': ('borrower', 'status', 'due_back')
	    }),
	)
