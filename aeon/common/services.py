def all_objects(objects):
    return objects.all()

def filter_objects(objects, **kwargs):
    return objects.filter(**kwargs)