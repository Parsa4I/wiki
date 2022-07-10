from django.shortcuts import render
from markdown2 import markdown
from pathlib import Path
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import random
import os
from . import util


def index(request):
    if request.method == 'POST':
        qlist = []
        for entry in util.list_entries():
            if request.POST['q'].lower() == entry.lower():
                return HttpResponseRedirect(f'/wiki/{entry}')
            if request.POST['q'].lower() in entry.lower():
                qlist.append(entry)
        return render(request, "encyclopedia/index.html", {
            "entries": qlist,
            'h': 'Search Results'
        })

    abc = 'ABCDEFGHIJKLMNOPQRSTUVQXYZ'
    entries = list(util.list_entries())
    entries.sort(key=str.lower)
    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        'h': 'All Pages',
        'entry_num': len(entries),
        'abc': abc
    })

def entry(request, title):
    if request.method == 'POST':
        if 'edit' in request.POST:
            return edit_entry(request, title, util.get_entry(title))
        elif 'delete' in request.POST:
            os.remove(f'entries/{title}.md')
            return HttpResponseRedirect('/')
        elif 'save' in request.POST:
            util.save_entry(request.POST['title'], request.POST['content'])
            return HttpResponseRedirect(f'/wiki/{request.POST["title"]}')
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(f'/wiki/{request.POST["title"]}')
    else:
        if util.get_entry(title):
            entry = str(util.get_entry(title))
            entry = markdown(entry)
            return render(request, 'encyclopedia/entry.html', {
                'title': title,
                'entry': entry
            })
        else:
            return render(request, 'encyclopedia/error.html', {
                'error': f'There is no entry with the title "{title}".'
            })

def newpage(request):
    if request.method == 'POST': 
        if 'save' in request.POST:
            if request.POST['title'].lower() in map(lambda a: a.lower(), util.list_entries()):
                return render(request, 'encyclopedia/error.html', {
                    'title': request.POST['title'],
                    'error': f'An entry with the title "{request.POST["title"]}" already exists.'
                })
            else:
                util.save_entry(request.POST['title'], request.POST['content'])
                return HttpResponseRedirect(f'/wiki/{request.POST["title"]}')
        elif 'cancel' in request.POST:
            return HttpResponseRedirect('/wiki')
    else:
        return render(request, 'encyclopedia/newpage.html')

def randent(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return HttpResponseRedirect(f'/wiki/{random_entry}')

def edit_entry(request, title, content):
    return render(request, 'encyclopedia/editentry.html', {
        'title': title, 'content': content
    })

def abc(request, abc):
    entries = list(util.list_entries())
    abc_entries = []
    for entry in entries:
        if entry[0].upper() == abc:
            abc_entries.append(entry)

    return render(request, 'encyclopedia/abc.html', {
        'abc': abc,
        'entries': abc_entries
    })
