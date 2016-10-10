from django.shortcuts import render,HttpResponse
# Create your views here.
from Log import logHandle


def test(request):

	a = logHandle.test()

	return HttpResponse(a)