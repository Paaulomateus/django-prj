from django.shortcuts import render
from contact.models import Contact
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.core.paginator import Paginator

def index(request):
    contacts  = Contact.objects.filter(show=True).order_by('-id')

    paginator = Paginator(contacts, 5)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'site_title':'Contatos - '
    }
    return render(
        request,
        'contact/index.html',
        context
    )

def search(request):
    search_value = request.GET.get('q', '').strip()

    if search_value == '':
        return redirect('contact:index')
    
    contacts  = Contact.objects\
        .filter(show=True)\
        .filter(
            Q(nome__icontains=search_value) |
            Q(sobrenome__icontains=search_value) |
            Q(telefone__icontains=search_value) |
            Q(email__icontains=search_value) 
        )\
        .order_by('-id')
    
    paginator = Paginator(contacts, 5)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
        
    context = {
        'page_obj':page_obj,
        'site_title':'Search - ',
        'search_value': search_value
    }
    return render(
        request,
        'contact/index.html',
        context
    )


def contact(request, contact_id):
    # single_contact  = Contact.objects.get(pk=contact_id)
    single_contact = get_object_or_404(Contact, pk=contact_id, show=True)
    site_title = f'{single_contact.nome} {single_contact.sobrenome}'

    
    context = {
        'contact':single_contact,
        'site_title':site_title
    }
    return render(
        request,
        'contact/contact.html',
        context
    )