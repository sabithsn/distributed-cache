from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.http import HttpResponse
from testcache.models import Recipe
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files import File

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

@csrf_exempt
@cache_page(CACHE_TTL)
def index(request):
    cached_data = cache.get("index_html")
    if cached_data is not None:
        # print ("cached:", cached_data)
        data = {
            "summary": cached_data,
            "miss": 0
        }
        return JsonResponse(data, safe=False)
        # return HttpResponse (cached_data)
    else:
        with open('index.html', 'r') as f:
            file_content = f.read()

        cache.set("index_html", file_content)  # cache the result
        data = {
            "summary": file_content,
            "miss": 1
        }
        return JsonResponse (data, safe=False)
    return render(request, 'index.html')

@csrf_exempt
@cache_page(60 * 15)  # cache for 15 minutes
def db_query(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        cleaned_title = title.replace(" ","_")

        cached_data = cache.get(cleaned_title)
        if cached_data is not None:
            print ("cached:", cached_data)
            data = {
                "summary": cached_data,
                "miss": 0
            }
            return JsonResponse(data, safe=False)
            # return HttpResponse (cached_data)
        else:
            expensive_data = Recipe.objects.filter(title=title)[0]  # perform the expensive operation
            summary = expensive_data.summary
            print ("title:", title)
            print ("summary:", summary)
            cache.set(cleaned_title, summary)  # cache the result
            data = {
                "summary": summary,
                "miss": 1
            }
            return JsonResponse (data, safe=False)



