from django.urls import path
from graphene_django.views import GraphQLView
from graphene_file_upload.django import FileUploadGraphQLView
from .schema import schema

urlpatterns = [
    # path("graphql/", GraphQLView.as_view(graphiql=True)),  # Enable GraphQL UI
    path("graphql/", FileUploadGraphQLView.as_view(graphiql=True, schema=schema)),
]