from django.shortcuts import render, get_object_or_404
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
import datetime
from .forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView


def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_genres = Genre.objects.count()
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(
    	status__exact='a').count()
    num_authors = Author.objects.count()  # The 'all()' is implied by default.

	# Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'catalog/index.html',
        context={
        	'num_books': num_books,
        	'num_instances': num_instances,
        	'num_genres': num_genres,
        	'num_instances_available': num_instances_available,
        	'num_authors': num_authors,
        	'num_visits': num_visits,
        },
    )

def book_list(request):
	book_list = Book.objects.all()

	return render(
		request,
		'catalog/book_list.html',
		context={
			'book_list': book_list,
		},
	)

def book_detail(request, pk):
	book = get_object_or_404(
		Book,
		pk=pk)

	return render(
		request,
		'catalog/book_detail.html',
		context={
			'book': book,
		},
	)

@login_required
def loanedbooksbyuser(request):
	loaned_books = BookInstance.objects.filter(
		borrower=request.user).filter(
		status__exact='o').order_by(
		'due_back')

	return render(
		request,
		'catalog/bookinstance_list_borrowed_user.html',
		context={
			'bookinstance_list': loaned_books,
		},
	)

@permission_required('catalog.can_mark_returned')
def borrowed_books(request):
	borrowed_books = BookInstance.objects.filter(
		status__exact='o').order_by(
		'due_back')

	return render(
		request,
		'catalog/bookinstance_all_borrowed.html',
		context={
			'bookinstance_list': borrowed_books,
		},
	)


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(
    	BookInstance, 
    	pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required 
            # (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
            # redirect to a new URL:
            return HttpResponseRedirect(
            	reverse('all-borrowed'))
    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(
    	request, 
    	'catalog/book_renew_librarian.html', 
    	{'form': form, 
    	'bookinst':book_inst}
    )


class AuthorCreate(CreateView):
	model = Author
	fields = '__all__'
	initial = {'date_of_death': '12/10/2016',}

class AuthorUpdate(UpdateView):
	model = Author
	fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
	model = Author
	success_url = reverse_lazy('authors')

	