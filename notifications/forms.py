from django.forms import CharField, Form, HiddenInput, UUIDField


class NotificationLinkForm(Form):
    notification_id = UUIDField(
        widget=HiddenInput(),
        required=True
    )
    redirect_url = CharField(
        widget=HiddenInput(),
        required=True
    )