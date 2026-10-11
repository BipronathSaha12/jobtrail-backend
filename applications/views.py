import zoneinfo
from django.utils import timezone
from rest_framework import viewsets, generics, permissions, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from .models import Application
from .serializers import ApplicationSerializer, RegisterSerializer, CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
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

class StatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        rows = (
            Application.objects.filter(owner=request.user)
            .values("status")
            .annotate(n=Count("id"))
        )
        data = {row["status"].lower(): row["n"] for row in rows}
        
        # Ensure every key is present even if count is 0
        for key in ["wishlist", "applied", "interview", "offer", "rejected"]:
            data.setdefault(key, 0)
            
        data["total"] = sum(data.values())
        return Response(data, status=status.HTTP_200_OK)
