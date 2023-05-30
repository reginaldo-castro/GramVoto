from rest_framework import serializers
from main.models import Candidato, Voto
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db import IntegrityError


class CandidateSerializer(serializers.ModelSerializer):
    votes = serializers.ReadOnlyField()

    class Meta:
        model = Candidato
        fields = "__all__"


class VoteSerializer(serializers.ModelSerializer):
    candidato_name = serializers.CharField()
    #eleitor_name = serializers.CharField()
    def create(self, validated_data):
        #eleitor = get_object_or_404(Candidato, name=validated_data["eleitor_name"])
        candidato = get_object_or_404(Candidato, name=validated_data["candidato_name"])
        voto = Voto()
        #voto.eleitor = eleitor
        voto.candidato = candidato
        
        try:
            voto.save(commit=False)
        except IntegrityError:
            return voto
        return voto

    class Meta:
        model = Voto
        exclude = ("id", "ip_address", "candidato")
