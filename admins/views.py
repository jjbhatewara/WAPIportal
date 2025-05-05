from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Customer, CustomerType, Executive, Department, AMC, Call

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Executive
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def dashboard(request):
    return render(request, "owner/dashboard.html")


def customers(request):
    customer_types = CustomerType.objects.all()  # Fetch all customer types
    customers = Customer.objects.all()  # Fetch all customers
    return render(
        request,
        "owner/customers.html",
        {"customer_types": customer_types, "customers": customers},
    )


def add_customer(request):
    if request.method == "POST":
        try:
            # Retrieve form data
            customer_type_id = request.POST.get("customer_type")
            company_customer_name = request.POST.get("name")
            contact_number = request.POST.get("contact_number")
            contact_person = request.POST.get("contact_person")
            alternate_number = request.POST.get("alternate_number")
            email = request.POST.get("email")
            gst_number = request.POST.get("gst_number")
            address = request.POST.get("address")
            area = request.POST.get("area")
            city = request.POST.get("city")
            state = request.POST.get("state")
            zip_code = request.POST.get("zip")
            country = request.POST.get("country")
            google_map_url = request.POST.get("google_map_url")
            notes = request.POST.get("notes")

            # Get the CustomerType object
            customer_type = CustomerType.objects.get(id=customer_type_id)

            # Create and save the Customer object
            Customer.objects.create(
                customer_type=customer_type,
                company_customer_name=company_customer_name,
                contact_number=contact_number,
                contact_person=contact_person,
                alternate_number=alternate_number,
                email=email,
                gst_number=gst_number,
                address=address,
                area=area,
                city=city,
                state=state,
                zip_code=zip_code,
                country=country,
                google_map_url=google_map_url,
                notes=notes,
            )

            # Return success response
            return JsonResponse(
                {"status": "success", "message": "Customer added successfully!"}
            )
        except Exception as e:
            # Return error response
            return JsonResponse(
                {"status": "error", "message": f"Error adding customer: {str(e)}"}
            )

    # Return error for non-POST requests
    return JsonResponse({"status": "error", "message": "Invalid request method."})


def delete_customer(request, customer_id):
    if request.method == "DELETE":
        try:
            # Fetch the customer by ID and delete it
            customer = Customer.objects.get(id=customer_id)
            customer.delete()
            return JsonResponse(
                {"status": "success", "message": "Customer deleted successfully!"}
            )
        except Customer.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Customer not found!"})
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": f"Error deleting customer: {str(e)}"}
            )
    return JsonResponse({"status": "error", "message": "Invalid request method."})


@csrf_exempt
def get_customer_details(request, customer_id):
    if request.method == "GET":
        try:
            # Fetch the customer by ID
            customer = get_object_or_404(Customer, id=customer_id)

            # Prepare customer data
            customer_data = {
                "id": customer.id,
                "contact_number": customer.contact_number,
                "gst_number": customer.gst_number,
                "address": customer.address,
                "area": customer.area,
                "city": customer.city,
                "state": customer.state,
                "zip_code": customer.zip_code,
                "google_map_url": customer.google_map_url,
                "customer_type": customer.customer_type.title,  # Return customer type name
            }

            # Fetch AMCs linked to the customer
            amcs = AMC.objects.filter(customer=customer).values(
                "id", "amc_name", "contact_number", "amc_doc_no", "renew_status"
            )
            amc_list = list(amcs)

            # Return success response
            return JsonResponse(
                {"status": "success", "customer": customer_data, "amcs": amc_list}
            )
        except Exception as e:
            # Return error response
            return JsonResponse(
                {"status": "error", "message": f"Error fetching customer details: {str(e)}"}
            )

    # Return error for non-GET requests
    return JsonResponse({"status": "error", "message": "Invalid request method."})


@csrf_exempt
def edit_customer(request, customer_id):
    if request.method == "POST":
        try:
            customer = get_object_or_404(Customer, id=customer_id)

            # Update customer fields
            customer.customer_type_id = request.POST.get("customer_type")
            customer.company_customer_name = request.POST.get("company_customer_name")
            customer.contact_number = request.POST.get("contact_number")
            customer.contact_person = request.POST.get("contact_person")
            customer.alternate_number = request.POST.get("alternate_number")
            customer.email = request.POST.get("email")
            customer.gst_number = request.POST.get("gst_number")
            customer.address = request.POST.get("address")
            customer.area = request.POST.get("area")
            customer.city = request.POST.get("city")
            customer.state = request.POST.get("state")
            customer.zip_code = request.POST.get("zip_code")
            customer.country = request.POST.get("country")
            customer.google_map_url = request.POST.get("google_map_url")
            customer.notes = request.POST.get("notes")

            customer.save()  # Save changes
            return JsonResponse(
                {
                    "status": "success",
                    "message": "Customer details updated successfully!",
                }
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": f"Error updating customer: {str(e)}"}
            )

    return JsonResponse({"status": "error", "message": "Invalid request method."})


