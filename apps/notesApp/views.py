# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect, HttpResponse
from models import *
from django.core import serializers
from math  import floor,trunc
import datetime

total_posts=Note.objects.count()
# Create your views here.
def query_to_dict(queryset):
    d =[]
    di={}
    for note in queryset:
        di['note']=note.note
        di['created_at']=note.created_at
        di['id']=note.id
        d.append(di)   #append dictionary to list
        di={}          #clear dictionary because it wont work otherwise
    return d

def how_many_pages(num_posts):
    num_of_pages=trunc(num_posts/5)
    if num_posts%5 >0:
        num_of_pages+=1
    print "num of pages: ", num_of_pages
    pagesl=list(range(1,num_of_pages+1))
    pagesk=pagesl
    pagesd=dict(zip(pagesk,pagesl))
    return pagesd

def add_page_col(notes):
    i=1
    i_sub=0
    for n in notes:
        n['on_page']=i
        i_sub+=1
        if i_sub==5:
            i_sub=0
            i+=1
    return notes

def table(request):
    notesq=Note.objects.all()
    #5 notes per page will be displayed
    num_posts=len(notesq)
    pagesd=how_many_pages(num_posts)
    notes=query_to_dict(notesq)
    notes=add_page_col(notes)
    print notes, type(notes), "length: ",len(notes)

    context={'notes':notes,
            'pages':pagesd,
            }
    return render(request,'notes/table.html',context)

def select_page(request):
    print "select page called"
    print request.POST
    page_selected=int(request.POST['page_selected'])
    #print str(request.POST['notes_dict'])
    print page_selected
    #if str(request.POST['notes_dict'])!="null":
    try:
        print "trying"

        #notes=str(request.POST['notes_dict'])
        print notes
        print "trying"
        #notes=[dict(y.split(':') for y in notes.split(','))]
        #print notes
        #print "trying"
        num_posts=len(notes)
        print "trying"
        global total_posts
        total_posts=num_posts
        #5 notes per page will be displayed
        pagesd=how_many_pages(num_posts)
        print pagesd, type(pagesd), "length: ",len(pagesd)
        page_selected=1
        print "end of try"
    except:
        print "No other post data"
        notesq=Note.objects.all()
        num_posts=len(notesq)
        #5 notes per page will be displayed
        pagesd=how_many_pages(num_posts)
        notes=query_to_dict(notesq)
        notes=add_page_col(notes)
    #print notes
    #print pagesd
    context={'notes':notes,
            'pages':pagesd,
            'page_selected':page_selected  }
    return render(request,'notes/table_page.html',context)

def refresh_pagination(request):
    #notesq=Note.objects.all()
    #5 notes per page will be displayed
    #num_posts=len(notesq)
    global total_posts
    print "total_posts: ", total_posts
    pagesd=how_many_pages(total_posts)
    context={'pages':pagesd,
            }
    return render(request,'notes/new_pages.html',context)

def update_note(request):
    print "update note called"
    idTU=int(request.POST['idTU'])
    print idTU
    new_text=request.POST['noteTE']
    noteTU=Note.objects.get(id=idTU)
    noteTU.note=new_text
    noteTU.save()
    #update session??
    response="updated"
    return redirect('/table')

def delete2(request):
    idTD=int(request.POST['idTU'])
    noteTD=Note.objects.get(id=idTD)
    noteTD.delete()
    global total_posts
    total_posts=Note.objects.count()
    return redirect('/table')

def from_date(request):
    from_date=request.POST['from_date']
    print from_date, type(from_date)
    notesq=Note.objects.filter(created_at__gte=from_date)
    num_posts=len(notesq)
    global total_posts
    total_posts=num_posts
    #5 notes per page will be displayed
    pagesd=how_many_pages(num_posts)
    notes=query_to_dict(notesq)
    notes=add_page_col(notes)

    context={'notes':notes,
            'pages':pagesd,
            'page_selected':1 }
    return render(request,'notes/table_page.html',context)

def to_date(request):
    to_date=request.POST['to_date']
    notesq=Note.objects.filter(created_at__lte=to_date)
    num_posts=len(notesq)
    global total_posts
    total_posts=num_posts
    #5 notes per page will be displayed
    pagesd=how_many_pages(num_posts)
    notes=query_to_dict(notesq)
    #print notes
    notes=add_page_col(notes)

    context={'notes':notes,
            'pages':pagesd,
            'page_selected':1 }
    return render(request,'notes/table_page.html',context)


def add2(request):
    noteTA=request.POST['noteTA']
    Note.objects.create(note=noteTA)
    response="add successful"
    global total_posts
    total_posts=Note.objects.count()
    #update session ??
    print "total posts: ", total_posts
    return HttpResponse(response)

def delete(request):
    noteTD=Note.objects.get(id=request.POST['id'])
    noteTD.delete()
    print noteTD.note
    notes=Note.objects.all()
    context={'notes':notes}
    print notes
