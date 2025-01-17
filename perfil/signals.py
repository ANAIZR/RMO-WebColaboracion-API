from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Perfil
from scenario_permissions.models import DetailPermission

@receiver(post_migrate)
def insert_perfil(sender, **kwargs):
    print("Migrando perfil y permisos")
    if sender.name == "perfil":
        perfiles = [
            (1, "Entidad", [1, 5, 6, 7, 11, 12]),
            (2, "Área", [6, 12]),
        ]
        for perfil_id, description, *permissions in perfiles:
            print(f"Procesando perfil ID {perfil_id} - {description}")
            perfil, created = Perfil.objects.get_or_create(
                id=perfil_id, defaults={"description": description}
            )
            if permissions:
                permission_ids = permissions[0]                  
                permission_objs = DetailPermission.objects.filter(id__in=permission_ids)
                
                perfil.detail_permisos.set(permission_objs)
                perfil.save()
            else:
                print(f"No se encontraron permisos para el Perfil {perfil_id}")
