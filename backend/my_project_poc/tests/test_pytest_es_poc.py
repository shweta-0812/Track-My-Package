import pytest

from pytest_elasticsearch import factories

from common.app_settings import app_settings

elasticsearch_noproc = factories.elasticsearch_noproc(
    port=app_settings.ELASTICSEARCH_PORT, host=app_settings.ELASTICSEARCH_HOST)

elasticsearch = factories.elasticsearch('elasticsearch_noproc')


class TestSuccessResponses:
    @pytest.fixture(autouse=True)
    def spam_index(self, elasticsearch):
        elasticsearch.indices.create(index="spam")
        elasticsearch.indices.put_mapping(
            include_type_name=True,
            body={
                "properties": {
                    "id": {"type": "keyword"},
                    "type": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
                    },
                }
            },
            doc_type="_doc",
            index="spam",
        )

    def test_egg_finder(self, elasticsearch):
        elasticsearch.create(
            "spam", "1", {"id": "1", "type": "Scrambled"}, refresh=True
        )
        resp = elasticsearch.indices.exists("spam")
        assert resp

