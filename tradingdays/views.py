from accounts.models import Account
from django.db.models import query
from django.views import generic
from django.shortcuts import reverse, render, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
from django.conf import settings

from .models import TradingDay
from .forms import CustomUserCreationForm, TradingDayModelForm, CustomUserCreationForm, CsvUploadForm
from .modules.tradingdays_modules import parse_csv_file


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(generic.TemplateView):
    template_name = "landing.html"


class TradingDayListView(LoginRequiredMixin, generic.ListView):
    template_name = "tradingdays/tradingday-list.html"
    context_object_name = "tradingdays"

    def get_queryset(self):
        user = self.request.user
        return TradingDay.objects.filter(user=user)


class TradingDayCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "tradingdays/tradingday_create.html"
    form_class = TradingDayModelForm

    def get_form_kwargs(self):
        kwargs = super(TradingDayCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse("tradingdays:tradingday-list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.user = self.request.user
        user.save()
        return super(TradingDayCreateView, self).form_valid(form)


class TradingDayDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "tradingdays/tradingday_detail.html"

    def get_queryset(self):
        return TradingDay.objects.all()


class TradingDayUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "tradingdays/tradingday_update.html"
    form_class = TradingDayModelForm

    def get_form_kwargs(self):
        kwargs = super(TradingDayUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse("tradingdays:tradingday-list")

    def get_queryset(self):
        return TradingDay.objects.all()


class TradingDayDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "tradingdays/tradingday_delete.html"
    queryset = TradingDay.objects.all()

    def get_success_url(self):
        return reverse("tradingdays:tradingday-list")


# CSV File upload an parse
def upload_csv(request):
    if request.method == "POST":
        form = CsvUploadForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            parse_csv_file(request.FILES["file"])
            return HttpResponse("ok", status=200)
        else:
            form = CsvUploadForm()
        return render(request, "tradingdays/csv_upload.html", {"form": form})

    if request.method == "GET":
        form = CsvUploadForm(user=request.user)
        return render(request, "tradingdays/csv_upload.html", {"form": form})
