from .models import Follow
from django import forms
from datetime import datetime


class FollowForm(forms.Form):
    target = forms.IntegerField()
    remove = forms.IntegerField(required=False)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(FollowForm, self).__init__(*args, **kwargs)

    def save(self):
        target = self.cleaned_data['target']
        remove = bool(int(self.cleaned_data.get('remove', 0) or 0))

        if remove:
            follows = Follow.objects.filter(user=self.user, target_id=target)
            now = datetime.now()
            for follow in follows:
                follow.deleted_at = now
                follow.save()
        else:
            follow, created = Follow.objects.get_or_create(user=self.user, target_id=target)
            if not created and follow.deleted_at is not None:
                follow.deleted_at = None
                follow.save()
