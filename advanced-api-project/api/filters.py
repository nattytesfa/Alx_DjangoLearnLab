from rest_framework.filters import SearchFilter as DRFSearchFilter
from rest_framework.filters import OrderingFilter as DRFOrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Create aliases that can be imported as filters.SearchFilter, filters.OrderingFilter
SearchFilter = DRFSearchFilter
OrderingFilter = DRFOrderingFilter
