from .token_manager import TokenManager


def send_verification_link(user):
    #make user inactive

    try:
        useremail = user.email
        if not useremail:
            raise KeyError(
                'No key named "email" in your form. Your field should be named as email'
            )

        verification_url = token_manager.generate_link(user)
        msg = render_to_string(
            self.settings.get('html_message_template', raise_exception=True),
            {"link": verification_url, "inactive_user": inactive_user}, 
            request=request
        )

        self.__send_email(msg, useremail)
        return inactive_user
    except Exception:
        inactive_user.delete()
        raise
