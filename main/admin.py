from django.contrib import admin

from main.models import Candidato, Voto


@admin.register(Candidato)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ["name", "matricula", "numero"]


@admin.register(Voto)
class VoteAdmin(admin.ModelAdmin):
    list_display = ["candidato", "ip_address"]
