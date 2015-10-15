# -*- coding: utf-8 -*-

from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Module
from .serializers import ModuleSerializer


class ModuleCreateView(viewsets.ModelViewSet):
    """
    API endpoint for creating a Module
    """
    serializer_class = ModuleSerializer
    permission_classes = (IsAuthenticated, )

class ModuleUpdateView(viewsets.ModelViewSet):
    """
    API endpoint for retrieve, update, destroy a Module
    """
    lookup_field = 'slug'
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = (IsAuthenticated, )
    

class ModuleReadView(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for retreive an Module
    """
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = 'slug'


class ModuleListView(generics.ListAPIView):
    """
    View to list all Modules in app
    """
    permission_classes = (IsAuthenticated, )
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    paginate_by = 100


"""Views for Forum wrap"""
from rest_framework.decorators import api_view, permission_classes
from forum.views import AskCreateView
from forum.models import Ask

from .models import Module, Forum_wrap
from django.http import Http404

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def module_forum_create_wrap(request, module):
    """
    wrap create Ask
    """
    try:
        module = Module.objects.get(slug=module)
        response = AskCreateView.as_view({'post':'create'})(request)
        
        ask = Ask.objects.get(pk=response.data['id'])
        Forum_wrap(module=module, ask=ask).save()
        
        return response

    except Module.DoesNotExist:
        raise Http404


from forum.models import Ask
from forum.serializers import ShortAskSerializer

class ForumList(generics.ListAPIView):
    """
    View to list all Ask in the foro.
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = ShortAskSerializer
    paginate_by = 10

    def get_queryset(self):
        module = Module.objects.get(slug=self.kwargs['module'])
        list_ask = Forum_wrap.objects.filter(module=module).values_list('ask', flat=True)
        asks = Ask.objects.filter(pk__in=list_ask)
        return asks


"""Views for Activitie wrap"""
from activitie.views import ActivitieParentCreateView
from activitie.models import ActivitieParent
from .models import Activitie_wrap

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def module_activitie_create_wrap(request, module):
    """
    wrap create Activitie Parent
    """
    try:
        module = Module.objects.get(slug=module)
        response = ActivitieParentCreateView.as_view({'post':'create'})(request)
        activitie = ActivitieParent.objects.get(pk=response.data['id'])
        
        Activitie_wrap(module=module, activitie=activitie).save()
        return response

    except Module.DoesNotExist:
        raise Http404


from activitie.serializers import ActivitieParentSerializer

class ActivitieList(generics.ListAPIView):
    """
    View to list all Activitites
    """
    permission_classes = (AllowAny,)
    serializer_class = ActivitieParentSerializer
    paginate_by = 10


    def get_queryset(self):
        module = Module.objects.get(slug=self.kwargs['module'])
        list_activities = Activitie_wrap.objects.filter(module=module).values_list('activitie', flat=True)
        activities = ActivitieParent.objects.filter(pk__in=list_activities)
        return activities


"""Views for Wiki wrap"""
#from .models import Wiki_wrap
#from waliki.rest.views import PageCreateView
from wiki.views import PageCreateView

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def module_wiki_create_wrap(request, module):
    """
    wrap create Wiki
    """
    print "create Wiki"
    try:
        module = Module.objects.get(slug=module)
        print module

        response = PageCreateView.as_view()(request)
        print response.data
        #ask = Ask.objects.get(pk=response.data['id'])
        #Forum_wrap(module=module, ask=ask).save()
        
        return response

    except Module.DoesNotExist:
        raise Http404