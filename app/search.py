from flask import current_app


def add_to_index(index, model):
    try:
        if not current_app.elasticsearch:
            return
        payload = {}
        for field in model.__searchable__:
            payload[field] = getattr(model, field)
        current_app.elasticsearch.index(index=index, doc_type=index, id=model.id,
                                        body=payload)
    except Exception as e:
        print(e)


def remove_from_index(index, model):
    try:
        if not current_app.elasticsearch:
            return
        current_app.elasticsearch.delete(index=index, doc_type=index, id=model.id)
    except Exception as e:
        print(e)


def query_index(index, query, page, per_page):
    try:
        if not current_app.elasticsearch:
            return [], 0
        search = current_app.elasticsearch.search(
            index=index, doc_type=index,
            body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
                  'from': (page - 1) * per_page, 'size': per_page})
        ids = [int(hit['_id']) for hit in search['hits']['hits']]
        return ids, search['hits']['total']
    except Exception as e:
        print(e)
