from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from . import plots


class IndexView(TemplateView):
    template_name = "plot_index.html"


# class StuffView(TemplateView):
#     template_name = "stuff.html"
#
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super(StuffView, self).get_context_data(**kwargs)
#         username = self.request.user.username
#         context['plot'] = plots.stuff_plot(username)
#         return context
#

def stuff_vew(request):
    if request.method == 'GET':
        return render(request, 'stuff.html')
    username = request.user.username
    graphJason = plots.stuff_plot(username)
    return render(request, 'stuff.html', {'plot':graphJason})


