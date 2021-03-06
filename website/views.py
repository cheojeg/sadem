#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import simplejson as json
import json as js_parser
from django.shortcuts import render, render_to_response
from django.urls import reverse
from django.conf.urls import url
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core import serializers
from detection.models import Detection
from dgii.models import Marbete
from agents.models import Agent

from .forms import UserForm


# Create your views here.
def index(request):
	return render(request, 'index.html', {})


@csrf_protect
def login_user(request):
	logout(request)
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('detection_list'))

	username = password = ''
	form = UserForm(request.POST or None)
	if request.POST and str(request.POST['username']) and \
		(request.POST['password']):
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse('detection_list'))
		else:
			messages.error(request, 'Usuario o contraseña \
				incorrecta. Verifique.')

	return render(request, 'website/login.html', {'form': form})


def logout_user(request):
	logout(request)
	return HttpResponseRedirect(reverse('login_user'))


def map(request, agent_id=False):
	if agent_id:
		detections = Detection.objects.filter(agent_id=agent_id)
	else:
		detections = Detection.objects.all()
	detections_json = serializers.serialize("json", detections)
	mod_dectections = js_parser.loads(detections_json)
	for d in mod_dectections:
		detection = Detection.objects.filter(marbete_id=d['fields']['marbete_id'])
		d['fields']['license_plate'] = detection[0].marbete_id.license_plate
		d['fields']['owner'] = detection[0].marbete_id.owner
		d['fields']['time'] = detection[0].created.strftime("%d-%m-%Y %H:%M:%S")
		d['fields']['agent'] = detection[0].agent_id.first_name + ' ' + detection[0].agent_id.last_name
		d['fields']['agent_number'] = detection[0].agent_id.agent_number
		d['fields']['capture_img'] = 'http://127.0.0.1:8000/media/' + str(detection[0].photo)
		d['fields']['identificacion'] = str(detection[0].id)
	detections_json = js_parser.dumps(mod_dectections, ensure_ascii=False)
	agents = Agent.objects.all()

	return render(request, 'website/map.html', {'detections': detections_json, 'agents':agents, 'current_agent':agent_id})


@csrf_protect
def detection_list(request):
	detection_list = Detection.objects.all()

	return render(request, 'website/events.html',
		{'detection_list': detection_list})
