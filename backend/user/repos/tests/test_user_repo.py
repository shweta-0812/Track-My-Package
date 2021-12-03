import pytest

from pytest_elasticsearch import factories

from backend.common.app_settings import app_settings
from user.model import USER_MODEL, USER_ES_INDEX_DOC_MAPPINGS
from user.repos import user_repo

elasticsearch_noproc = factories.elasticsearch_noproc(
    port=app_settings.ELASTICSEARCH_PORT, host=app_settings.ELASTICSEARCH_HOST
)

elasticsearch = factories.elasticsearch("elasticsearch_noproc")

