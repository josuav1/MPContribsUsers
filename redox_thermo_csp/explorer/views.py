"""This module provides the views for the redox_thermo_csp explorer interface."""

import os
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from mpcontribs.rest.views import get_endpoint
from mpcontribs.io.core.components import render_dataframe
from mpcontribs.io.core.recdict import render_dict
from test_site.settings import STATIC_URL, DEBUG
from webtzite.models import RegisteredUser

access_msg = 'Coming Soon! Contact <a href="mailto:josua.vieten@dlr.de">J. Vieten</a> to request pre-publication access.'

def index(request):
    ctx = RequestContext(request)
    if request.user.is_authenticated():
        user = RegisteredUser.objects.get(username=request.user.username)
        if user.groups.filter(name='redox_thermo_csp').exists():
            ctx['static_url'] = STATIC_URL
            if DEBUG:
                mod = os.path.dirname(__file__).split(os.sep)[-2]
                ctx['static_url'] = '_'.join([STATIC_URL[:-1], mod])
        else:
            ctx.update({'alert': access_msg})
    else:
        return redirect('{}?next={}'.format(reverse('cas_ng_login'), request.path))
    return render_to_response("redox_thermo_csp_explorer_index.html", ctx)

def isographs(request):
    ctx = RequestContext(request)
    if request.user.is_authenticated():
        user = RegisteredUser.objects.get(username=request.user.username)
        if user.groups.filter(name='redox_thermo_csp').exists():
            from ..rest.rester import RedoxThermoCspRester
            with RedoxThermoCspRester(user.api_key, endpoint=get_endpoint(request)) as mpr:
                try:
                    prov = mpr.get_provenance()
                    ctx['title'] = prov.pop('title')
                    ctx['provenance'] = render_dict(prov, webapp=True)
                    df = mpr.get_contributions()
                    url = request.build_absolute_uri(request.path) + 'rest/table'
                    ctx['table'] = render_dataframe(
                        df, webapp=True,
                        #url=url, total_records=mpr.count()
                    )
                except Exception as ex:
                    ctx.update({'alert': str(ex)})
        else:
            ctx.update({'alert': access_msg})
    else:
        return redirect('{}?next={}'.format(reverse('cas_ng_login'), request.path))
    return render_to_response("redox_thermo_csp_explorer_isographs.html", ctx)

def energy_analysis(request):
    ctx = RequestContext(request)
    if request.user.is_authenticated():
        user = RegisteredUser.objects.get(username=request.user.username)
        if user.groups.filter(name='redox_thermo_csp').exists():
            ctx['static_url'] = STATIC_URL
            if DEBUG:
                mod = os.path.dirname(__file__).split(os.sep)[-2]
                ctx['static_url'] = '_'.join([STATIC_URL[:-1], mod])
        else:
            ctx.update({'alert': access_msg})
    else:
        return redirect('{}?next={}'.format(reverse('cas_ng_login'), request.path))
    return render_to_response("redox_thermo_csp_explorer_energy_analysis.html", ctx)

def documentation(request):
    ctx = RequestContext(request)
    if request.user.is_authenticated():
        user = RegisteredUser.objects.get(username=request.user.username)
        if user.groups.filter(name='redox_thermo_csp').exists():
            ctx['static_url'] = STATIC_URL
            if DEBUG:
                mod = os.path.dirname(__file__).split(os.sep)[-2]
                ctx['static_url'] = '_'.join([STATIC_URL[:-1], mod])
        else:
            ctx.update({'alert': access_msg})
    else:
        return redirect('{}?next={}'.format(reverse('cas_ng_login'), request.path))
    return render_to_response("redox_thermo_csp_explorer_documentation.html", ctx)

def tolerance_factors(request):
    ctx = RequestContext(request)
    if request.user.is_authenticated():
        user = RegisteredUser.objects.get(username=request.user.username)
        from ..rest.rester import RedoxThermoCspRester
        with RedoxThermoCspRester(user.api_key, endpoint=get_endpoint(request)) as mpr:
            try:
                ionic_radii = render_dataframe(mpr.get_ionic_radii(), webapp=True)
            except Exception as ex:
                ctx.update({'alert': str(ex)})
    else:
        return redirect('{}?next={}'.format(reverse('cas_ng_login'), request.path))
    return render_to_response("redox_thermo_csp_explorer_tolerance_factors.html", ctx)