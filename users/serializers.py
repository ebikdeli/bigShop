"""
** Unlike Models and signals that we should use 'settings.AUTH_USER_MODEL' instead of 'get_user_model' method,
in serializers and filtersets we can't use 'AUTH_USER_MODEL' or stringized <app_name.Model_Name>' or we get
this error:
AttributeError: 'str' object has no attribute '_meta'
https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#referencing-the-user-model

** To have a independent app, we defined our Generic serailizer here too.
We are following this document to define serializer for Generic serailizer:
https://www.django-rest-framework.org/api-guide/relations/#generic-relationships

** In this module AddressSerializer 'create' and 'update' methods are overrided to be able to create and update
address using diffrent methods and update or create Address with 1- DRF standard GUI and 2- Via client-server
architectures like React or Vue. And even we client could get address 'user' field is a nested serializer and
gets its data from 'address' serializer.

** If we need to use 'request' object for 'HyperlinkedModelSerializer', 'HyperlinkedFields' or anything else
we must sure to send 'request' object by 'context' attribute in the Serializer. It's important to know that
we can access to 'context' structure with 'context' attribute in Serializer. This is very useful when
we want to use context data in methods for eg:'to represent', 'validate', 'update' and 'create'.
For more information about extra context read below document:
https://www.django-rest-framework.org/api-guide/serializers/#including-extra-context

** We used 'Serializer Inheritance' to be able to use 'nested relations' for 'Address' in 'User' Model.
If we want to not include a field in child serializer from parent serializer, we just need to set its value to 'None'.
for more information read below documents:
https://www.django-rest-framework.org/api-guide/serializers/#serializer-inheritance
https://www.django-rest-framework.org/api-guide/relations/#nested-relationships
"""
# from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Address


class UserSerializer(serializers.HyperlinkedModelSerializer):
# class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    url = serializers.HyperlinkedIdentityField(view_name='accounts:user-detail',
					                           # If change 'lookup_field' in the UserViewset:
                                               lookup_field=get_user_model().USERNAME_FIELD
                                              )
    """
    We can't use 'user_address' field here because this module can't identify 'AddressSerializer' yet:
    # user_address = AddressSerializer(many=True, read_only=True)
    TO do that we can Inherit from 'UserSerializer' after 'AddressSerializer'.
    NOTE: We can't use every name for nested field. The field name must be the value we set for
    'relation_field' arguement in ForeignKey field.
    """

    class Meta:
        # model = settings.AUTH_USER_MODEL  <==> This is wrong! We should use below command instead:
        model = get_user_model()
        fields = [
                  'url',
                  'username', 'password', 'email', 'name', 'is_active',
                  'is_staff', 'is_admin', 'is_superuser',]
        extra_kwargs = {
            'password': {'write_only': True,
                         'style': {'input_type': 'password'}}
        }
        # https://www.django-rest-framework.org/api-guide/fields/#style


class AddressSerializer(serializers.HyperlinkedModelSerializer):
# class AddressSerializer(serializers.ModelSerializer):
    """Serializer for Address model"""
    url = serializers.HyperlinkedIdentityField(view_name='accounts:address-detail')
    user = UserSerializer(read_only=True, many=False)
    """IMPORTANT: If we have 'allow_null' field, it's highly recommended to set it's 'default=None' arguement."""
    user_obj = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(),
                                                  many=False,
                                                  write_only=True,
                                                  allow_null=True,
                                                  default=None)
    username = serializers.CharField(write_only=True, allow_null=True, default=None)

    class Meta:
        # model = 'accounts.Address'    <==> This command is wrong! We should below line instead:
        model = Address
        fields = '__all__'
        """
        By default a 'ForeignKey' field is a 'PrimaryRealtedField' and it's not return ForeignRelation Model
        data as nested. So to have nested relation we should use 'Serializer' field. More information in below link:
        https://www.django-rest-framework.org/api-guide/relations/#nested-relationships
        extra_kwargs = {
            'user': {'queryset': get_user_model().objects.all(),
                     'many': False,
                     'view_name': 'accounts:user-detail'}
        }
        """
    
    def create(self, validated_data):
        """
        Override serializer 'create' method to be able to create new 'Address' with
        both DRF standard GUI and client-server architecture.
        """
        # First we should pop additional fields from validated data to prevent 'TypeError'
        user_obj = validated_data.pop('user_obj', None)
        username = validated_data.pop('username', None)

        # 1- Create address from DFR GUI
        if user_obj:
            validated_data.update({'user': user_obj})
            address = Address.objects.create(**validated_data)
            return address

        # 2- Create address with client-server architecture
        elif username:
            q_user = get_user_model().objects.filter(username=username)
            if q_user.exists():
                user = q_user.last()
                validated_data.update({'user': user})
                address = Address.objects.create(**validated_data)
                return address
            else:
                raise ValidationError('Error: There is no user with this username')
        
        # If there is no user object or username entered raise this error
        else:        
            raise ValidationError(detail={'Error': 'No user object or username entered!'})
        
    def update(self, instance, validated_data):
        """
        Overriding 'update' method to support methods to update 'Address' object with DRF GUI or from
        client side technologies in client-server architecture.
        """
        # First we should pop additional fields from validated data to prevent 'TypeError'
        user_obj = validated_data.pop('user_obj', None)
        username = validated_data.pop('username', None)

        # 1- Update address with DRF GUI
        if user_obj:
            validated_data.update({'user': user_obj})
            Address.objects.filter(id=instance.id).update(**validated_data)
            # https://docs.djangoproject.com/en/4.0/ref/models/instances/#django.db.models.Model.refresh_from_db
            instance.refresh_from_db()
            return instance

        # 2- Update ticket with client-server architecture
        elif username:
            user_q = get_user_model().objects.filter(username=username)
            if user_q.exists():
                user = user_q.first()
                validated_data.update({'user': user})
                Address.objects.filter(id=instance.pk).update(**validated_data)
                instance.refresh_from_db()
                return instance
            else:
                raise ValidationError(detail=f'No user found with this username: {username}')

        # If No username or user_obj selected to update the instance
        raise ValidationError({'Error': 'No username or user object found!'})


class UserNewSerializer(UserSerializer):
    """
    This serializer inherited from UserSerializer and takes all the fields and methods of the parent
    Serializer.
    """
    # This field name must be the same as 'related_name' arguement in 'user' field in 'Address' Model:
    user_address = AddressSerializer(many=True, read_only=True)
    # Below field used for test purpose! But be aware if we use default 'create' and 'update' methods,
    # This field cause 'TypeError' as it's a unexpected keyword argument.
    # some_field = serializers.CharField(default='Test field')

    # To not include a field from parent in child (eg):
    # name = None

    class Meta(UserSerializer.Meta):
        fields = [
                  'url',
                  'username', 'password', 'email', 'name', 'is_active',
                  'is_staff', 'is_admin', 'is_superuser', 'user_address',
                  # 'some_field',
                  ]
