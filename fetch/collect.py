import pandas as pd
from pandas import DataFrame
from typing import List, Dict
from pymongo.collection import Collection

def make_query(
        query: Dict[str, str],
        collection: Collection
        ) -> DataFrame:
    data = list(
            collection
            .find(
                query,
                {
                    "_id": False,
                    "hora": True,
                    "mean": True,
                    "min": True,
                    "max": True,
                    "std": True
                    }
                )
            )
    return (
            pd
            .DataFrame(data)
            .sort_values(by="hora")
            .reset_index(drop=True)
            )

def find_categories(
        query: Dict[str, str],
        collection: Collection,
        field: str
        ) -> List[str]:
    categories = list(
            collection
            .find(
                query,
                {
                    "_id": False,
                    field: True
                    }
                )
            .distinct(field)
            )
    return categories
