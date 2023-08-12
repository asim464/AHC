from django.db import models


class Hierarchy(models.Model):
    LEVEL_FIRST = 1
    LEVEL_OTHER = 2

    LEVEL_CHOICES = (
        (LEVEL_FIRST, 1),
        (LEVEL_OTHER, 2),
    )

    child = models.ForeignKey('GHQOrganization', related_name='+', blank=True, null=True, on_delete=models.CASCADE)
    parent = models.ForeignKey('GHQOrganization', related_name='children', blank=True, null=True, on_delete=models.CASCADE)
    level = models.IntegerField(default=LEVEL_FIRST, choices=LEVEL_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('GHQUser', related_name='+', blank=True, null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('GHQUser', related_name='+', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.child} {self.parent}'
