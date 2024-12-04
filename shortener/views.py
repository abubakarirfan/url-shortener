from django.shortcuts import get_object_or_404, render, get_object_or_404
from .models import URL
from .utils import generate_short_url
from django.http import JsonResponse
from django.shortcuts import redirect
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def shorten_url(request):
    if request.method == 'POST':
        long_url = request.POST.get('long_url')

        if not long_url:
            return JsonResponse({"error": "Long URL is required"}, status=400)

        # Validate the URL
        validator = URLValidator()
        try:
            validator(long_url)
        except ValidationError:
            return JsonResponse({"error": "Invalid URL format"}, status=400)

        # Check if the URL already exists in the database
        url, created = URL.objects.get_or_create(long_url=long_url)
        if created:
            # Generate a unique short URL
            url.short_url = generate_short_url()
            url.save()

        # Return the shortened URL
        short_url = f"{request.build_absolute_uri('/')}{url.short_url}"
        return JsonResponse({"short_url": short_url})

    return JsonResponse({"error": "Invalid request method"}, status=405)


def search_url(request):
    code = request.GET.get('code', '').strip()
    if code:
        try:
            # Retrieve the URL object based on the short code
            searched_url = URL.objects.get(short_url=code)
            # Build the full short URL
            base_url = request.build_absolute_uri(
                '/')  # e.g., 'http://127.0.0.1:8000/'
            full_short_url = base_url + searched_url.short_url
            return render(request, 'shortener/index.html', {
                'searched_url': searched_url,
                'full_short_url': full_short_url,
            })
        except URL.DoesNotExist:
            # If no URL is found with the provided code
            return render(request, 'shortener/index.html', {
                'search_error': 'No URL found with the provided code.'
            })
    else:
        # If no code was entered
        return render(request, 'shortener/index.html', {
            'search_error': 'Please enter a code to search.'
        })


def index(request):
    if request.method == 'POST':
        long_url = request.POST.get('long_url')
        if not long_url:
            return render(request, 'shortener/index.html', {"error": "Please provide a valid URL"})

        # Validate the URL
        validator = URLValidator()
        try:
            validator(long_url)
        except ValidationError:
            return render(request, 'shortener/index.html', {"error": "Invalid URL format"})

        # Check if the URL already exists in the database
        url, created = URL.objects.get_or_create(long_url=long_url)
        if created:
            # Generate a unique short URL
            url.short_url = generate_short_url()
            url.save()

        short_url = f"{request.build_absolute_uri('/')}{url.short_url}"
        return render(request, 'shortener/index.html', {"short_url": short_url, "click_count": url.click_count})

    return render(request, 'shortener/index.html')


def redirect_url(request, short_url):
    url = get_object_or_404(URL, short_url=short_url)
    # Increment the click count
    url.click_count += 1
    url.save()
    return redirect(url.long_url)

