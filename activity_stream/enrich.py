#from stream_django.enrich import Enrich as BaseEnrich
from .models import Follow


'''
def do_i_follow_users(user, users):
    followed_user_ids = Follow.objects.filter(user_id=user.id, target__in=users, deleted_at__isnull=True).values_list('target_id', flat=True)
    for u in users:
        u.followed = u.id in followed_user_ids


def do_i_follow(user, follows):
    do_i_follow_users(user, [f.target for f in follows])


class Enrich(BaseEnrich):

    def __init__(self, current_user, *args, **kwargs):
        super(Enrich, self).__init__(*args, **kwargs)
        self.current_user = current_user

    def fetch_follow_instances(self, pks):
        follows = Follow.objects.select_related(*Follow.activity_related_models()).in_bulk(pks)
        if self.current_user.is_authenticated():
            do_i_follow(self.current_user, follows.values())
        return follows
'''

