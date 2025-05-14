from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
import json
from itertools import groupby
from operator import itemgetter

from admins.models import Call, Customer, JobSheet, Executive

# Create your views here.

@login_required(login_url='/')
def dashboard(request):
    return render(request, "exec/dashboard.html")


@login_required(login_url='/')
def calllist(request):
    start_date = request.GET.get('start_date', now().date())
    end_date = request.GET.get('end_date', (now() + timedelta(days=5)).date())
    statuses = request.GET.get('statuses', 'Pending').split(',')  # Split the statuses string into a list

    calls_raw = Call.objects.filter(
        executives=request.user,
        attend_date__date__range=[start_date, end_date],
        call_status__in=statuses
    ).select_related("customer", "amc").prefetch_related("executives").values(
        "id",
        "call_document_number",
        "priority",
        "attend_date",
        "customer__company_customer_name",
        "customer__contact_number",
        "customer__address",
        "customer__google_map_url",
        "notes",
        "call_status",
    )

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({"calls": list(calls_raw)})

    calls = list(calls_raw)
    return render(request, "exec/calllist.html", {
        "calls": calls,
        "today": now().date(),
        "future_date": (now() + timedelta(days=5)).date()
    })


@csrf_exempt
@login_required(login_url='/')
def update_call_status(request, call_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            reason = data.get('reason')

            if action not in ['Complete', 'Cancel']:
                return JsonResponse({'error': 'Invalid action'}, status=400)

            call = Call.objects.get(id=call_id, executives=request.user)
            call.call_status = 'Completed' if action == 'Complete' else 'Rejected'
            call.reason = reason
            call.closed_at = now()
            call.save()

            # Return success response with a message
            return JsonResponse({'message': f'Call status updated to {call.call_status}', 'success': True})
        except Call.DoesNotExist:
            return JsonResponse({'error': 'Call not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required(login_url='/')
def jobsheet(request):
    start_date = request.GET.get('start_date', now().date())
    end_date = request.GET.get('end_date', (now() + timedelta(days=5)).date())
    statuses = request.GET.get('statuses', 'Pending').split(',')  # Split the statuses string into a list

    jobsheets_raw = JobSheet.objects.filter(
        executives=request.user,
        # job_date__date__range=[start_date, end_date],
        # job_status__in=statuses
    ).select_related("customer").values(
        "job_sheet_no",        
        # "job_date",
        "customer__company_customer_name",
        "customer__contact_number",
        "customer__address",
        "customer__google_map_url",
        "notes",
        "job_status",
    )

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({"jobsheets": list(jobsheets_raw)})

    jobsheets = list(jobsheets_raw)
    return render(request, "exec/jobsheet.html", {
        "jobsheets": jobsheets,
        "today": now().date(),
        "future_date": (now() + timedelta(days=5)).date()
    })



