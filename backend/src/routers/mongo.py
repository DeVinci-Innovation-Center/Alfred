from fastapi import APIRouter

from src.global_instances import md

router = APIRouter()

@router.get("/mongo/all")
def get_all():
    ret = {}

    collections = md.collection_names(include_system_collections=False)
    for collection in collections:
        ret[collection] = []

        cursor = md[collection].find({})

        for document in cursor:
            document["_id"] = str(document["_id"])
            ret[collection].append(document)

    return ret
