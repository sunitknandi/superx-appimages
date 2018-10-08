from rest_framework.response import Response
from rest_framework.views import status


def validate_search(fn):
    def decorated(*args, **kwargs):
        query = args[0].request.GET.get("search")
        if not query:
            return Response(
                data={
                    "message": "Empty Search! You forgot to type."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return decorated