from django.db import models


class ServingStatus(models.Model):
    name = models.CharField(max_length=255)

    created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='+')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'
