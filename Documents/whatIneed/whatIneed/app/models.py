from autoslug import AutoSlugField
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Event(models.Model):
    name = models.CharField(max_length=200)
    date_time = models.DateTimeField()
    description = models.TextField()
    admin = models.ForeignKey(User, related_name="admin_of")
    participants = models.ManyToManyField(User, through='Inscription', related_name='goes_to')
    # items = models.ManyToManyField('Item')
    # location = models.PointField()
    address = models.CharField(max_length=60, default="")
    slug = AutoSlugField(
        populate_from='name',
        unique=True
    )

    def __str__(self):
        return "%s | %s" % (self.name, self.slug)


class Inscription(models.Model):
    date_time = models.DateTimeField()
    user = models.ForeignKey(User)
    event = models.ForeignKey('Event')

    def __str__(self):
        return str(self.user) + " : " + str(self.event)


class UserBringItem(models.Model):
    date_time = models.DateTimeField(null=True)
    user = models.ForeignKey(User)
    item = models.ForeignKey('Item', related_name="contributions")
    qty = models.DecimalField(max_digits=10, decimal_places=1, default=0)

    def __str__(self):
        return str(self.user) + " : " + str(self.item)


class Item(models.Model):
    name = models.CharField(max_length=30)
    qty = models.DecimalField(max_digits=10, decimal_places=1)
    unit = models.CharField(max_length=10)
    event = models.ForeignKey(to='Event', related_name="items", null=True)
    category = models.ForeignKey(to='ItemCategory', related_name='items', null=True)

    def qty_left_to_bring(self):
        qty_taken = UserBringItem.objects.filter(item=self).aggregate(Sum('qty'))
        sum = 0
        if qty_taken["qty__sum"] is not None:
            sum = qty_taken["qty__sum"]
        return self.qty - sum

    def qty_taken(self):
        return self.qty - self.qty_left_to_bring()

    def load_contributions_of_user(self, user):
        self.user_contrib = UserBringItem.objects.filter(item=self, user=user).first()
        return self

    def __str__(self):
        return self.name


class ItemCategory(models.Model):
    name = models.CharField(max_length=20)
    emoji_code = models.CharField(max_length=2,null=True)

    def __str__(self):
        return self.name
