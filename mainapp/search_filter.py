import django_filters
from django_filters import DateFilter, CharFilter, NumberFilter

from .models import Article
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class DateInput(forms.DateInput):
    input_type = 'date'


class ArticleFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='contains')
    text = CharFilter(field_name='text', lookup_expr='contains')
    rating_start = NumberFilter(field_name='rating', lookup_expr='gte')
    rating_end = NumberFilter(field_name='rating', lookup_expr='lte')
    start_date = DateFilter(field_name='add_datetime', lookup_expr='gte', widget=DateInput())
    end_date = DateFilter(field_name='add_datetime', lookup_expr='lte', widget=DateInput())

    class Meta:
        model = Article
        fields = ['author', 'hub']