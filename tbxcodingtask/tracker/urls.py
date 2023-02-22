from django.conf.urls import url

from .views import (
	create_project_view,
	create_ticket_view,
	delete_project_view,
	delete_ticket_view,
	my_tickets_view,
	project_view,
	project_list_view,
	ticket_detail_view,
	update_project_view,
	update_ticket_view,
)

urlpatterns = [
    url(r'^projects/$', project_list_view, name='project_list'),
    url(r'^projects/create/$', create_project_view, name='project_create'),
    url(
    	r'^projects/(?P<project_id>\d+)/edit/$',
    	update_project_view,
    	name='project_update'
	),
	url(
    	r'^projects/(?P<project_id>\d+)/delete/$',
    	delete_project_view,
    	name='project_delete'
	),
    url(
    	r'^projects/(?P<project_id>\d+)/tickets/create$',
    	create_ticket_view,
    	name='ticket_create'
	),
    url(
    	r'^projects/(?P<project_id>\d+)/tickets/(?P<ticket_id>\d+)/edit$',
    	update_ticket_view,
    	name='ticket_update'
	),
	url(
    	r'^projects/(?P<project_id>\d+)/tickets/(?P<ticket_id>\d+)/delete$',
    	delete_ticket_view,
    	name='ticket_delete'
	),
    url(r'^projects/(?P<project_id>\d+)/$', project_view, name='project_detail'),
    url(r'^$', my_tickets_view, name='my_tickets'),
	url(
    	r'^projects/(?P<project_id>\d+)/tickets/(?P<ticket_id>\d+)$',
    	ticket_detail_view,
    	name='ticket_detail'
	),
]
