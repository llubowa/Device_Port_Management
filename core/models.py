from django.db import models

# Create your models here.

class CoreHubPorts(models.Model):
    ip_address = models.CharField(primary_key=True, max_length=255)
    port = models.CharField(max_length=255)
    port_type = models.TextField(db_column='Port_Type', blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    status = models.TextField(db_column='Status', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'core_hub_ports'
        unique_together = (('ip_address', 'port'),)