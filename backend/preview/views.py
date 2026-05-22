from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .scrapers.router import get_scraper_for_url, UnsupportedPlatformError
from .scrapers.base import ScrapeError
from .validators import validate_social_url


@require_GET
def preview_endpoint(request):
    raw_url = request.GET.get("url")
    if not raw_url:
        return JsonResponse({"detail": "Missing url query parameter."}, status=400)

    try:
        normalized_url = validate_social_url(raw_url)
    except ValueError as exc:
        return JsonResponse({"detail": str(exc)}, status=400)

    try:
        scraper = get_scraper_for_url(normalized_url)
        preview = scraper.fetch_preview()
        return JsonResponse(preview, status=200)
    except UnsupportedPlatformError as exc:
        return JsonResponse({"detail": str(exc)}, status=400)
    except ScrapeError as exc:
        status_code = 502 if exc.status_code is None else exc.status_code
        return JsonResponse({"detail": exc.message}, status=status_code)
    except Exception as exc:
        return JsonResponse(
            {"detail": "Unable to fetch preview from the target URL."},
            status=502,
        )
