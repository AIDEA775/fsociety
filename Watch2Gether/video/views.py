from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Document
from django.conf import settings
import os


# @login_required
# def list(request):
#     # Handle file upload
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             newdoc = Document(docfile=request.FILES['docfile'])
#             newdoc.save()
#             # Redirect to the document list after POST
#             return HttpResponseRedirect(reverse('video:list'))
#     else:
#         form = DocumentForm()  # A empty, unbound form
#
#     # Load documents for the list page
#     documents = Document.objects.all()
#
#     # Render list page with the documents and the form
#     context = {'documents': documents, 'form': form}
#     return render(request, "video/list.html", context)


@login_required
def list(request):
    """Create a new document file"""
    name = request.POST.get('name')
    docfile = request.FILES.get('docfile')
    description = request.POST.get('description')
    if all([name, docfile]):
        newdoc = Document(name=name, docfile=docfile, description=description)
        newdoc.save()

    documents = Document.objects.all()
    context = {'documents' : documents}
    return render(request, "video/list.html", context)

@login_required
def delete(self, *args, **kwargs):
    os.remove(os.path.join(settings.MEDIA_ROOT, self.docfile.name))
    super(Document, self).delete(*args, **kwargs)
