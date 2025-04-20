from elasticsearch import Elasticsearch
from django.conf import settings
import ssl

def get_es_client():
    """Returns an Elasticsearch client configured with your credentials."""
    es = Elasticsearch(
        hosts=f"https://{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}",
        basic_auth=(settings.ELASTICSEARCH_USER, settings.ELASTICSEARCH_PASSWORD),
        verify_certs=False,
        ssl_show_warn=False
    )
    print(es)
    return es