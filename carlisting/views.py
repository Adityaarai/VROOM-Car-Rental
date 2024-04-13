from django.shortcuts import render
from .models import CarDetail

# Create your views here.
def index(request):
    return render(request, 'main/index.html')
        
def carlisting(request):
    items = CarDetail.objects.all()

    context = {
        'items': items,
    }

    return render(request, 'main/carlisting.html', context)

def orders(request):
    name = request.GET.get('renter_name')
    model = request.GET.get('car_model')
    print(name)
    print(model)

    details_queryset = CarDetail.objects.filter(renter_name=name, car_model=model)

    # Convert queryset to list of dictionaries with image URLs
    details_list = []
    for detail in details_queryset:
        detail_dict = {
            'id': detail.id,
            'renter_name': detail.renter_name,
            'renter_contact': detail.renter_contact,
            'car_type': detail.car_type,
            'car_model': detail.car_model,
            'price': detail.price,
            'availability': detail.availability,
            'image': detail.image.url
        }
        print(detail.image.url)
        details_list.append(detail_dict)

    context = {
        'details': details_list,
    }
    return render(request, 'main/car_details.html', context)

def about_us(request):
    return render(request, 'main/about.html')

def userprofile(request):
   return render(request, 'main/user_profile.html')

def staffprofile(request):
   return render(request, 'main/staff_profile.html')

