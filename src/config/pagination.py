from math import ceil

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "count_pages": ceil(self.page.paginator.count // self.page_size),
                "page": self.page.number,
                "results": data,
            }
        )


class DynamicPageSizePagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "count_pages": ceil(self.page.paginator.count // self.page_size),
                "page": self.page.number,
                "results": data,
            }
        )
