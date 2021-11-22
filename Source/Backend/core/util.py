import json

from django.db import models, connection
from django.http.response import JsonResponse


def makeQuery(query_str: str):
    with connection.cursor() as cursor:
        try:
            cursor.execute(query_str)
        except:
            return

        columns = [col[0] for col in cursor.description]
        res = [dict(zip(columns, row)) for row in cursor.fetchall()]
        res = json.dumps(res, default=str, ensure_ascii=False)

        if not res:
            return JsonResponse({'error': 'Something went wrong'}, safe=False, status=404)

        return JsonResponse(json.loads(res), safe=False, status=200)
