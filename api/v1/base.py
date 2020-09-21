from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    page_size = 100  # Default number of elements in each page
    page_size_query_param = 'page_size'
    max_page_size = 150  # Max number of elements in each page
