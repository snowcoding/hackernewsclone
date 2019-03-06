import graphene
from graphene_django import DjangoObjectType
from users.schema import UserType

from .models import Link


# When creating a new Type, if we Model then we can inherit the fields by using a built-in DjangoObjectType, which is
# also an ObjectType
class LinkType(DjangoObjectType):
    # We can create a field outside the model (if it makes sense) and then resolve it via whatever logic makes sense
    foo = graphene.String()

    class Meta:
        model = Link

    def resolve_foo(self, info, **kwargs):
        # self refers to the link instance
        return "Resolve F"


class Query(graphene.ObjectType):
    # Each element in the list  is a LinkType
    # links is an class instance of the List which is of LinkType
    links = graphene.List(LinkType)

    # Resolving - what should we return in that field?
    def resolve_links(self, info, **kwargs):
        return Link.objects.all()


class CreateLink(graphene.Mutation):
    # These fields are initialized with some instance of types (which reserves a portion in memory)
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()
    posted_by = graphene.Field(UserType)

    class Arguments:
        url = graphene.String()
        description = graphene.String()

    def mutate(self, info, url, description):
        user = info.context.user or None
        link = Link(
            url=url,
            description=description,
            posted_by=user,
        )
        link.save()

        # Instance of the CreateLink class
        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
            posted_by=link.posted_by,
        )


class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    vim = CreateLink.Field()
