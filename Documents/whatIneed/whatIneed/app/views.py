from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator

from app.forms import EventForm, ItemFormSet
from app.models import Event, Inscription, Item, UserBringItem


def landing_page(request):
    return render(request, template_name="win/landing_page.html")


@login_required()
def event(request, slug):
    event = get_object_or_404(Event, slug=slug)
    items = event.items.all()
    return render(
        request,
        template_name="win/event/index.html",
        context={
            # TODO: Create a proxy model
            "items": [i.load_contributions_of_user(request.user) for i in items],
            "participants": event.participants.all(),
            "event": event,
            "is_participant": request.user in event.participants.all(),
            "is_admin": event.admin == request.user
        }
    )


@login_required()
def go_to(request, slug):
    event = get_object_or_404(Event, slug=slug)
    inscription = Inscription(
        user=request.user,
        event=event,
        date_time=datetime.now()
    )
    inscription.save()
    event.inscription_set.add(inscription)
    event.save()
    messages.add_message(
        request,
        messages.SUCCESS,
        "You're have successfully joined this event ! Tell the others what you'll bring !",
        extra_tags='go_to'
    )
    return HttpResponseRedirect(reverse("show-event", kwargs={"slug": slug}))


@login_required()
def dashboard(request):
    return render(
        request,
        template_name="win/dashboard/index.html",
        context={
            "admin_of": request.user.admin_of.all(),
            "goes_to": request.user.goes_to.all()
        }
    )


@method_decorator(login_required, name='dispatch')
class EventCreate(CreateView):
    model = Event
    form_class = EventForm
    template_name = "win/event/create.html"

    def form_valid(self, form):
        """
        Adds the current user as the admin
        """
        form.instance.admin = self.request.user
        form.save()
        return HttpResponseRedirect(reverse("show-event", kwargs={"slug": form.instance.slug}))


class EventUpdate(UpdateView):
    model = Event
    form_class = EventForm
    template_name = "win/event/create.html"


class Items(TemplateView):
    template_name = "win/items/create.html"

    def get(self, request, *args, **kwargs):
        event = Event.objects.get(slug=self.kwargs["slug"])
        form = ItemFormSet(instance=event)
        return render(request, self.template_name, {'formset': form})

    def post(self, request, *args, **kwargs):
        event = Event.objects.get(slug=self.kwargs["slug"])
        form = ItemFormSet(request.POST, instance=event)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("show-event", kwargs={"slug": self.kwargs["slug"]}))
        else:
            return render(request, self.template_name, {'formset': form})


class BringItems(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        event = get_object_or_404(Event, slug=self.kwargs["slug"])
        item = get_object_or_404(Item, id=self.kwargs["item_id"])
        qty = float(request.POST.get("qty"))

        if event.participants.filter(id=request.user.id).exists():

            qty_left = item.qty_left_to_bring()

            if qty > qty_left:
                qty = qty_left

            user_brings_item, _ = UserBringItem.objects.get_or_create(
                item=item,
                user=request.user
            )

            if qty == 0:
                user_brings_item.delete()
            else:
                user_brings_item.qty = qty
                user_brings_item.date_time = datetime.now()
                user_brings_item.save()

            return HttpResponseRedirect(
                reverse("show-event", kwargs={"slug": self.kwargs["slug"]})
            )
        else:
            return HttpResponseForbidden()
