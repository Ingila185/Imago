import requests

from rest_framework.decorators import api_view
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Match, Term, MatchAll
from rest_framework.response import Response
from rest_framework import status
from .elasticsearch_utils import get_es_client
from elasticsearch import Elasticsearch
from django.core.paginator import Paginator, EmptyPage
def check_image_url(url):
    """Check if an image exists at the given URL."""
    try:
        response = requests.head(url, timeout=5)  # Use HEAD request to check existence
        if response.status_code == 200:
            return True
    except requests.RequestException:
        pass
    return False

@api_view(['GET'])
def search_imago_data(request):
    es_client = get_es_client()
    query_param = request.query_params.get('q', None) 
    page = request.query_params.get('page', 1)  # Default to page 1
    page_size = request.query_params.get('page_size', 10)  # Default page size


    try:
        if query_param:
            search_queries = []
            search_queries.append(Match(suchtext=query_param))
            search_queries.append(Term(fotografen=query_param))  # Use Term for keyword field

            # Try to convert query_param to integer for bildnummer search
            try:
                bildnummer_int = int(query_param)
                search_queries.append(Term(bildnummer=bildnummer_int))  # Use Term for exact integer match
            except ValueError:
                # If it's not an integer, we can't directly match against bildnummer
                print(f"Warning: '{query_param}' is not an integer, skipping bildnummer search.")
                pass

            if search_queries:
                combined_query = search_queries[0]
                for q in search_queries[1:]:
                    combined_query = combined_query | q

                s = Search(index="imago", using=es_client).query(combined_query)
                print(f"Generated Elasticsearch query: {s.to_dict()}")
            else:
                return Response({"results": []})  # No valid search queries
        else:
            # Use MatchAll query to fetch all documents when no query parameter is provided
            s = Search(index="imago", using=es_client).query(MatchAll())
            print("No query parameter provided. Fetching all documents.")

        results = s.execute()        
        hits = []
        for hit in results:
            hit_dict = hit.to_dict()
            # Construct the thumbnail URL
            bildnummer = hit_dict.get("bildnummer", "")
            bildnummer = str(bildnummer).zfill(10)
            # Check the primary URL
            primary_url = f"https://www.imago-images.de/bild/st/{bildnummer}/s.jpg"
            if check_image_url(primary_url):
                hit_dict["thumbnail_url"] = primary_url
            else:
                # Check the fallback URL
                fallback_url = f"https://www.imago-images.de/bild/sp/{bildnummer}/s.jpg"
                if check_image_url(fallback_url):
                    hit_dict["thumbnail_url"] = fallback_url
                else:
                    # If neither URL works, set an empty string
                    hit_dict["thumbnail_url"] = ""

            hits.append(hit_dict)
              # Apply pagination
        paginator = Paginator(hits, page_size)
        try:
            paginated_hits = paginator.page(page)
        except EmptyPage:
            return Response({"results": [], "message": "Page out of range"}, status=status.HTTP_404_NOT_FOUND)

        # Return paginated results
        return Response({
            "results": list(paginated_hits),
            "page": int(page),
            "page_size": int(page_size),
            "total_pages": paginator.num_pages,
            "total_results": paginator.count,
        })

        return Response(hits)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)