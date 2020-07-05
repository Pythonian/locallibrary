from django.conf.urls import url 
from . import views


urlpatterns = [

	url(r'^$', 
		views.index, 
		name='index'),

	url(r'^books/$',
		views.book_list,
		name='books'),

	url(r'^mybooks/$',
		views.loanedbooksbyuser,
		name='my-borrowed'),

	url(r'^borrowed/$',
		views.borrowed_books,
		name='all-borrowed'),

	url(r'^book/(?P<pk>\d+)/$',
		views.book_detail,
		name='book-detail'),

	url(r'^book/(?P<pk>[-\w]+)/renew/$', 
		views.renew_book_librarian, 
		name='renew-book-librarian')

]

urlpatterns += [  
    url(r'^author/create/$', 
    	views.AuthorCreate.as_view(), 
    	name='author_create'),

    url(r'^author/(?P<pk>\d+)/update/$', 
    	views.AuthorUpdate.as_view(), 
    	name='author_update'),

    url(r'^author/(?P<pk>\d+)/delete/$', 
    	views.AuthorDelete.as_view(), 
    	name='author_delete'),
]

