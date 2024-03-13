from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from PIL import Image
import io
from django.http import JsonResponse
from .serializer import ImageSerializer, UserVisitSerializer, ImageModelSerializer
import requests
import base64
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from .models import UserVisit, ImageModel
# from django.contrib.gis.geoip2 import GeoIP2
import geoip2.database
from django.utils import timezone
import calendar
import os


class ResizeImageView(APIView):
    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data)
        print(serializer, "before ....................")
        if serializer.is_valid():
            print("inside valid function", serializer)
            image_data = serializer.validated_data['image'].read()
            # width_cm = serializer.validated_data.get('width_cm')
            # height_cm = serializer.validated_data.get('height_cm')
            width_px = serializer.validated_data.get('width_px')
            height_px = serializer.validated_data.get('height_px')

            # custom_filename = serializer.validated_data.get('filename')
            image_format = serializer.validated_data.get('format', 'JPEG')

            # crop_left = serializer.validated_data.get('crop_left')
            # crop_top = serializer.validated_data.get('crop_top')
            # crop_right = serializer.validated_data.get('crop_right')
            # crop_bottom = serializer.validated_data.get('crop_bottom')

            img = Image.open(io.BytesIO(image_data))
            print("image open", img)

            # if crop_left is not None and crop_top is not None and crop_right is not None and crop_bottom is not None:
            #     img = img.crop((crop_left, crop_top, crop_right, crop_bottom))

            if width_px and height_px:
                width_data = width_px
                height_data = height_px
            # elif width_cm and height_cm:
            #     width_data = int(width_cm * 37.7952755906)
            #     height_data = int(height_cm * 37.7952755906)
            else:
                return Response({"error": "Provide either pixel scale or centimeter scale for width and height"}, status=status.HTTP_400_BAD_REQUEST)

            resize_image = img.resize((width_data, height_data))
            print(resize_image, "resize image....")
            if resize_image.mode == 'RGBA':
                resize_image = resize_image.convert('RGB')

            output_stream = io.BytesIO()
            resize_image.save(output_stream, format=image_format, quality=90, optimize=True, progressive=True)
            print(resize_image, "After Save")
            output_stream.seek(0)
            print(output_stream, "output stream")
            try:
                base64_string = base64.b64encode(output_stream.getvalue()).decode('utf-8')
                print(base64_string, "base 64...output")
            except Exception as e:
                print(e, "Exception Error")

            url = 'https://api.imgur.com/3/image'

            data = {
                "image": base64_string,
                "type":  "base64",
                "title": "demo",
                "description": "demo"

            }

            token = '390fd1592441500'

            headers = {
               'Authorization': token
            }
            print('befor API call')

            try:
                response = requests.post(url, data=data, headers=headers)

                print("after api call", response.json())

                if response.status_code == 200:
                    data = response.json()
                    title = data.get('title')
                    image_url = data.get('image')
                    image_obj = ImageModel(title=title, image=image_url)
                    serializer = ImageModelSerializer(data=image_obj)

                    if serializer.is_valid():
                        serializer.save()
                        print("Image object saved successfully!")
                    else:
                        print("Error:", serializer.errors)

                    response = JsonResponse(data, safe=False)
                    response.content_type = 'application/json'
                    # Save user visit data
                    ip_address = request.META.get('REMOTE_ADDR')  # Get user's IP address
                    user_visit_data = {'ip_address': ip_address}
                    user_visit_serializer = UserVisitSerializer(data=user_visit_data)
                    if user_visit_serializer.is_valid():
                        user_visit_serializer.save()
                    else:
                        print("Error saving user visit data:", user_visit_serializer.errors)
                    return response
                # Print the response content

                else:
                    # If the request was not successful, print the error status code
                    print("API Error:", response.status_code)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e, 'Exception error')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            # Handle invalid login
            return render(request, 'core/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'core/login.html')


# mmdb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'GeoLite2-Country.mmdb')
reader = geoip2.database.Reader('./GeoLite2-Country.mmdb')


def get_country_from_ip(ip_address):
    try:
        response = reader.country(ip_address)
        return response.country.name  # You can also get other country information like name, continent, etc.
    except geoip2.errors.AddressNotFoundError:
        return None


def admin_dashboard(request):
    if request.user.is_authenticated:
        # Logic to retrieve data for the admin dashboard
        user_visit_count = UserVisit.objects.count()
        image_count = ImageModel.objects.count()
     
        # Logic to retrieve country-wise visit counts
        country_visit_counts = {}
        print(country_visit_counts, "country wise counts")
        for visit in UserVisit.objects.all():
            country_code = get_country_from_ip(visit.ip_address)
            if country_code:
                if country_code in country_visit_counts:
                    country_visit_counts[country_code] += 1
                else:
                    country_visit_counts[country_code] = 1

        # Prepare data for the country-wise visit counts chart
        country_labels = list(country_visit_counts.keys())
        print(country_labels, "country labels")
        country_data = list(country_visit_counts.values())
        print(country_data, "country data")

    
        # Logic to retrieve monthly visit counts for the current year
        current_year = timezone.now().year
        monthly_visit_counts = UserVisit.objects.filter(timestamp__year=current_year).annotate(
            month=ExtractMonth('timestamp')
        ).values('month').annotate(
            visit_count=Count('id')
        ).order_by('month')

        # Prepare data for the monthly user visits chart
        # month_labels = [f"{calendar.month_name[count['month']]} {current_year}" for count in monthly_visit_counts]
        month_labels = ["Jan", "Feb", "Mar", "Apr"]
        print(month_labels, "month labels")
        # month_data = [count['visit_count'] for count in monthly_visit_counts]
        month_data = [15, 10, 25, 12]
        print(month_data, "month data")

        context = {
            'user_visit_count': user_visit_count,
            'image_count': image_count,
            'country_labels': country_labels,
            'country_data': country_data,
            'month_labels': month_labels,
            'month_data': month_data,
            # Other data for the admin dashboard
        }
        return render(request, 'core/dashboard.html', context)
    else:
        return redirect('login')
