from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .serializers import QuestionSerializer, AnswerSerializer, CreateUserSerializer
from .models import Question, Answer
from .permissions import IsOwnerOrReadOnly


class QuestionAPIView(generics.ListCreateAPIView):
    """
    List & create questions
    /api/v1/question/ GET
    /api/v1/question/ POST
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if serializer.validated_data['owner'] == self.request.user:
                self.create(request, *args, **kwargs)
                return Response({"success": "New question added successful"})
            return Response({"userInvalid": "You can't create for others!! Create for you!!"})


class QuestionUpdateAPIView(generics.UpdateAPIView):
    """
    Update the question
    /api/v1/question/<id>/ PUT
    """
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsAdminUser, IsOwnerOrReadOnly]


class AnswerListAPIView(generics.ListCreateAPIView):
    """
        User answers
        /api/v1/qanswer/<id>/ POST & GET
    """
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if serializer.validated_data['user'] == self.request.user:
                if Answer.objects.filter(question=serializer.validated_data['question'], user=self.request.user):
                    return Response({"error": "You have already answered this question"})
                else:
                    self.create(request, *args, **kwargs)
                    return Response({"success": "Thanks for your response :)"})
            else:
                return Response({"userInvalid": "You can't vote for others!!"})

    def get_queryset(self):
        user = self.request.user
        return Answer.objects.filter(user=user)


# register api view
class CreateUserAPIView(generics.CreateAPIView):
    model = get_user_model()
    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer


# register for admins
class CreateAdminAPIView(generics.CreateAPIView):
    model = get_user_model()
    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer
