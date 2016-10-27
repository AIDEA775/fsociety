from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Document
import os


@login_required
def list(request):
    """Create a new document file"""
    title = request.POST.get('title')
    document_file = request.FILES.get('document_file')
    description = request.POST.get('description')
    author = request.user

    if all([title, document_file]):
        new_doc = Document(title=title,
                           document_file=document_file,
                           description=description,
                           author=author)
        new_doc.save()

    documents = Document.objects.all()
    context = {'documents': documents}
    return render(request, "video/list.html", context)


@login_required
def video_delete(request):
    try:
        video = Document.objects.get(id=request.GET['id'])
        video.delete()
    except(KeyError, Document.DoesNotExist):
        return redirect('video:my_videos')
    return redirect('video:my_videos')
    
    
@login_required
def my_videos(request):
    videos = Document.objects.filter(author=request.user)
    context = {'videos': videos}
    return render(request, "video/my_videos.html", context)
