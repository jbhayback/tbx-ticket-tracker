from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    ListView,
    DetailView
)
from django.views.generic.edit import DeleteView
from itertools import chain

from .forms import (
    CommentForm,
    ProjectForm,
    TicketForm
)
from .models import (
    Comment,
    Project,
    Ticket
)


class ProjectContextMixin(object):
    project = None

    def get_project(self):
        if not self.project:
            self.project = get_object_or_404(Project, pk=self.kwargs['project_id'])

        return self.project

    def get_context_data(self, **kwargs):
        context = super(ProjectContextMixin, self).get_context_data(**kwargs)
        context['current_project'] = self.get_project()
        return context


class MyTicketsView(TemplateView):
    template_name = "tracker/my_tickets.html"

    def get_context_data(self):
        if self.request.user.is_authenticated:
            tickets = (
                Ticket.objects
                .filter(assignees=self.request.user.pk)
                .order_by('-modified')
            )
        else:
            tickets = []

        return {
            'tickets': tickets
        }

my_tickets_view = MyTicketsView.as_view()


class ProjectListView(ListView):
    model = Project
    template_name = "tracker/project_list.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        projects = Project.objects.all()

        if self.request.user.is_authenticated:
            projects_with_assigned_tickets = (
                Project.objects
                .filter(tickets__assignees__in=[self.request.user.pk])
                .distinct()
            )
            projects_with_no_assigned_tickets = (
                Project.objects
                .exclude(tickets__assignees__in=[self.request.user.pk])
                .distinct()
            )
            projects = projects_with_assigned_tickets.union(projects_with_no_assigned_tickets, all=True)

        context["projects"] = projects

        return context


project_list_view = ProjectListView.as_view()


class CreateProjectView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "tracker/project_form.html"

    def get_success_url(self):
        return reverse("project_list")

    def get_form_kwargs(self):
        kwargs = super(CreateProjectView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['title'] = 'Create project'
        return kwargs

create_project_view = login_required(CreateProjectView.as_view())


class UpdateProjectView(ProjectContextMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    pk_url_kwarg = 'project_id'
    template_name = "tracker/project_form.html"

    def get_success_url(self):
        return reverse("project_list")

    def get_form_kwargs(self):
        kwargs = super(UpdateProjectView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['title'] = "Edit {0}".format(self.object.title)
        return kwargs

update_project_view = login_required(UpdateProjectView.as_view())


class DeleteProjectView(ProjectContextMixin, DeleteView):
    model = Project
    pk_url_kwarg = 'project_id'
    template_name = "tracker/confirm_delete.html"

    def get_success_url(self):
        return reverse("project_list")

delete_project_view = login_required(DeleteProjectView.as_view())


class ProjectView(ProjectContextMixin, TemplateView):
    template_name = "tracker/project_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)
        project = self.get_project()
        context.update({
            "project": project,
            "tickets": project.tickets.all()
        })
        return context

project_view = ProjectView.as_view()


class CreateTicketView(ProjectContextMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = "tracker/ticket_form.html"

    def get_success_url(self):
        return reverse("project_detail", kwargs={"project_id": self.kwargs['project_id']})

    def get_form_kwargs(self):
        kwargs = super(CreateTicketView, self).get_form_kwargs()
        kwargs['project'] = self.get_project()
        kwargs['user'] = self.request.user
        kwargs['title'] = 'Create ticket'
        return kwargs

create_ticket_view = login_required(CreateTicketView.as_view())


class UpdateTicketView(ProjectContextMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    pk_url_kwarg = 'ticket_id'
    template_name = "tracker/ticket_form.html"

    def get_success_url(self):
        return reverse("project_detail", kwargs={"project_id": self.kwargs['project_id']})

    def get_form_kwargs(self):
        kwargs = super(UpdateTicketView, self).get_form_kwargs()
        kwargs['project'] = self.get_project()
        kwargs['user'] = self.request.user
        kwargs['title'] = "Edit {0}".format(self.object.title)

        if not self.model.objects.filter(pk=self.object.id, project_id=kwargs['project'].id).exists():
            raise ValidationError(f"Ticket: {self.object.title} does not exist in project: {kwargs['project'].title}.")
        
        return kwargs

update_ticket_view = login_required(UpdateTicketView.as_view())


class DeleteTicketView(ProjectContextMixin, DeleteView):
    model = Ticket
    pk_url_kwarg = 'ticket_id'
    template_name = "tracker/confirm_delete.html"

    def get_success_url(self):
        return reverse("project_detail", kwargs={"project_id": self.kwargs['project_id']})

delete_ticket_view = login_required(DeleteTicketView.as_view())


class TicketDetailView(TemplateView):
    model = Comment
    template_name = "tracker/ticket_detail.html"
    pk_url_kwarg = 'ticket_id'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super(TicketDetailView, self).get_context_data(**kwargs)
        ticket = None
        comment_form = None
        if self.request.user.is_authenticated:
            ticket = get_object_or_404(Ticket, pk=self.kwargs['ticket_id'])
            comment_form = self.form_class

        return {
            "ticket": ticket,
            "comment_form": comment_form,
        }

    def post(self, request, *args, **kwargs):
        ticket = get_object_or_404(Ticket, pk=self.kwargs['ticket_id'])
        comment_form = CommentForm(user=request.user, ticket=ticket, data=request.POST)
        if comment_form.is_valid():
            comment_form.save()

        context_data = self.get_context_data(ticket_id=kwargs.get("ticket_id"))
        return self.render_to_response(context_data)

ticket_detail_view = login_required(TicketDetailView.as_view())
