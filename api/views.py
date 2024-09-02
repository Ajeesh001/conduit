from django.contrib.auth.models import User
from .models import Article
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes,api_view
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import json

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
         try:
             data = json.loads(request.body)
             username = data.get('username')
             email = data.get('email')
             password = data.get('password')
             if not username or not email or not password:
                 return JsonResponse({'error': 'All fields are required.'}, status=400)
             if User.objects.filter(username=username).exists():
                 return JsonResponse({'error': 'Username already exists.'}, status=400)
             if User.objects.filter(email=email).exists():
                 return JsonResponse({'error': 'Email already registered.'}, status=400)
             user = User.objects.create_user(username=username, email=email, password=password)
             user.save()
             return JsonResponse({'message': 'User created successfully'}, status=201)
         except json.JSONDecodeError:
             return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def signin_view(request):
      if request.headers.get('X-Requested-With') == 'XMLHttpRequest': 
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                print("Authentication successful for:", user)
                token, _ = Token.objects.get_or_create(user=user)
                return JsonResponse({'token': token.key}, status=200)
            else:
                print("Authentication failed for:", email)
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
        


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_article(request):
        print(f"Request User: {request.user}")
        print(f"Authorization Header: {request.headers.get('Authorization')}")

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body)
                title = data.get('title')
                description = data.get('description')
                body = data.get('body')
                tagList = data.get('taglist')

                article = Article.objects.create(
                    title=title,
                    description=description,
                    body=body,
                    tagList=tagList,
                    user=request.user
                )
                article.save()

                return JsonResponse({"message": "Article added successfully."}, status=200)

            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid request type.'}, status=400)



@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            print(f"Request User: {request.user}")
            token = Token.objects.get(user=request.user)
            token.delete()
            return JsonResponse({"message": "Successfully logged out."}, status=200)
        except Token.DoesNotExist:
            return JsonResponse({"error": "Token not found."}, status=400)
    return JsonResponse({"error": "Invalid request type."}, status=400)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_articles_view(request):
    articles = Article.objects.filter(user=request.user)
    article_list = [
        {
            'id': article.id,
            'title': article.title,
            'description': article.description,
            'body': article.body,
            'tagList': article.tagList,
            'username': article.user.username
        }
        for article in articles
    ]
    return JsonResponse({'articles': article_list}, status=200)

        
@csrf_exempt
@permission_classes([AllowAny])
def global_feed(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        article_list = []
        for article in articles:
            article_list.append({
                'id': article.id,
                'title': article.title,
                'description': article.description,
                'body': article.body,
                'username': article.user.username,
                'tagList': article.tagList.split(',') if article.tagList else [],
            })
        return JsonResponse({'articles': article_list}, status=200)
    return JsonResponse({'error': 'Invalid HTTP method'}, status=400)


# from rest_framework.authtoken.models import Token
# from django.http import JsonResponse

# def check_token(request):
#     try:
#         token = Token.objects.get(key='d0150538525124af7816f647370b45e8dfd1d59b')
#         print(f"Associated User: {token.user}")
#         return JsonResponse({'user': token.user.username}, status=200)
#     except Token.DoesNotExist:
#         print("Invalid Token")
#         return JsonResponse({'error': 'Invalid Token'}, status=400)

