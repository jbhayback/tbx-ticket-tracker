from django import forms
from django.contrib.auth import get_user_model

from crispy_forms_foundation.forms import FoundationModelForm

from .models import Comment, Project, Ticket


class BaseTrackerForm(FoundationModelForm):
    def __init__(self, user=None, title=None, *args, **kwargs):
        self.title = title
        self.user = user

        super(BaseTrackerForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label

    def save(self, *args, **kwargs):
        commit = kwargs.pop('commit', True)
        instance = super(BaseTrackerForm, self).save(
            commit=False, *args, **kwargs)

        self.pre_save(instance)

        if commit:
            instance.save()

        return instance

    def pre_save(self, instance):
        pass


class ProjectForm(BaseTrackerForm):
    class Meta:
        model = Project
        fields = ('title',)

    def pre_save(self, instance):
        instance.created_by = self.user


class TicketForm(BaseTrackerForm):
    assignees = forms.ModelMultipleChoiceField(queryset=None, required=False)

    class Meta:
        model = Ticket
        fields = ('title', 'description', 'assignees',)

    def __init__(self, project=None, *args, **kwargs):
        self.project = project
        self.assignees = dict(kwargs.get('data', {})).get("assignees", [])
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['assignees'].queryset = get_user_model().objects.all()

    def pre_save(self, instance):
        instance.created_by = self.user
        instance.project = self.project

        # This is needed for the creation of Ticket
        # because the Ticket object has to be saved first before an assignee can be assigned to it
        if not Ticket.objects.filter(pk=instance.pk).exists():
            instance.save()

        self._assign_users(instance)
    
    def _assign_users(self, instance):
        # Clear the assigness before assigning the new ones
        # to avoid error when reassigning already assigned Users
        instance.assignees.clear()
        for assignee in self.assignees:
            instance.assignees.add(int(assignee))


class CommentForm(BaseTrackerForm):
    class Meta:
        model = Comment
        fields = ('content',)

    def __init__(self, user=None, ticket=None, *args, **kwargs):
        self.ticket = ticket
        super(CommentForm, self).__init__(user=user, *args, **kwargs)

    def pre_save(self, instance):
        instance.author = self.user
        instance.ticket = self.ticket
