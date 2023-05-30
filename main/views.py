from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from main.serializers import VoteSerializer, CandidateSerializer
from main.models import Candidato
from django.db import IntegrityError


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_client_user(request):
    usuario = request.user
    return usuario


class CandidateViewSet(ModelViewSet):
    queryset = Candidato.objects.all().order_by('-votes')
    serializer_class = CandidateSerializer
    permission_classes = [IsAdminUser, ]


class CastVoteView(APIView):

    def post(self, request):
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            created_instance = serializer.create(validated_data=request.data)
            created_instance.ip_address = get_client_ip(request)
            created_instance.eleitor = get_client_user(request)
            
            try:
                created_instance.save()

            except IntegrityError:
                return Response(
                    {
                        "message": "Já votei"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                {
                    "message": "Voto lançado com sucesso"
                },
                status=status.HTTP_200_OK
            )
