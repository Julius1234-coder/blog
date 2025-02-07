
from django.contrib import messages
from django.contrib.auth.mixins  import(
    LoginRequiredMixin,
)


from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404


from django.views import generic 
from groups.models import Group,GroupMember
from . import models 
# Create your views here.

class CreateGroup(LoginRequiredMixin,generic.CreateView):
    fields = ("name", "description")
    model = Group 
class SingleGroup(generic.DetailView):
    model = Group 

class ListGroup(generic.ListView):
    model = Group

class JoinGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse("groups:single", kwargs = {"slug": self.kwargs.get("slug")})
    
    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug = self.kwargs.get("slug"))
        try:
            GroupMember.objects.create(user = self.request.user, group=group)
        except models.GroupMember.DoesNotExist:
            messages.warning(
                self.request,("Advertencia, ya eres miembro de {}". format(group.name)))
                
        else:
            messages.success(
                self.request,"Ahora eres miembro de {}".format(group.name))
        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse("groups:single", kwargs = {"slug": self.kwargs.get("slug")})
    
    def get(self, request, *args, **kwargs):
        try:
            memebership = models.GroupMember.objects.filter(
                user = self.request.user,
                group__slug = self.kwargs.get("slug")
            ).get()
        except models.GroupMember.DoesNotExist:
            messages.warning(
                self.request,
                "No puedes salir del grupo porque no perteneces a el"
            )
        else:
            memebership.delete()
            messages.success(
                self.request,
                self.request,
                "Haz salido exitosamente al grupo"
            )
        return super().get(request, *args, **kwargs)
        

