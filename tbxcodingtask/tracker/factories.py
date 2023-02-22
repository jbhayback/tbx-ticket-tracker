import factory

from django.contrib.auth.models import User
from tbxcodingtask.tracker.models import (
    Comment,
    Project,
    Ticket
)


class UserFactory(factory.django.DjangoModelFactory):
    email = "test@test.com"
    username = "test_user"
    password = "test_password"

    class Meta:
        model = User


class ProjectFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: f'Project {n}')

    class Meta:
        model = Project


class TicketFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: f'Ticket {n}')
    description = factory.Sequence(lambda n: f'Some description {n}')
    project = factory.SubFactory(ProjectFactory)

    class Meta:
        model = Ticket


class CommentFactory(factory.django.DjangoModelFactory):
    content = factory.Sequence(lambda n: f'Comment {n}')
    ticket = factory.SubFactory(TicketFactory)
    author = factory.SubFactory(UserFactory)

    class Meta:
        model = Comment




    