@csrf_exempt
def add_executive(request):
    if request.method == "POST":
        try:
            # Retrieve form data
            name = request.POST.get("name")
            contact = request.POST.get("contact")
            email = request.POST.get("email")
            username = request.POST.get("username")
            password = request.POST.get("password")
            alt_contact = request.POST.get("alt_contact")
            gender = request.POST.get("gender")
            marital_status = request.POST.get("marital_status")
            dob = request.POST.get("dob")
            doj = request.POST.get("doj")
            blood_group = request.POST.get("blood_group")
            designation = request.POST.get("designation")
            department_name = request.POST.get("department")
            address = request.POST.get("address")
            area = request.POST.get("area")
            city = request.POST.get("city")
            state = request.POST.get("state")
            country = request.POST.get("country")
            zip_code = request.POST.get("zip")
            map_url = request.POST.get("map_url")
            notes = request.POST.get("notes")
            profile_image = request.FILES.get("photo")
            front_adhar_card = request.FILES.get("aadhar")
            pan_card = request.FILES.get("pan")
            driving_licence = request.FILES.get("driving_licence")

            # Get the department object
            department = Department.objects.get(id=department_name)

            # Create and save the Executive object
            executive = Executive.objects.create(
                first_name=name,
                username=username,
                email=email,
                contact_number=contact,
                alternate_number=alt_contact,
                gender=gender,
                marital_status=marital_status,
                dob=dob,
                date_of_joining=doj,
                blood_group=blood_group,
                designation=designation,
                department=department,
                address=address,
                area=area,
                city=city,
                state=state,
                country=country,
                zip_code=zip_code,
                google_map_url=map_url,
                notes=notes,
                profile_image=profile_image,
                front_adhar_card=front_adhar_card,
                pan_card=pan_card,
                driving_licence=driving_licence,
            )
            executive.set_password(password)  # Set the password
            executive.save()

            # Return success response
            return JsonResponse(
                {"status": "success", "message": "Executive added successfully!"}
            )
        except Department.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Invalid department selected!"}
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": f"Error adding executive: {str(e)}"}
            )

    # Return error for non-POST requests
    return JsonResponse({"status": "error", "message": "Invalid request method."})


def delete_executive(request, executive_id):
    if request.method == "DELETE":
        try:
            # Fetch the executive by ID
            executive = Executive.objects.get(id=executive_id)

            # Delete associated media files
            if executive.profile_image and os.path.isfile(executive.profile_image.path):
                os.remove(executive.profile_image.path)
            if executive.front_adhar_card and os.path.isfile(
                executive.front_adhar_card.path
            ):
                os.remove(executive.front_adhar_card.path)
            if executive.pan_card and os.path.isfile(executive.pan_card.path):
                os.remove(executive.pan_card.path)
            if executive.driving_licence and os.path.isfile(
                executive.driving_licence.path
            ):
                os.remove(executive.driving_licence.path)

            # Delete the executive
            executive.delete()
            return JsonResponse(
                {
                    "status": "success",
                    "message": "Executive and associated media files deleted successfully!",
                }
            )
        except Executive.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Executive not found!"})
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": f"Error deleting executive: {str(e)}"}
            )
    return JsonResponse({"status": "error", "message": "Invalid request method."})


@csrf_exempt
def edit_executive(request, executive_id):
    if request.method == "POST":
        try:
            # Fetch the executive by ID
            executive = get_object_or_404(Executive, id=executive_id)

            # Update fields
            executive.username = request.POST.get("username", executive.username)
            executive.email = request.POST.get("email", executive.email)
            executive.contact_number = request.POST.get(
                "contact_number", executive.contact_number
            )
            executive.alternate_number = request.POST.get(
                "alternate_number", executive.alternate_number
            )
            executive.gender = request.POST.get("gender", executive.gender)
            executive.designation = request.POST.get(
                "designation", executive.designation
            )
            executive.address = request.POST.get("address", executive.address)
            executive.city = request.POST.get("city", executive.city)
            executive.state = request.POST.get("state", executive.state)
            executive.country = request.POST.get("country", executive.country)
            executive.notes = request.POST.get("notes", executive.notes)

            # Update department
            department_id = request.POST.get("department")
            if department_id:
                department = get_object_or_404(Department, id=department_id)
                executive.department = department

            # Handle file uploads
            if "profile_image" in request.FILES:
                executive.profile_image = request.FILES["profile_image"]
            if "front_adhar_card" in request.FILES:
                executive.front_adhar_card = request.FILES["front_adhar_card"]
            if "pan_card" in request.FILES:
                executive.pan_card = request.FILES["pan_card"]
            if "driving_licence" in request.FILES:
                executive.driving_licence = request.FILES["driving_licence"]

            # Save the updated executive
            executive.save()

            return JsonResponse(
                {
                    "status": "success",
                    "message": "Executive details updated successfully!",
                }
            )
        except Department.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Invalid department selected!"}
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": f"Error updating executive: {str(e)}"}
            )

    return JsonResponse({"status": "error", "message": "Invalid request method."})


