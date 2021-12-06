from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'ps'
    page_query_param = 'pi'
    max_page_size = 30
