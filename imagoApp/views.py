from rest_framework.decorators import api_view
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Match, Term, MatchAll
from rest_framework.response import Response
from rest_framework import status
from .elasticsearch_utils import get_es_client
from elasticsearch import Elasticsearch


@api_view(['GET'])
def search_imago_data(request):
    es_client = get_es_client()
    query_param = request.query_params.get('q', None)

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
        hits = [hit.to_dict() for hit in results]
        return Response(hits)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)