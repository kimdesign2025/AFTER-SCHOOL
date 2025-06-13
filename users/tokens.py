from django.contrib.auth.tokens import PasswordResetTokenGenerator

class RegistrationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        """Génère une valeur de hachage pour le token."""
        return (
            str(user.pk) + str(timestamp) +
            str(user.is_active)
        )

registration_token = RegistrationTokenGenerator()