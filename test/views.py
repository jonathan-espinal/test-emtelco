from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

from .models import Vulnerability
from .serializers import VulnerabilitySerializer


class VulnerabilityPagination(PageNumberPagination):
    page_size = 10


class VulnerabilityListView(APIView):
    pagination_class = VulnerabilityPagination

    def get(self, request):
        items = Vulnerability.objects.all()
        paginator = self.pagination_class()
        paginated_items = paginator.paginate_queryset(items, request)
        serializer = VulnerabilitySerializer(paginated_items, many=True)
        return paginator.get_paginated_response(serializer.data)


class VulnerabilityFixView(APIView):
    def post(self, request):
        cve_ids = request.data.get("cve_ids", [])

        if not isinstance(cve_ids, list):
            return Response({"error": "cve_ids must to be a list."}, status=status.HTTP_400_BAD_REQUEST)

        updated_count = Vulnerability.objects.filter(cve_id__in=cve_ids).update(fixed=True)

        return Response({"message": f"{updated_count} vulnerabilities fixed."}, status=status.HTTP_200_OK)


class VulnerabilityNonFixedListView(APIView):
    pagination_class = VulnerabilityPagination

    def get(self, request):
        items = Vulnerability.objects.filter(fixed=False)
        paginator = self.pagination_class()
        paginated_items = paginator.paginate_queryset(items, request)
        serializer = VulnerabilitySerializer(paginated_items, many=True)
        return paginator.get_paginated_response(serializer.data)


class VulnerabilityCountView(APIView):
    def get(self, request):
        severity_counts = Vulnerability.objects.values("severity").annotate(count=Count("id"))

        return Response(severity_counts)
