from django.shortcuts import render, redirect
from .forms import OrganizationForm
from .models import Organization

'''
We use a dictionary so we can give names to the data we pass into the template.
This allows the template to access variables like form, organization, user, etc
It's not specific to forms — all data passed to templates goes inside a dictionary.

<form method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Submit</button>
</form>
Here, {{ form.as_p }} works because you gave the template access to a variable named form.

'''

# Create your views here.
def organization_list(request):
    # Fetches all instances of the Organization model from the database
    orgs = Organization.objects.all() # return a query set containing every record in the organization table
    return render(request, 'organizations/list.html', {'organization': orgs}) # render the
    # organization/list.html, pass context dictionary 'organization' refers to orgs queryset

def organization_detail(request, org_id):
    org = Organization.objects.get(id=org_id)  # using id, display details of organization
    # render is used to return HTML response using a template or context
    return render(request, 'organizations/detail.html', {'organization': org})

def organization_create(request):
    if request.method == 'POST': # POST use for form submission
        # request.POST contains all the text field, request.FILES contain the uploaded file data like images, documents
        form = OrganizationForm(request.POST, request.FILES) # Instantiate the form with POST data and uploaded files
        if form.is_valid(): #validates form input
            form.save() # creates new organization instance
            return redirect('organization_list') # if complete the save redirect to some pages, NEED TO CHANGE THIS
    else:
        form = OrganizationForm()
    #Render the template and provide a variable called form that the template can access, whose value is this
    # OrganizationForm instance.
    return render(request, 'organizations/create.html', {'form': form})