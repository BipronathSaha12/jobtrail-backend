import io
import csv
import zoneinfo
from django.utils import timezone
from django.http import HttpResponse
from django.db.models import Q
from rest_framework import viewsets, generics, permissions, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Application
from .serializers import ApplicationSerializer, RegisterSerializer, CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class ApplicationPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 500

class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ApplicationPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "job_type"]
    search_fields = ["company", "position"]
    ordering_fields = ["created_at", "applied_on", "expected_salary"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Application.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        applied_on = serializer.validated_data.get("applied_on")
        if not applied_on:
            tz_header = self.request.headers.get("X-Timezone", "Asia/Dhaka")
            try:
                user_tz = zoneinfo.ZoneInfo(tz_header)
            except Exception:
                user_tz = zoneinfo.ZoneInfo("Asia/Dhaka")
            local_today = timezone.now().astimezone(user_tz).date()
            serializer.save(owner=self.request.user, applied_on=local_today)
        else:
            serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def export(self, request):
        queryset = self.get_queryset()
        status_filter = request.GET.get("status")
        job_type_filter = request.GET.get("job_type")
        search = request.GET.get("search")

        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if job_type_filter:
            queryset = queryset.filter(job_type=job_type_filter)
        if search:
            queryset = queryset.filter(
                Q(company__icontains=search) | Q(position__icontains=search)
            )

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "ID", "Company", "Position", "Status", "Job Type",
            "Expected Salary", "Applied On", "Job Link", "Notes", "Created At"
        ])
        for app in queryset:
            writer.writerow([
                app.id,
                app.company,
                app.position,
                app.status,
                app.job_type,
                app.expected_salary or "",
                app.applied_on or "",
                app.job_link or "",
                app.notes or "",
                app.created_at.strftime("%Y-%m-%d %H:%M:%S") if app.created_at else "",
            ])

        csv_data = "\ufeff" + output.getvalue()
        response = HttpResponse(csv_data, content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="jobtrail_applications.csv"'
        return response

class StatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        apps = Application.objects.filter(owner=request.user).values(
            "id", "status", "applied_on", "created_at"
        )

        status_counts = {"wishlist": 0, "applied": 0, "interview": 0, "offer": 0, "rejected": 0}
        monthly_map = {}

        for app in apps:
            st = (app["status"] or "WISHLIST").lower()
            status_counts[st] = status_counts.get(st, 0) + 1

            # Determine date: prefer applied_on, fallback to created_at
            d = app["applied_on"] or (app["created_at"].date() if app["created_at"] else None)
            if d:
                key = d.strftime("%Y-%m")
                label = d.strftime("%b %Y")
                if key not in monthly_map:
                    monthly_map[key] = {
                        "key": key,
                        "month": label,
                        "total": 0,
                        "wishlist": 0,
                        "applied": 0,
                        "interview": 0,
                        "offer": 0,
                        "rejected": 0,
                    }
                monthly_map[key]["total"] += 1
                if st in monthly_map[key]:
                    monthly_map[key][st] += 1

        status_counts["total"] = len(apps)
        sorted_trends = [monthly_map[k] for k in sorted(monthly_map.keys())]

        return Response({
            **status_counts,
            "monthly_trends": sorted_trends,
        }, status=status.HTTP_200_OK)

