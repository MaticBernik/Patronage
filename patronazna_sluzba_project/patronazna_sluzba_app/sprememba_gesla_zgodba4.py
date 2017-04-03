from .models import *
from kreiranje_pacienta_zgodba2 import preveri_gesli


def sprememba_gesla(geslo1, geslo2, id):
    if preveri_gesli(geslo1, geslo2):
        user = User.objects.get(username=id)
        user.set_password(geslo1)
        user.save()

        return 1
    return 0

