from typing import Any, Optional, Dict


class ESDataParser:
    def __init__(self, es_data):
        self.es_data = es_data
        self.shards_details = None
        self.hits_count_details = None
        self.hits_data_details = None
        self.parsed_data = None
        if es_data is not None:
            self.shards_details = es_data["_shards"]
            self.hits_count_details = es_data["hits"]["total"]
            self.hits_data_details = es_data["hits"]["hits"]
            self.parsed_data = dict(
                shard_details=self.shards_details,
                hits_count_details=self.hits_count_details,
                hits_data_details=self.hits_data_details,
            )


def get_data(self) -> Dict[Any, Any]:
    return self
