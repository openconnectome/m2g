#!/usr/bin/python
"""
@author: Disa Mhembere
@organization: Johns Hopkins University
@contact: disa@jhu.edu

@summary: A module to alter/update the MRdjango database as necessary
"""

'''
FileField stores files e.g. to media/documents based MEDIA_ROOT
Generally, each model maps to a single database table.
'''
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
import os
from time import strftime, localtime

class BuildGraphModel(models.Model):
  '''
  Allows us to store data on build graph view
  '''
  project_name = models.CharField(max_length=255)
  site = models.CharField(max_length=255,)
  subject = models.CharField(max_length=255,)
  session = models.CharField(max_length=255,)
  scanId = models.CharField(max_length=255)
  location = models.TextField()
  owner = models.ForeignKey(to=User, to_field='username', null=True) # Many-to-one .Many here, other in auth_user

  def __repr__(self):
    _repr = '\n' + "project_name: " + str(self.project_name) + '\n' + \
            "site: " + str(self.site) + '\n' + \
            "subject: " + str(self.subject) + '\n' + \
            "session: " + str(self.session) + '\n' + \
            "scanId: " + str(self.scanId) + '\n' + \
            "location: " + str(self.location) + '\n' + \
            "owner: " + str(self.owner) + '\n'

    return super(BuildGraphModel, self).__repr__() + _repr


class OwnedProjects(models.Model):
  '''
  This will let us keep track of owned projects for
  integrity constraints & sharing
  '''
  project_name = models.CharField(max_length=255)
  owner = models.ForeignKey(User, 'username') # Many-to-one .Many here, other in auth_user
  is_private = models.BooleanField(null=False)
  owner_group = models.CharField(max_length=255, null=True) # Will reference other table soon
  # Really should be --> owner_groups = models.ForeignKey(to=User, to_field='groups')

class SharingTokens(models.Model):
  '''
  Class to allow you to create a project sharing token
  that allows a user to let others see a private project.
  '''
  token = models.CharField(max_length=64)
  issued_by = models.ForeignKey(User, 'username') # Many-to-one . Many here, other in auth_user
  project_name = models.ManyToManyRel(to=BuildGraphModel, related_name='project_name')
  issue_date = models.DateTimeField(auto_now_add=True)
  expire_date = models.DateField(null=True)

class GraphDownloadModel(models.Model):

  filepath = models.CharField(max_length=1024, null=False)
  genus = models.CharField(max_length=128)
  region = models.CharField(max_length=128)
  numvertex = models.BigIntegerField(null=False)
  numedge = models.BigIntegerField(null=False)
  graphattr = models.TextField() # I will use JSON encoded string to store
  vertexattr = models.TextField()
  edgeattr = models.TextField()
  sensor = models.CharField(max_length=128)
  source = models.CharField(max_length=256)
  mtime = models.FloatField() # Modification Time
  url = models.URLField(max_length=2048)


class Person(models.Model):
  # For tutorial
  name = models.CharField(verbose_name="full name", max_length=256)


admin.site.register(BuildGraphModel)
admin.site.register(OwnedProjects)
admin.site.register(SharingTokens)
