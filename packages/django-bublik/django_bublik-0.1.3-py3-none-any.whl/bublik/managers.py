from datetime import timedelta

from django.db import models
from django.utils.timezone import now


def is_confirmed(confirm_text='Are you sure?') -> bool:
    for confirmation_text in (confirm_text, 'Really!?!'):
        answer = ''
        while answer not in ('y', 'n'):
            answer = input(f'{confirmation_text} [y,Y,n,N] ').lower()
        if answer == 'n':
            return False

    return True


class RecentQuerySet(models.QuerySet):
    def delete(self):
        if not is_confirmed():
            return

        if 'is_removed' in (f.name for f in self.model._meta.get_fields()):
            return self.update(is_removed=True)

        return super().delete()


class RecentManager(models.Manager):

    def count(self):
        raise NotImplementedError

    def exists(self):
        raise NotImplementedError

    def get_queryset(self):
        return RecentQuerySet(self.model, using=self._db)

    def all(self, m=None, h=None, d=None):
        """
        :param m: minutes
        :param h: hours
        :param d: days
        :return: QuerySet
        """

        if not m and not h and not d:
            m = 10

        assert sum([bool(v) for v in [m, h, d]]) == 1

        if h:
            m = h * 60
        if d:
            m = d * 24 * 60

        return self.get_queryset().filter(created_at__gt=now() - timedelta(minutes=m))

    def first(self, *args, **kwargs):
        return self.all(*args, **kwargs).order_by('created_at').first()

    def last(self, *args, **kwargs):
        return self.all(*args, **kwargs).order_by('created_at').last()