def executives(request):
    departments = Department.objects.all()  # Fetch all departments
    executives = Executive.objects.filter(is_superuser=False).values(
        "id", "first_name", "department__name", "contact_number", "notes"
    )  # Fetch required fields of executives who are not superusers
    return render(
        request,
        "owner/executives.html",
        {"departments": departments, "executives": executives},
    )


def executive_details(request, executive_id):
    if request.method == "GET":
        try:
            # Fetch the executive by ID
            executive = get_object_or_404(Executive, id=executive_id)
            departments = Department.objects.all()  # Fetch all departments

            # Render the executive details into an HTML template
            html = render(
                request,
                "owner/executive_details.html",
                {"executive": executive, "departments": departments},
            ).content.decode("utf-8")

            # Return the HTML as part of the JSON response
            return JsonResponse({"status": "success", "html": html})
        except Exception as e:
            return JsonResponse(
                {
                    "status": "error",
                    "message": f"Error fetching executive details: {str(e)}",
                }
            )

    return JsonResponse({"status": "error", "message": "Invalid request method."})


def call(request):
    customers = Customer.objects.values(
        "id", "company_customer_name"
    )  #
    executives = Executive.objects.filter(is_superuser=False).values(
        "id", "first_name",
    ) 
    calls = Call.objects.select_related("customer", "amc").prefetch_related("executives").values(
        "id",
        "call_document_number",
        "call_type",
        "priority",
        "attend_date",
        "customer__company_customer_name",
        "amc__amc_name",
        "amc__renew_status",
        "customer__contact_number",
        "executives__first_name",
    )
    return render(request, "owner/call.html",{"customers": customers, "executives": executives, "calls": calls})


def jobs(request):
    return render(request, "owner/jobs.html")


def amc(request):
    customers = Customer.objects.values(
        "id", "company_customer_name"
    )  # Fetch customer id and name
    amcs = AMC.objects.values(
        "id",
        "amc_name",
        "amc_doc_no",
        "contact_number",
        "renew_status",
        "gst_number",
        "number_of_services",
        "customer__company_customer_name",  # Include customer name
    )  # Fetch AMC details
    return render(
        request,
        "owner/amc.html",
        {"customers": customers, "amcs": amcs},
    )


@csrf_exempt
def add_amc(request):
    if request.method == "POST":
        try:
            # Retrieve form data
            customer_id = request.POST.get("customerName")
            amc_name = request.POST.get("amcName")
            contact_number = request.POST.get("contactNumber")
            amc_doc_no = request.POST.get("amcDocNo")
            amc_category = request.POST.get("amcCategory")
            starting_date = request.POST.get("startingDate")
            end_date = request.POST.get("endDate")
            renew_status = request.POST.get("renewStatus")
            number_of_services = request.POST.get("numberOfServices")
            gst_number = request.POST.get("gstNumber")
            terms_and_conditions = request.POST.get("termsAndConditions")
            address = request.POST.get("address")
            area = request.POST.get("area")
            city = request.POST.get("city")
            state = request.POST.get("state")
            zip_code = request.POST.get("zip")
            country = request.POST.get("country")
            google_map_url = request.POST.get("googleMapUrl")
            amc_notes = request.POST.get("amcNotes")
            services_notes = request.POST.get("servicesNotes")

            # Get the Customer object
            customer = get_object_or_404(Customer, id=customer_id)

            # Create and save the AMC object
            AMC.objects.create(
                customer=customer,
                amc_name=amc_name,
                contact_number=contact_number,
                amc_doc_no=amc_doc_no,
                amc_category=amc_category,
                starting_date=starting_date,
                end_date=end_date,
                renew_status=renew_status,
                number_of_services=number_of_services,
                gst_number=gst_number,
                terms_and_conditions=terms_and_conditions,
                address=address,
                area=area,
                city=city,
                state=state,
                zip_code=zip_code,
                country=country,
                google_map_url=google_map_url,
                amc_notes=amc_notes,
                services_notes=services_notes,
            )

            # Return success response
            return JsonResponse(
                {"status": "success", "message": "AMC created successfully!"}
            )
        except Exception as e:
            # Return error response
            return JsonResponse(
                {"status": "error", "message": f"Error creating AMC: {str(e)}"}
            )

    # Return error for non-POST requests
    return JsonResponse({"status": "error", "message": "Invalid request method."})


