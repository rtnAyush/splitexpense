from django.shortcuts import render
from .models import User
from django.http import Http404, JsonResponse
from json import JSONDecodeError, loads
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def createUser(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            name = data.get("name")
            email = data.get("email")
            phone = data.get("phone")
            password = data.get("password")

            # Handling missing data 
            if not name:
                return JsonResponse({
                'error':True,
                'message':"Name required"
            }, status=400)
            if not email:
                return JsonResponse({
                'error':True,
                'message':"Email required"
            }, status=400)
            if not phone:
                return JsonResponse({
                'error':True,
                'message':"Phone required"
            }, status=400)
            if not password:
                return JsonResponse({
                'error':True,
                'message':"Password required"
            }, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    'error':True,
                    'message':"Email already exists"
                }, status=400) 
             
            hashed_password = make_password(password)

            user = User.objects.create(name=name, email=email, phone=phone, password=hashed_password)

            return JsonResponse({
                    'error':False,
                    'message':"User created successfully",
                    "userId":user.id
                }, status=201)  

        except JSONDecodeError:
            return JsonResponse({
                'error':True,
                'message':"Invalid JSON"
            }, status=400)
        except Exception as e:
            return JsonResponse({
                    'error':True,
                    'message':str(e)
                }, status=500) 

@csrf_exempt
def getUserById(request, userId):
    try:
        user = User.objects.get(id=userId)
        return JsonResponse({
            "id": user.id,
            'name':user.name,
            'email':user.email,
            'phone':user.phone
        })
    except User.DoesNotExist:
        return JsonResponse({
            "error": True,
            'message':"User not found"
        }, status=404)
    except Exception as e:
            return JsonResponse({
                    'error':True,
                    'message':str(e)
                }, status=500)