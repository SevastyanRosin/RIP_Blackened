import random
import uuid
from datetime import datetime, timedelta

from django.contrib.auth import authenticate
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from .permissions import *
from .redis import session_storage
from .serializers import *
from .utils import identity_user, get_session


def get_draft_decree(request):
    user = identity_user(request)

    if user is None:
        return None

    decree = Decree.objects.filter(owner=user).filter(status=1).first()

    return decree


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'unit_name',
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING
        )
    ]
)
@api_view(["GET"])
def search_units(request):
    unit_name = request.GET.get("unit_name", "")

    units = Unit.objects.filter(status=1)

    if unit_name:
        units = units.filter(name__icontains=unit_name)

    serializer = UnitsSerializer(units, many=True)

    draft_decree = get_draft_decree(request)

    resp = {
        "units": serializer.data,
        "units_count": UnitDecree.objects.filter(decree=draft_decree).count() if draft_decree else None,
        "draft_decree_id": draft_decree.pk if draft_decree else None
    }

    return Response(resp)


@api_view(["GET"])
def get_unit_by_id(request, unit_id):
    if not Unit.objects.filter(pk=unit_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    unit = Unit.objects.get(pk=unit_id)
    serializer = UnitSerializer(unit)

    return Response(serializer.data)


@swagger_auto_schema(method='put', request_body=UnitSerializer)
@api_view(["PUT"])
@permission_classes([IsModerator])
def update_unit(request, unit_id):
    if not Unit.objects.filter(pk=unit_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    unit = Unit.objects.get(pk=unit_id)

    serializer = UnitSerializer(unit, data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()

    return Response(serializer.data)


@swagger_auto_schema(method='POST', request_body=UnitAddSerializer)
@api_view(["POST"])
@permission_classes([IsModerator])
@parser_classes((MultiPartParser,))
def create_unit(request):
    serializer = UnitSerializer(data=request.data, partial=False)

    serializer.is_valid(raise_exception=True)

    unit = Unit.objects.create(**serializer.validated_data)

    image = request.data.get("image")
    if image is not None:
        unit.image = image
        unit.save()

    units = Unit.objects.filter(status=1)
    serializer = UnitSerializer(units, many=True)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsModerator])
def delete_unit(request, unit_id):
    if not Unit.objects.filter(pk=unit_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    unit = Unit.objects.get(pk=unit_id)
    unit.status = 2
    unit.save()

    unit = Unit.objects.filter(status=1)
    serializer = UnitSerializer(unit, many=True)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_unit_to_decree(request, unit_id):
    if not Unit.objects.filter(pk=unit_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    unit = Unit.objects.get(pk=unit_id)

    draft_decree = get_draft_decree(request)

    if draft_decree is None:
        draft_decree = Decree.objects.create()
        draft_decree.date_created = timezone.now()
        draft_decree.owner = identity_user(request)
        draft_decree.save()

    if UnitDecree.objects.filter(decree=draft_decree, unit=unit).exists():
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    item = UnitDecree.objects.create()
    item.decree = draft_decree
    item.unit = unit
    item.save()

    serializer = DecreeSerializer(draft_decree)
    return Response(serializer.data["units"])


@swagger_auto_schema(
    method='post',
    manual_parameters=[
        openapi.Parameter('image', openapi.IN_FORM, type=openapi.TYPE_FILE),
    ]
)
@api_view(["POST"])
@permission_classes([IsModerator])
@parser_classes((MultiPartParser,))
def update_unit_image(request, unit_id):
    if not Unit.objects.filter(pk=unit_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    unit = Unit.objects.get(pk=unit_id)

    image = request.data.get("image")

    if image is None:
        return Response(status.HTTP_400_BAD_REQUEST)

    unit.image = image
    unit.save()

    serializer = UnitSerializer(unit)

    return Response(serializer.data)


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'status',
            openapi.IN_QUERY,
            type=openapi.TYPE_NUMBER
        ),
        openapi.Parameter(
            'date_formation_start',
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'date_formation_end',
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING
        )
    ]
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_decrees(request):
    status_id = int(request.GET.get("status", 0))
    date_formation_start = request.GET.get("date_formation_start")
    date_formation_end = request.GET.get("date_formation_end")

    decrees = Decree.objects.exclude(status__in=[1, 5])

    user = identity_user(request)
    if not user.is_superuser:
        decrees = decrees.filter(owner=user)

    if status_id > 0:
        decrees = decrees.filter(status=status_id)

    if date_formation_start and parse_datetime(date_formation_start):
        decrees = decrees.filter(date_formation__gte=parse_datetime(date_formation_start))

    if date_formation_end and parse_datetime(date_formation_end):
        decrees = decrees.filter(date_formation__lt=parse_datetime(date_formation_end))

    serializer = DecreesSerializer(decrees, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_decree_by_id(request, decree_id):
    user = identity_user(request)

    if not Decree.objects.filter(pk=decree_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    decree = Decree.objects.get(pk=decree_id)
    serializer = DecreeSerializer(decree)

    return Response(serializer.data)


@swagger_auto_schema(method='put', request_body=DecreeSerializer)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_decree(request, decree_id):
    user = identity_user(request)

    if not Decree.objects.filter(pk=decree_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    decree = Decree.objects.get(pk=decree_id)
    serializer = DecreeSerializer(decree, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_status_user(request, decree_id):
    user = identity_user(request)

    if not Decree.objects.filter(pk=decree_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    decree = Decree.objects.get(pk=decree_id)

    if decree.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    decree.status = 2
    decree.date_formation = timezone.now()
    decree.save()

    serializer = DecreeSerializer(decree)

    return Response(serializer.data)


def random_date():
    now = datetime.now(tz=timezone.utc)
    return now + timedelta(random.uniform(-1, 0) * 100)


@swagger_auto_schema(
    method='put',
    request_body=openapi.Schema(
        title="Update order",
        type=openapi.TYPE_OBJECT,
        properties={
            'status': openapi.Schema(type=openapi.TYPE_NUMBER),
        }
    )
)
@api_view(["PUT"])
@permission_classes([IsModerator])
def update_status_admin(request, decree_id):
    if not Decree.objects.filter(pk=decree_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = int(request.data["status"])

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    decree = Decree.objects.get(pk=decree_id)

    if decree.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    if request_status == 3:
        decree.date = random_date()

    decree.status = request_status
    decree.date_complete = timezone.now()
    decree.moderator = identity_user(request)
    decree.save()

    serializer = DecreeSerializer(decree)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_decree(request, decree_id):
    user = identity_user(request)

    if not Decree.objects.filter(pk=decree_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    decree = Decree.objects.get(pk=decree_id)

    if decree.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    decree.status = 5
    decree.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_unit_from_decree(request, decree_id, unit_id):
    user = identity_user(request)

    if not Decree.objects.filter(pk=decree_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not UnitDecree.objects.filter(decree_id=decree_id, unit_id=unit_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = UnitDecree.objects.get(decree_id=decree_id, unit_id=unit_id)
    item.delete()

    decree = Decree.objects.get(pk=decree_id)

    serializer = DecreeSerializer(decree)
    units = serializer.data["units"]

    return Response(units)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_unit_decree(request, decree_id, unit_id):
    user = identity_user(request)

    if not Decree.objects.filter(pk=decree_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not UnitDecree.objects.filter(unit_id=unit_id, decree_id=decree_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = UnitDecree.objects.get(unit_id=unit_id, decree_id=decree_id)

    serializer = UnitDecreeSerializer(item)

    return Response(serializer.data)


@swagger_auto_schema(method='PUT', request_body=UnitDecreeSerializer)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_unit_in_decree(request, decree_id, unit_id):
    user = identity_user(request)

    if not Decree.objects.filter(pk=decree_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not UnitDecree.objects.filter(unit_id=unit_id, decree_id=decree_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = UnitDecree.objects.get(unit_id=unit_id, decree_id=decree_id)

    serializer = UnitDecreeSerializer(item, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@swagger_auto_schema(method='post', request_body=UserLoginSerializer)
@api_view(["POST"])
def login(request):
    serializer = UserLoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(**serializer.data)
    if user is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    session_id = str(uuid.uuid4())
    session_storage.set(session_id, user.id)

    serializer = UserSerializer(user)
    response = Response(serializer.data, status=status.HTTP_200_OK)
    response.set_cookie("session_id", session_id, samesite="lax")

    return response


@swagger_auto_schema(method='post', request_body=UserRegisterSerializer)
@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    session_id = str(uuid.uuid4())
    session_storage.set(session_id, user.id)

    serializer = UserSerializer(user)
    response = Response(serializer.data, status=status.HTTP_201_CREATED)
    response.set_cookie("session_id", session_id, samesite="lax")

    return response


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    session = get_session(request)
    session_storage.delete(session)

    response = Response(status=status.HTTP_200_OK)
    response.delete_cookie('session_id')

    return response


@swagger_auto_schema(method='PUT', request_body=UserSerializer)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    if not User.objects.filter(pk=user_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = identity_user(request)

    if user.pk != user_id:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    serializer.save()

    return Response(serializer.data, status=status.HTTP_200_OK)
