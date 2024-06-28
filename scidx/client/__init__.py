from .init_client import sciDXClient
from .register_organization import register_organization
from .search_resource import search_resource
from .search_organization import search_organization
from .register_url import register_url
from .register_s3 import register_s3


# Add the methods to sciDXClient
sciDXClient.register_organization = register_organization
sciDXClient.search_organization = search_organization
sciDXClient.search_resource = search_resource
sciDXClient.register_url = register_url
sciDXClient.register_s3 = register_s3

