from django.http import JsonResponse

__author__ = 'snake'


def m2m_ajax(request, model, search_fields, limit=10):
    limit = request.GET.get('limit') if request.GET.get('limit') is not None else limit
    q = request.GET.get('q')
    query_kwargs = {'%s__istartswith' % search_field: q for search_field in search_fields}
    qs = model.objects.filter(**query_kwargs).order_by(*search_fields)[:limit]
    choices = list({'id': o.pk, 'value': str(o)} for o in qs)
    return JsonResponse({'choices': choices})
