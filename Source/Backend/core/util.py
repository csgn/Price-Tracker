import json

from django.db import models, connection
from django.http.response import JsonResponse


def makeQuery(query_str: str, query_return: bool = True):
    with connection.cursor() as cursor:
        try:
            cursor.execute(query_str)
        except:
            return JsonResponse({'error': 'Database Error'}, safe=False, status=502)

        res = None
        if query_return:
            columns = [col[0] for col in cursor.description]
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            data = json.dumps(data, default=str, ensure_ascii=False)

            if not data:
                return JsonResponse({'error': 'Something went wrong'}, safe=False, status=404)

            res = data

        return JsonResponse(json.loads(res) if res is not None else {}, safe=False, status=200)


def convertToPSQL(other: dict) -> str:
    return ",".join(list(map(
        lambda x: f"""{x[0]}={ "'"+str(x[1])+"'" if type(x[1]) is str else x[1]}""", other.items())))
