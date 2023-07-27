from django.db import models
from django.utils.translation import gettext as _

# Create your models here.
class AggregationHubs(models.Model):
    ip_address = models.CharField(primary_key=True, max_length=255)
    port = models.CharField(max_length=255)
    port_type = models.TextField(db_column='Port_Type', blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    status = models.TextField(db_column='Status', blank=True, null=True)  # Field name made lowercase.



    class Meta:
        managed = False
        db_table = 'aggregation_hubs'
        unique_together = (('ip_address', 'port'),)

# Aggregation huh IPs
class AggregationIps(models.Model):
    ip_address = models.CharField(primary_key=True, max_length=255)
    hub_name = models.TextField(db_column='Hub_name', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aggregation_ips'

#CASCADED
class CascAggIps(models.Model):
    ip_address = models.CharField(db_column='IP_Address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cascaded = models.TextField(db_column='Cascaded', blank=True, null=True)  # Field name made lowercase.
    cascade_no = models.CharField(db_column='Cascade_No', primary_key=True, max_length=255)  # Field name made lowercase.
    agg_ip = models.CharField(db_column='Agg_Ip', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'casc_agg_ips'
        unique_together = (('cascade_no', 'agg_ip'),)


class CascadedHubs(models.Model):
    ip_address = models.CharField(primary_key=True, max_length=255)
    port = models.CharField(max_length=255)
    port_type = models.TextField(db_column='Port_Type', blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    status = models.TextField(db_column='Status', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cascaded_hubs'
        unique_together = (('ip_address', 'port'),)


class CascadedIps(models.Model):
    ip_address = models.CharField(primary_key=True, max_length=255)
    cascaded = models.TextField(db_column='Cascaded', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cascaded_ips'