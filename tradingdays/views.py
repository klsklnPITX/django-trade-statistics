from accounts.models import Account
from django.db.models import query
from django.views import generic
from django.shortcuts import redirect, reverse, render, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
from django.conf import settings

from .models import TradingDay
from .forms import CustomUserCreationForm, TradingDayModelForm, CustomUserCreationForm, CsvUploadForm
from .modules.tradingdays_modules import parse_csv_file, allowed_file, delete_previous_account_data


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
        return TradingDay.objects.filter(user=user).order_by("date_created")


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
def upload_csv_view(request):
    if request.method == "POST":
        form = CsvUploadForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            account = request.POST["account"]
            if allowed_file(file):
                if "check_delete_account_data" in request.POST:
                    # Delete previous account data
                    delete_previous_account_data(request, account)
                parse_csv_file(file, account, request.user)
                return redirect("tradingdays:tradingday-list")
            else:
                return upload_csv_error_view(request, "Filetype not allowed")
        else:
            form = CsvUploadForm()
        return render(request, "tradingdays/csv_upload.html", {"form": form})

    if request.method == "GET":
        form = CsvUploadForm(user=request.user)
        return render(request, "tradingdays/csv_upload.html", {"form": form})


def upload_csv_error_view(request, errors):
    return render(request, "tradingdays/csv_error.html", {"errors": errors})
