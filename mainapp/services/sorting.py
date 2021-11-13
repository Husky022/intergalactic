from mainapp.models import Sorting


def get_sorted_queryset(self, query_set):
    if self.request.user.is_anonymous:
        try:
            sorting_type = self.request.session['sorting']
        except:
            sorting_type = 'NEWEST'
    else:
        sorting_obj = Sorting.objects.get_or_create(user=self.request.user)
        sorting_type = sorting_obj[0].sorting_type
    if sorting_type == 'ELDEST':
        query_set = query_set.order_by('add_datetime')
    elif sorting_type == 'NEWEST':
        query_set = query_set.order_by('-add_datetime')
    elif sorting_type == 'LK_MORE':
        query_set = query_set.order_by('-count_like')
    elif sorting_type == 'LK_LESS':
        query_set = query_set.order_by('count_like')
    elif sorting_type == 'COM_MORE':
        query_set = query_set.order_by('-count_comment')
    elif sorting_type == 'COM_LESS':
        query_set = query_set.order_by('count_comment')
    return query_set

