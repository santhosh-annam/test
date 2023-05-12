from django.conf.urls import url
from ebanking.views import RegistrationView
from ebanking.views import CSPViolationView

urlpatterns = [
    url(r'^eregister/', RegistrationView.as_view()),
    url(r'^csp-violation-report/', CSPViolationView.as_view()),
]