@csrf_exempt
def delete_amc(request, amc_id):
    if request.method == "DELETE":
        try:
            # Fetch the AMC by ID and delete it
            amc = get_object_or_404(AMC, id=amc_id)
            amc.delete()
            return JsonResponse(
                {"status": "success", "message": "AMC deleted successfully!"}
            )
        except AMC.DoesNotExist:
            return JsonResponse({"status": "error", "message": "AMC not found!"})
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": f"Error deleting AMC: {str(e)}"}
            )
    return JsonResponse({"status": "error", "message": "Invalid request method."})


def get_amc_details(request, amc_id):
    if request.method == "GET":
        try:
            amc = get_object_or_404(AMC, id=amc_id)
            amc_data = {
                "id": amc.id,
                "amc_name": amc.amc_name,
                "contact_number": amc.contact_number,
                "amc_doc_no": amc.amc_doc_no,
                "amc_category": amc.amc_category,
                "renew_status": amc.renew_status,
                "number_of_services": amc.number_of_services,
                "starting_date": amc.starting_date.strftime("%Y-%m-%d"),
                "end_date": amc.end_date.strftime("%Y-%m-%d"),
                "amc_notes": amc.amc_notes,
                "services_notes": amc.services_notes,
            }
            return JsonResponse({"status": "success", "amc": amc_data})
        except Exception as e:
            return JsonResponse({"status": "error", "message": f"Error: {str(e)}"})


@csrf_exempt
def edit_amc(request, amc_id):
    if request.method == "POST":
        try:
            amc = get_object_or_404(AMC, id=amc_id)

            # Update AMC fields
            amc.amc_name = request.POST.get("amc_name", amc.amc_name)
            amc.contact_number = request.POST.get("contact_number", amc.contact_number)
            amc.amc_doc_no = request.POST.get("amc_doc_no", amc.amc_doc_no)
            amc.amc_category = request.POST.get("amc_category", amc.amc_category)
            amc.renew_status = request.POST.get("renew_status", amc.renew_status)
            amc.number_of_services = request.POST.get("number_of_services", amc.number_of_services)
            amc.starting_date = request.POST.get("starting_date", amc.starting_date)
            amc.end_date = request.POST.get("end_date", amc.end_date)
            amc.amc_notes = request.POST.get("amc_notes", amc.amc_notes)
            amc.services_notes = request.POST.get("services_notes", amc.services_notes)

            # Save changes
            amc.save()

            return JsonResponse({"status": "success", "message": "AMC updated successfully!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": f"Error: {str(e)}"})


@csrf_exempt
def create_call(request):
    if request.method == "POST":
        try:
            # Retrieve form data
            customer_id = request.POST.get("customer")
            amc_id = request.POST.get("amc")
            # contact_number = request.POST.get("contact_number")
            call_document_number = request.POST.get("call_document_number")
            call_type = request.POST.get("call_type")
            # customer_type = request.POST.get("customer_type")
            priority = request.POST.get("priority")
            executive_ids = request.POST.getlist("executives")
            attend_date = request.POST.get("attend_date")
            # address = request.POST.get("address")
            # area = request.POST.get("area")
            # city = request.POST.get("city")
            # state = request.POST.get("state")
            # zip_code = request.POST.get("zip_code")
            # google_map_url = request.POST.get("google_map_url")
            notes = request.POST.get("notes")

            # Get the Customer and AMC objects
            customer = get_object_or_404(Customer, id=customer_id)
            amc = get_object_or_404(AMC, id=amc_id) if amc_id else None

            # Create the Call object
            call = Call.objects.create(
                customer=customer,
                amc=amc,
                call_document_number=call_document_number,
                call_type=call_type,
                priority=priority,
                attend_date=attend_date,
                notes=notes,
            )

            # Add executives to the call
            executives = Executive.objects.filter(id__in=executive_ids)
            call.executives.set(executives)

            # Return success response
            return JsonResponse({"status": "success", "message": "Call created successfully!"})
        except Exception as e:
            # Return error response
            return JsonResponse({"status": "error", "message": f"Error creating call: {str(e)}"})

    # Return error for non-POST requests
    return JsonResponse({"status": "error", "message": "Invalid request method."})


def todo(request):
    return render(request, "owner/todo.html")


def settings(request):
    return render(request, "owner/settings.html")
