from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView
from rest_framework.response import Response
from core.serializers import TransactionSerializer
from .forms import NewTransactionForm
from .models import Transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from rest_framework.generics import ListAPIView
from django.db.models import Sum
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

# View list of transactions
class IndexView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'index.html'
    context_object_name = 'transactions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Calculate the sum of amounts for repaid and unpaid transactions
        repaid_sum = Transaction.objects.filter(user=self.request.user, repayment=True).aggregate(total=Sum('amount'))['total'] or 0
        unpaid_sum = Transaction.objects.filter(user=self.request.user, repayment=False).aggregate(total=Sum('amount'))['total'] or 0

        # Calculate the balance
        context['balance'] = repaid_sum - unpaid_sum

        return context


class NewTransaction(LoginRequiredMixin, View):
    template_name = 'new-transaction.html'

    # Render the form
    def get(self, request, *args, **kwargs):
        form = NewTransactionForm()
        return render(request, self.template_name, {'form': form})

    # Handle form submission
    def post(self, request, *args, **kwargs):
        form = NewTransactionForm(request.POST)
        if form.is_valid():
            try:
                # Create and save the transaction
                transaction = Transaction(
                    user=request.user,  # Associate with the logged-in user
                    amount=form.cleaned_data['amount'],
                    description=form.cleaned_data.get('description'),
                    repayment=form.cleaned_data.get('repayment'),
                )
                transaction.full_clean()  # Optional: validate the model instance
                transaction.save()

                # Success message and redirect
                messages.success(request, "The transaction has been created!")
                return redirect('index')  # Adjust to your desired redirect view

            except ValidationError as e:
                # Handle validation errors for the model
                for field, error_list in e.error_dict.items():
                    if field in form.fields:
                        form.add_error(field, error_list[0])
                    else:
                        messages.error(request, error_list[0])

        # If the form is invalid, re-render the page with errors
        return render(request, self.template_name, {'form': form})


class DeleteTransactionView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
        transaction.delete()
        messages.success(request, "Transaction deleted successfully.")
        return redirect('index')


class TransactionListView(ListAPIView):

    queryset = Transaction.objects.all()  # Required for DjangoModelPermissionsOrAnonReadOnly
    serializer_class = TransactionSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Calculate the balance
        repaid_sum = queryset.filter(repayment=True).aggregate(total=Sum('amount'))['total'] or 0
        unpaid_sum = queryset.filter(repayment=False).aggregate(total=Sum('amount'))['total'] or 0
        balance = repaid_sum - unpaid_sum

        return Response({
            'balance': balance,
            'transactions': serializer.data
        })