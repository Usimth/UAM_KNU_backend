from django.db import models

from apps.accounts.models import User
from apps.vertiports.models import Vertiport


class State(models.Model):
    sequence = models.IntegerField(default=0, null=False, blank=False)
    datetime = models.DateTimeField(auto_now=True, null=False, blank=False)
    fato_in_UAM = models.SmallIntegerField(default=0, null=False, blank=False)
    path_in_UAM = models.SmallIntegerField(default=0, null=False, blank=False)
    gate_UAM = models.SmallIntegerField(default=0, null=False, blank=False)
    path_out_UAM = models.SmallIntegerField(default=0, null=False, blank=False)
    fato_out_UAM = models.SmallIntegerField(default=0, null=False, blank=False)
    gate_UAM_psg = models.SmallIntegerField(default=0, null=False, blank=False)
    waiting_room_psg = models.SmallIntegerField(default=0, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vertiport = models.ForeignKey(Vertiport, on_delete=models.CASCADE)

    class Meta:
        # 다중 기본키 설정
        constraints = [
            models.UniqueConstraint(fields=['sequence', 'user', 'vertiport'], name='composite primary key'),
        ]
        # DB 테이블 이름
        db_table = 'state'

    def __str__(self):
        return f'{self.vertiport.name}.{self.sequence}'
