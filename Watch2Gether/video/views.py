from django.shortcuts import render
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
def delete(self, *args, **kwargs):
    os.remove(os.path.join(settings.MEDIA_ROOT, self.document_file.name))
    super(Document, self).delete(*args, **kwargs)
