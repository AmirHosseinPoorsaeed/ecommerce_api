from djoser.serializers import \
    UserCreateSerializer as DjoserUserCreateSerializer, \
    UserSerializer as DjoserUserSerializer


class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        fields = ['id', 'username', 'email',
                  'password', 'first_name', 'last_name']


class UserSerializer(DjoserUserCreateSerializer):
    class Meta(DjoserUserSerializer.Meta):
        fields = ['id', 'username', 'email', 
                  'first_name', 'last_name']
