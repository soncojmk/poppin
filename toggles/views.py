from django.http import HttpResponseForbidden
from django.views.generic.base import View


class ToggleView(View):
    """
    Handles requests to turn on/off a toggle.
    """
    http_method_names = ('put', 'delete')


class AuthenticatedToggleView(ToggleView):
    """
    Extends ToggleView by requiring an authenticated user.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        return super(AuthenticatedToggleView, self).dispatch(request, *args, **kwargs)

class LikeToggleView(AuthenticatedToggleView):
    def put(self, request, object_pk):
        """
        Handle requests to like an object.
        """
        try:
            request.user.liked_objects.add(object_pk)
        except IntegrityError:
            return HttpResponseBadRequest()
        return HttpResponse()

    def delete(self, request, object_pk):
        """
        Handle requests to unlike an object.
        """
        try:
            request.user.liked_objects.remove(object_pk)
        except IntegrityError:
            return HttpResponseBadRequest()
        return HttpResponse()
    def get_context_date(self, request, object_pk):
        
        liked_objects = []
        user = self.request.user
        if user.is_authenticated():
            liked_objects = frozenset(user.liked_objects.values_list('pk', flat=True))
        for obj in all_objects_to_be_displayed_on_this_page:
            obj.liked = obj.pk in liked_objects
