from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = "limit"

    def get_paginated_response(self, data):
        headers = {
            "Page": self.page.number,
            "Total": self.page.paginator.count,
            "Per-Page": self.page.paginator.per_page,
        }
        return Response(data, headers=headers)

    def get_paginated_response_schema(self, schema):
        return schema
