from django.db import models


class Project(models.Model):
    description = models.CharField(max_length=80)


class DataEntry(models.Model):
    # TODO: Add some properties here e.g. cardinality, optional
    name = models.CharField(max_length=80)
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        default=-1,
    )


class DataEntryPair(models.Model):
    parent = models.ForeignKey(
        'DataEntry',
        related_name='parent',
        on_delete=models.CASCADE,
    )
    child = models.ForeignKey(
        'DataEntry',
        related_name='child',
        on_delete=models.CASCADE,
    )
