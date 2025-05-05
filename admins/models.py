from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import date

# Create your models here.

class CustomerType(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    
class Customer(models.Model):
    customer_type = models.ForeignKey(CustomerType, on_delete=models.CASCADE)
    company_customer_name = models.CharField(max_length=255, null=False, blank=False)
    contact_number = models.CharField(max_length=15, null=False, blank=False)
    contact_person = models.CharField(max_length=255, null=True, blank=True)
    alternate_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    gst_number = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    area = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    google_map_url = models.URLField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.company_customer_name

class Department(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Executive(AbstractUser):
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    date_of_joining = models.DateField(null=True, blank=True)
    alternate_number = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    marital_status = models.CharField(max_length=20, null=True, blank=True, choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed')])
    dob = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=5, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    area = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    google_map_url = models.URLField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='executives/profiles/', null=True, blank=True)
    front_adhar_card = models.FileField(upload_to='executives/adhar_front/', null=True, blank=True)
    back_adhar_card = models.FileField(upload_to='executives/adhar_back/', null=True, blank=True)
    pan_card = models.FileField(upload_to='executives/pan/', null=True, blank=True)
    passport = models.FileField(upload_to='executives/passport/', null=True, blank=True)
    driving_licence = models.FileField(upload_to='executives/license/', null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username

class AMC(models.Model):
    # Choices for AMC category
    AMC_CATEGORY_CHOICES = [
        ('Service AMC', 'Service AMC'),
        ('Labor AMC', 'Labor AMC'),
    ]

    # Choices for Renew Status
    RENEW_STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    # Fields
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='amcs')
    amc_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15, null=True, blank=True)  # Optional, autofilled from Customer
    amc_doc_no = models.CharField(max_length=100)
    amc_category = models.CharField(max_length=20, choices=AMC_CATEGORY_CHOICES)
    starting_date = models.DateField()
    end_date = models.DateField()
    renew_status = models.CharField(max_length=10, choices=RENEW_STATUS_CHOICES)
    number_of_services = models.PositiveIntegerField(default=1)  # Max 52 validation in clean method
    gst_number = models.CharField(max_length=50, null=True, blank=True)
    terms_and_conditions = models.TextField()
    address = models.CharField(max_length=255, null=True, blank=True)  # Autofill or editable
    area = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    google_map_url = models.URLField(null=True, blank=True)
    amc_notes = models.TextField(null=True, blank=True)
    services_notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.amc_name} - {self.customer.company_customer_name}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.number_of_services > 52:
            raise ValidationError("Number of services cannot exceed 52.")

    class Meta:
        verbose_name = "AMC"
        verbose_name_plural = "AMCs"

class Call(models.Model):
    # Choices for call type
    CALL_TYPE_CHOICES = [
        ("Normal Call", "Normal Call"),
        ("AMC Call", "AMC Call"),
        ("Job Call", "Job Call"),
        ("Service Call", "Service Call"),
    ]

    # Choices for priority
    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    ]

    # Fields
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="calls")
    amc = models.ForeignKey(AMC, on_delete=models.CASCADE, related_name="calls", null=True, blank=True)
    call_document_number = models.CharField(max_length=100, null=True, blank=True)
    call_type = models.CharField(max_length=20, choices=CALL_TYPE_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="Low")
    executive_designation = models.CharField(max_length=100, null=True, blank=True)
    executives = models.ManyToManyField(Executive, related_name="calls")
    attend_date = models.DateTimeField()
    notes = models.TextField(null=True, blank=True)

    @property
    def remaining_days(self):
        """Calculate the remaining days between today and the AMC's end date."""
        if self.amc and self.amc.end_date:
            return (self.amc.end_date - date.today()).days
        return None

    def __str__(self):
        return f"Call - {self.customer.company_customer_name} - {self.call_type}"

