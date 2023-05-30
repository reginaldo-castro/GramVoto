from django.db import models, IntegrityError
from django.contrib.auth.models import User
1
class Candidato(models.Model):
    name = models.CharField(max_length=250)
    votes = models.IntegerField(default=0)
    matricula = models.CharField(max_length=4)
    numero = models.CharField(max_length=2)
    
    def __str__(self):
        return self.name


class Voto(models.Model):
    ip_address = models.CharField(
        max_length=50,
        default="None",
        unique=True
    )
    candidato = models.ForeignKey(
        to=Candidato,
        on_delete=models.CASCADE,
        related_name='voto'
    )
    eleitor = models.CharField(
        max_length=100,
        default="None",
        unique=True
    )

    def save(self, commit=True, *args, **kwargs):

        if commit:
            try:
                self.candidato.votes += 1
                self.candidato.save()
                super(Voto, self).save(*args, **kwargs)

            except IntegrityError:
                self.candidato.votes -= 1
                self.candidato.save()
                raise IntegrityError

        else:
            raise IntegrityError

    def __str__(self):
        return self.candidato.name
