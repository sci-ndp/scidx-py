from .init_client import sciDXClient
from .create_datasource import create_datasource

# Add the create_datasource method to sciDXClient
sciDXClient.create_datasource = create_datasource