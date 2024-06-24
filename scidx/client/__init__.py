from .init_client import sciDXClient
from .register_organization import register_organization
from .register_datasource import register_datasource
from .search_datasource import search_datasource
from .search_organization import search_organization
from .delete_organization import delete_organization
from .register_kafka import register_kafka
from .search_kafka import search_kafka

# Add the methods to sciDXClient
sciDXClient.register_organization = register_organization
sciDXClient.register_datasource = register_datasource
sciDXClient.search_datasource = search_datasource
sciDXClient.search_organization = search_organization
sciDXClient.delete_organization = delete_organization
sciDXClient.register_kafka = register_kafka
sciDXClient.search_kafka = search_kafka