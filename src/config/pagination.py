from math import ceil

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 20

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "count_pages": ceil(self.page.paginator.count // self.page_size),
                "page": self.page.number,
                "results": data,
            }
        )
