from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q
from .models import *
from .serializers import *
from django.contrib.auth import authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class SocialMediaUserSignupView(APIView):
    """
    API endpoint to allow users to sign up.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=SocialMediaUserSignupSerializer,
        responses={
            201: openapi.Response(description='Created', schema=SocialMediaUserSignupSerializer),
            400: openapi.Response(description='Bad Request', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
        }
    )
    def post(self, request):
        """
        Create a new user.
        """
        try:
            serializer = SocialMediaUserSignupSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response(
                    {
                        'responseCode': status.HTTP_201_CREATED,
                        'responseMessage': 'User created successfully.',
                        'responseData': {
                            'id': user.id,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'email': user.email,
                        },
                    },
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': [f"{error[1][0]}" for error in dict(serializer.errors).items()][0],
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except serializers.ValidationError as e:
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': [f"{error[1][0]}" for error in dict(e).items()][0],
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print("SocialMediaUserSignupView Error -->", e)
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Something went wrong! Please try again.',
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LoginView(APIView):
    """
    API endpoint to allow users to login and generate access and refresh tokens.
    """
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(description='OK', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            400: openapi.Response(description='Bad Request', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
        }
    )
    def post(self, request):
        """
        Authenticate user and generate tokens.
        """
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        'responseCode': status.HTTP_200_OK,
                        'responseMessage': 'Login successful.',
                        'responseData': {
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                        }
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': 'Bad Request',
                    'responseData': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Internal Server Error',
                    'responseData': {'error': str(e)},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserSearchView(APIView):
    """
    API endpoint to search other users by email and name with pagination.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='Bearer <token>', required=True),
            openapi.Parameter('search_keyword', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Search keyword', required=True),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Page number', required=False),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Page size', required=False),
        ],
        responses={
            200: openapi.Response(description='OK', schema=UserSearchSerializer(many=True)),
            400: "Bad Request",
            500: "Internal Server Error",
        }
    )
    def get(self, request):
        try:
            search_keyword = request.query_params.get('search_keyword')
            users = SocialMediaUser.objects.all()

            exact_match_user = users.filter(email__iexact=search_keyword)
            if exact_match_user.exists():
                serializer = UserSearchSerializer(exact_match_user, many=True)
                return Response(
                    {
                        'responseCode': status.HTTP_200_OK,
                        'responseMessage': 'User found by email.',
                        'responseData': serializer.data
                    },
                    status=status.HTTP_200_OK
                )

            name_match_users = users.filter(Q(first_name__icontains=search_keyword) | Q(last_name__icontains=search_keyword))
            if name_match_users.exists():
                serializer = UserSearchSerializer(name_match_users, many=True)
                return Response(
                    {
                        'responseCode': status.HTTP_200_OK,
                        'responseMessage': 'Users found by name.',
                        'responseData': serializer.data
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    'responseCode': status.HTTP_404_NOT_FOUND,
                    'responseMessage': 'No users found with the provided search keyword.',
                },
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            print("UserSearchView Error -->", e)
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Something went wrong! Please try again.',
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
class SendFriendRequestView(APIView):
    """
    API endpoint to send a friend request to another user.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
       manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='Bearer <token>', required=True),
            openapi.Parameter('to_user_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='ID of the user to send the friend request to', required=True),
        ],
        responses={
            200: openapi.Response(description='OK', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            400: openapi.Response(description='Bad Request', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            401: "Unauthorized",
            404: "Not Found",
            500: "Internal Server Error",
        }
    )
    def post(self, request):
        try:
            to_user_id = request.query_params.get('to_user_id')
            try:
                to_user_id = int(to_user_id)
            except ValueError:
                return Response(
                    {
                        'responseCode': status.HTTP_400_BAD_REQUEST,
                        'responseMessage': 'Invalid user ID.',
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                to_user = SocialMediaUser.objects.get(id=to_user_id)
            except ObjectDoesNotExist:
                return Response(
                    {
                        'responseCode': status.HTTP_404_NOT_FOUND,
                        'responseMessage': 'User does not exist.',
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            user_serializer = UserSearchSerializer(to_user)
            if to_user_id == request.user.id:
                return Response(
                    {
                        'responseCode': status.HTTP_400_BAD_REQUEST,
                        'responseMessage': 'You cannot send a friend request to yourself.',
                        'responseData': user_serializer.data
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if FriendRequest.objects.filter(from_user=to_user, to_user=request.user, status='P').exists():
                return Response(
                    {
                        'responseCode': status.HTTP_400_BAD_REQUEST,
                        'responseMessage': 'The user has already sent you a friend request. Check your Request List.',
                        'responseData': user_serializer.data
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            existing_request = FriendRequest.objects.filter(from_user=request.user, to_user=to_user).first()
            if existing_request and existing_request.status == 'A':
                print("Check if the friend request has already been accepted")
                user_serializer = UserSearchSerializer(existing_request.from_user)
                return Response(
                    {
                        'responseCode': status.HTTP_400_BAD_REQUEST,
                        'responseMessage': 'You both are already friends.',
                        'responseData': user_serializer.data
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            if existing_request:
                if existing_request.status == 'R':
                    existing_request.status = 'P'
                    existing_request.timestamp = timezone.now()
                    existing_request.save()
                    return Response(
                        {
                            'responseCode': status.HTTP_200_OK,
                            'responseMessage': 'Friend request re-sent successfully.',
                            'responseData': user_serializer.data
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {
                            'responseCode': status.HTTP_400_BAD_REQUEST,
                            'responseMessage': 'Friend request already sent to this user.',
                            'responseData': user_serializer.data
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

            one_minute_ago = timezone.now() - timedelta(minutes=1)
            recent_requests = FriendRequestLimit.objects.filter(user=request.user, timestamp__gte=one_minute_ago).first()

            if recent_requests:
                if recent_requests.request_count >= 3:
                    return Response(
                        {
                            'responseCode': status.HTTP_400_BAD_REQUEST,
                            'responseMessage': 'You have exceeded the limit of 3 friend requests per minute.',
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    recent_requests.request_count += 1
                    recent_requests.save()
            else:
                FriendRequestLimit.objects.create(user=request.user, timestamp=timezone.now(), request_count=1)

            friend_request = FriendRequest(from_user=request.user, to_user=to_user, status='P')
            friend_request.save()

            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'Friend request sent successfully.',
                    'responseData': user_serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            print("SendFriendRequestView Error -->", e)
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Something went wrong! Please try again.',
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AcceptFriendRequestView(APIView):
    """
    API endpoint to accept a friend request.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='Bearer <token>', required=True),
            openapi.Parameter('friend_request_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='ID of the friend request to accept', required=True),
        ],
        responses={
            200: openapi.Response(description='OK', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            400: openapi.Response(description='Bad Request', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            401: "Unauthorized",
            404: "Not Found",
            500: "Internal Server Error",
        }
    )
    def post(self, request):
        try:
            friend_request_id = request.query_params.get('friend_request_id')
            try:
                friend_request_id = int(friend_request_id)
            except ValueError:
                return Response(
                    {
                        'responseCode': status.HTTP_400_BAD_REQUEST,
                        'responseMessage': 'Invalid friend request ID.',
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                friend_request = FriendRequest.objects.get(id=friend_request_id)
            except ObjectDoesNotExist:
                return Response(
                    {
                        'responseCode': status.HTTP_404_NOT_FOUND,
                        'responseMessage': 'Friend request does not exist.',
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            if friend_request.to_user != request.user:
                return Response(
                    {
                        'responseCode': status.HTTP_400_BAD_REQUEST,
                        'responseMessage': 'You are not authorized to accept this friend request.',
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if friend_request.status == 'A':
                print("Check if the friend request has already been accepted")
                user_serializer = UserSearchSerializer(friend_request.from_user)
                return Response(
                    {
                        'responseCode': status.HTTP_400_BAD_REQUEST,
                        'responseMessage': 'You both are already friends.',
                        'responseData': user_serializer.data
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            friend_request.status = 'A'
            friend_request.save()

            user_serializer = UserSearchSerializer(friend_request.from_user)

            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'Friend request accepted successfully.',
                    'responseData': user_serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            print("AcceptFriendRequestView Error -->", e)
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Something went wrong! Please try again.',
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RejectFriendRequestView(APIView):
    """
    API endpoint to reject a friend request.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
       manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='Bearer <token>', required=True),
            openapi.Parameter('friend_request_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='ID of the friend request to reject', required=True),
        ],
        responses={
            200: openapi.Response(description='OK', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            400: openapi.Response(description='Bad Request', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            401: "Unauthorized",
            404: "Not Found",
            500: "Internal Server Error",
        }
    )
    def post(self, request):
        try:
            friend_request_id = request.query_params.get('friend_request_id')
            try:
                friend_request_id = int(friend_request_id)
            except ValueError:
                return Response(
                    {
                        'responseCode': status.HTTP_400_BAD_REQUEST,
                        'responseMessage': 'Invalid friend request ID.',
                        'responseData': None
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                friend_request = FriendRequest.objects.get(id=friend_request_id, to_user=request.user)
            except ObjectDoesNotExist:
                return Response(
                    {
                        'responseCode': status.HTTP_404_NOT_FOUND,
                        'responseMessage': 'Friend request does not exist.',
                        'responseData': None
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            user_serializer = UserSearchSerializer(friend_request.from_user)

            if friend_request.status == 'A':
                return Response(
                    {
                        'responseCode': status.HTTP_400_BAD_REQUEST,
                        'responseMessage': 'You both are already friends.',
                        'responseData': user_serializer.data
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if friend_request.to_user == request.user and friend_request.status == 'R':
                return Response(
                    {
                        'responseCode': status.HTTP_400_BAD_REQUEST,
                        'responseMessage': 'You have already rejected the friend request .',
                        'responseData': user_serializer.data
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            friend_request.status = 'R'
            friend_request.save()

            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'Friend request rejected successfully.',
                    'responseData': user_serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            print("RejectFriendRequestView Error -->", e)
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Something went wrong! Please try again.',
                    'responseData': None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class FriendListView(APIView):
    """
    API endpoint to get the list of friends.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='Bearer <token>', required=True),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Page number', required=False),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Page size', required=False),
        ],
        responses={
            200: openapi.Response(description='OK', schema=UserSearchSerializer(many=True)),
            400: "Bad Request",
            401: "Unauthorized",
            500: "Internal Server Error",
        }
    )
    def get(self, request):
        try:
            friends = FriendRequest.objects.filter(
                Q(from_user=request.user, status='A') | Q(to_user=request.user, status='A')
            ).select_related('from_user', 'to_user')

            page_number = request.query_params.get('page')
            page_size = request.query_params.get('page_size', 10)

            paginator = Paginator(friends, page_size)

            try:
                page_obj = paginator.page(page_number)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)

            serializer = UserSearchSerializer([fr.from_user for fr in page_obj], many=True)

            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'Friends retrieved successfully.',
                    'responseData': serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            print("FriendListView Error -->", e)
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Something went wrong! Please try again.',
                    'responseData': None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PendingFriendRequestsView(APIView):
    """
    API endpoint to get the list of pending friend requests.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='Bearer <token>', required=True),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Page number', required=False),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Page size', required=False),
        ],
        responses={
            200: openapi.Response(description='OK', schema=UserSearchSerializer(many=True)),
            400: "Bad Request",
            401: "Unauthorized",
            500: "Internal Server Error",
        }
    )
    def get(self, request):
        try:
            pending_requests = FriendRequest.objects.filter(to_user=request.user, status='P').select_related('from_user')

            page_number = request.query_params.get('page')
            page_size = request.query_params.get('page_size', 10)

            paginator = Paginator(pending_requests, page_size)

            try:
                page_obj = paginator.page(page_number)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)

            pending_users = [fr.from_user for fr in page_obj]

            serializer = UserSearchSerializer(pending_users, many=True)

            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'Pending friend requests retrieved successfully.',
                    'responseData': serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            print("PendingFriendRequestsView Error -->", e)
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Something went wrong! Please try again.',
                    'responseData': None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )