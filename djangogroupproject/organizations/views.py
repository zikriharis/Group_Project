from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import OrganizationApplicationForm, OrganizationAdminReviewForm
from .models import Organization, OrganisationApplicationDocument

@login_required
def apply_for_organization(request):
    if request.method == 'POST':
        form = OrganizationApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                organization = form.save(commit=False)
                organization.owner = request.user
                organization.verification_status = 'pending' # Default status
                organization.save()
                
                # Save uploaded documents using the custom method in the form
                # Ensure request.FILES is passed to the form for file uploads
                # The form's cleaned_data will contain 'application_documents'
                # We need to handle multiple files from request.FILES.getlist('application_documents')
                # The form's save_documents method is designed to handle this.
                
                # Re-instantiate form with files to access cleaned_data['application_documents'] if not already available
                # Or, more simply, pass the files directly to the save_documents method if the form is designed that way.
                # The current OrganizationApplicationForm expects to find 'application_documents' in its cleaned_data.
                form.save_documents(organization) # Call the helper method to save documents

                # Update user's role to 'organization' if they are applying
                # This assumes the user creating the organization should have their role updated.
                # This might need refinement based on exact role flow (e.g., if a donor can initiate an org application)
                if request.user.role == 'donor': # Or other appropriate initial role
                    request.user.role = 'organization' # Or a specific 'pending_organization_owner' role
                    request.user.organization = organization # Link user to this new org
                    request.user.save()

                messages.success(request, 'Your application has been submitted successfully and is pending review.')
                return redirect('dashboard:home')  # Or a specific 'application_submitted_success_page'
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = OrganizationApplicationForm()
    
    return render(request, 'organizations/application_form.html', {'form': form, 'title': 'Apply for Organization Account'})


@login_required
def admin_pending_organizations(request):
    if not request.user.role == 'admin':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('main_landing_pages:landing') # Or to a generic dashboard/login

    pending_organizations = Organization.objects.filter(verification_status='pending').order_by('created_at')
    context = {
        'organizations': pending_organizations,
        'title': 'Pending Organization Applications'
    }
    return render(request, 'organizations/admin_pending_list.html', context)


@login_required
def admin_review_organization(request, organization_id):
    if not request.user.role == 'admin':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('main_landing_pages:landing')

    organization = get_object_or_404(Organization, id=organization_id)
    documents = OrganisationApplicationDocument.objects.filter(organization=organization)

    if request.method == 'POST':
        form = OrganizationAdminReviewForm(request.POST, instance=organization)
        if form.is_valid():
            try:
                form.save() # The form's save method now handles updating verification_status
                messages.success(request, f'Organization "{organization.name}" has been updated to "{organization.get_verification_status_display()}".')
                return redirect('organizations:admin_pending_organizations')
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = OrganizationAdminReviewForm(instance=organization)

    context = {
        'organization': organization,
        'documents': documents,
        'form': form,
        'title': f'Review Application: {organization.name}'
    }
    return render(request, 'organizations/admin_review_detail.html', context)
