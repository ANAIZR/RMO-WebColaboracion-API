from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Perfil
from permissions.models import DetailPermission

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
            if created:
                print(f"Perfil creado: {perfil_id} - {description}")
            else:
                print(f"Perfil ya existente: {perfil_id} - {description}")

            if permissions:
                # `permissions` debería ser una lista de permisos
                permission_ids = permissions[0]  # Extrae la lista de permisos
                print(f"Permisos asociados: {permission_ids}")
                
                # Filtra permisos usando una lista de IDs
                permission_objs = DetailPermission.objects.filter(id__in=permission_ids)
                print(f"Permisos encontrados: {permission_objs}")
                
                # Asigna permisos al rol
                perfil.detail_permisos.set(permission_objs)
                perfil.save()
                print(f"Rol actualizado: {perfil_id}")
            else:
                print(f"No se encontraron permisos para el rol {perfil_id}")
