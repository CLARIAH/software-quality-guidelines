from django.shortcuts import render
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings
from collections import OrderedDict
import re
import sys

def latextomarkdown(s):
    s = s.replace('\n',' ')
    s = re.sub(r'\\textbf{([A-Za-z0-9\s]*)}','**\\1**',s)
    s = re.sub(r'\\emph\{([^\}]+)\}','*\\1*',s)
    s = re.sub(r'\\textit\{([^\}]+)\}','*\\1*',s)
    s = re.sub(r'\\texttt\{([^\}]+)\}','``\\1``',s)
    s = re.sub(r'\\url\{([^\}]+)\}','\\1',s)
    s = re.sub(r'\\refcrit\{([^\}]+)\}','[**\\1**]',s)
    s = re.sub(r'\\refcrit\{([^\}]+)$','[**\\1**]',s)
    return s.replace('\\&','&')

def latextohtml(s):
    return s.replace('\\&','&amp;')

responseoptions = OrderedDict((('NA', 'Not applicable'), (0,'No'), (1,'Minimal'), (2,'Adequate'), (3,'Good'), (4,'Perfect')))


def requirement_is_relevant(requirementconstraints, supported, experimental):
    if supported and 'unsupported' in requirementconstraints:
        return False
    if not supported and 'supported' in requirementconstraints:
        return False
    if experimental and 'production' in requirementconstraints:
        return False
    if not experimental and 'experimental' in requirementconstraints:
        return False
    return True


def parsetexsource(texfile,supported=True,experimental=False):
    #args.storeconst, args.dataset, args.num, args.bar
    buffer = []

    criteria = OrderedDict()
    requirements = []
    category = None

    begincriteria = False
    beginrequirements = False
    requirementcode = requirementtext = ""
    requirementconstraints = []
    with open(texfile,'r',encoding='utf-8') as f:
        for line in f:
            if line.startswith('%BEGINCRITERIA'):
                begincriteria = True
            elif line.startswith('%ENDCRITERIA'):
                begincriteria = False
            if line.startswith('%BEGINREQUIREMENTS'):
                beginrequirements = True
            elif line.startswith('%ENDREQUIREMENTS'):
                if requirementtext and requirement_is_relevant(requirementconstraints,supported, experimental):
                    secondorder = requirementcode[-1] == requirementcode[-1].upper()
                    requirements.append( (latextomarkdown(requirementtext.strip('\n }')), secondorder) )
                beginrequirements = False
            elif line.startswith('\\subsection') and begincriteria:
                category = latextomarkdown(line[12:line.find('}')])
                criteria[category] = OrderedDict()
            elif line.startswith('\\criterion'):
                code = buffer[-2][buffer[-2].rfind('{')+1:-1]
                label = buffer[-1][buffer[-1].rfind('{')+1:-1]
                criteria[category][code] = {'label': latextomarkdown(label), 'response':None, 'comments': None}
            elif line.strip().startswith('\\newcommand') and beginrequirements:
                line = line.strip()
                if requirementtext and requirement_is_relevant(requirementconstraints,supported, experimental):
                    secondorder = requirementcode[-1] == requirementcode[-1].upper()
                    requirements.append( (latextomarkdown(requirementtext.strip('\n }')), secondorder) )
                requirementcode = line[line.find('{')+1:line.find('}')]
                requirementtext = line[line.find('}')+2:]
                requirementconstraints = []
            elif beginrequirements and requirementcode:
                line = line.strip()
                if line.startswith('%^-- '):
                    requirementconstraints = line[5:].strip().split(',')
                elif not line.startswith('%'):
                    if requirementtext: requirementtext += ' '
                    requirementtext += line
            else:
                buffer.append(line.strip())

    return criteria, requirements

def render_markdown(request, context):
    context_instance = RequestContext(request) if request else None
    data = render_to_string('survey_template.md', context, context_instance)
    data = '\n'.join([ line for line in data.split('\n') if line != '' ])
    return HttpResponse(data, content_type='text/markdown; charset=UTF-8')


def interactive_survey(request):
    if request.method == 'GET':
        criteria, requirements = parsetexsource(settings.TEXSOURCE, True,False)
        return render(request, 'interactive_survey.html', { 'criteria': criteria })
    elif request.method == 'POST':
        supported = (request.POST.get('supported',"1") == "1")
        experimental = (request.POST.get('experimental',"0") == 0)
        criteria, requirements = parsetexsource(settings.TEXSOURCE, supported,experimental)
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
        return render_markdown(request, { 'criteria': criteria, 'requirements': requirements, 'name': request.POST.get('name','unspecified'), 'version': request.POST.get('version','unspecified'),'experimental': experimental, 'supported': supported, 'responded':True })


def survey_template(request):
    return render_markdown(request, { 'criteria': parsetexsource(settings.TEXSOURCE),'responsed': False })

