from django.forms import Form, UUIDField, HiddenInput, ChoiceField


class ApproveMembershipForm(Form):
    reader_id = UUIDField(
        widget=HiddenInput
    )
    club_role = ChoiceField(
        choices=(
            ('AD', 'Admin'), ('PT', 'Participant'), ('RD', 'Reader'), ('OB', 'Observer')
        )
    )


class DenyMembershipForm(Form):
    reader_id = UUIDField(
        widget=HiddenInput
    )
