from bson import ObjectId


def merge(src, dest):
    for key, value in src.items():
        setattr(dest, key, value)
    return dest


def convert_object_id_to_str(v):
    if isinstance(v, ObjectId):
        return str(v)
    return v
