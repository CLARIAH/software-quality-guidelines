from django.shortcuts import render
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings
from collections import OrderedDict
import sys

def latextomarkdown(s):
    return s.replace('\\&','&')

def latextohtml(s):
    return s.replace('\\&','&amp;')

responseoptions = OrderedDict((('NA', 'Not applicable'), (0,'No'), (1,'Minimal'), (2,'Adequate'), (3,'Good'), (4,'Perfect')))


def parsetexsource(texfile):
    #args.storeconst, args.dataset, args.num, args.bar
    buffer = []

    criteria = OrderedDict()
    category = None

    begincriteria = False
    with open(texfile,'r',encoding='utf-8') as f:
        for line in f:
            if line.startswith('%BEGINCRITERIA'):
                begincriteria = True
            elif line.startswith('%ENDCRITERIA'):
                begincriteria = False
            elif line.startswith('\\subsection') and begincriteria:
                category = latextomarkdown(line[12:line.find('}')])
                criteria[category] = OrderedDict()
            elif line.startswith('\\criterion'):
                code = buffer[-2][buffer[-2].rfind('{')+1:-1]
                label = buffer[-1][buffer[-1].rfind('{')+1:-1]
                criteria[category][code] = {'label': latextomarkdown(label), 'response':None, 'comments': None}
            else:
                buffer.append(line.strip())

    return criteria

def render_markdown(request, context):
    context_instance = RequestContext(request) if request else None
    data = render_to_string('survey_template.md', context, context_instance)
    data = '\n'.join([ line for line in data.split('\n') if line != '' ])
    return HttpResponse(data, content_type='text/markdown; charset=UTF-8')


def interactive_survey(request):
    if request.method == 'GET':
        return render(request, 'interactive_survey.html', { 'criteria': parsetexsource(settings.TEXSOURCE) })
    elif request.method == 'POST':
        criteria = parsetexsource(settings.TEXSOURCE)
        for categorydata in criteria.values():
            for code, itemdata in categorydata.items():
                if code in request.POST:
                    if settings.DEBUG: print("found response",file=sys.stderr)
                    key = int(request.POST[code]) if request.POST[code].isnumeric() else request.POST[code]
                    if key in responseoptions:
                        itemdata['response'] = responseoptions[key]
                    else:
                        raise KeyError(key)
                if 'comments_'+code in request.POST:
                    itemdata['comments'] = request.POST['comments_'+code]
        return render_markdown(request, { 'criteria': criteria, 'responded':True })


def survey_template(request):
    return render_markdown(request, { 'criteria': parsetexsource(settings.TEXSOURCE),'responsed': False })

