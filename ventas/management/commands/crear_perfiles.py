from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ventas.models import Perfil


class Command(BaseCommand):
    help = 'Crea perfiles para todos los usuarios que no tienen uno'

    def handle(self, *args, **kwargs):
        usuarios_sin_perfil = 0
        for user in User.objects.all():
            perfil, created = Perfil.objects.get_or_create(user=user)
            if created:
                usuarios_sin_perfil += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Perfil creado para: {user.username}')
                )
        
        if usuarios_sin_perfil == 0:
            self.stdout.write(
                self.style.WARNING('Todos los usuarios ya tienen perfil')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'\n¡Listo! Se crearon {usuarios_sin_perfil} perfiles')
            )
