from rest_framework import serializers
from console.models import *


class loginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=UserAccount
        fields=['email','password']



class reelsUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    class Meta:
        # models=all_identifiers
        fields=["file"]


class AddBookingSerializer_RW(serializers.Serializer):
    # package = serializers.IntegerField()
    # event_type = serializers.CharField()
    additional_service = serializers.ListField(allow_empty=True)
    shoot_date = serializers.DateField()

class AddBookingPreWeddingSerializer_RW(serializers.Serializer):
    shoot_date = serializers.DateField()
    event_type = serializers.CharField()


class BookingDateSerializer(serializers.ModelSerializer):
    # event_type = serializers.CharField()
    user = serializers.IntegerField()
    package = serializers.IntegerField()
    additional_service = serializers.ListField(allow_empty=True)
    class Meta:
        model = Booking_ShootDate
        fields = '__all__'

    def validate(self, data):
        for d in data['additional_service']:
            count = d['count']
            try:
                additional_service = AdditionalService.objects.get(id = d['id'])
                if not additional_service:
                    serializers.ValidationError('additional service id not valid')
            except:
                    serializers.ValidationError('additional service id not valid')

            if not isinstance(count, int):
                serializers.ValidationError('count should be integer value')

        try:
            package = Package.objects.get(id = d['id'])
            if not package:
                serializers.ValidationError('package id not valid')
        except:
            serializers.ValidationError('package id not valid')

        try:
            user = UserAccount.objects.get(id = d['user'])
            if not user:
                serializers.ValidationError('user id not valid')
        except:
            serializers.ValidationError('user id not valid')
            
        # print('data',data)

        return data
    
    def create(self, validated_data):
        additional_service = validated_data['additional_service']
        package = validated_data['package']
        user = validated_data['user']
        del validated_data['additional_service']
        del validated_data['package']
        del validated_data['user']
        booking = Booking_ShootDate.objects.create(**validated_data)
        for d in additional_service:
            additional_service_bookings_serializer = additional_service_bookings.objects.create(additional_service= AdditionalService.objects.get(id = d['id']) ,count=d['count'] )
            booking.additional_service.add(additional_service_bookings_serializer)


        booking_serializer = Booking.objects.create(user = Client.objects.get(id=user), package = Package.objects.get(id=package))
        booking_serializer.shoot_date.add(booking)


        return booking_serializer



class BookingDatePreWeddingSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField()
    package = serializers.IntegerField()
    event_type = serializers.CharField()
    class Meta:
        model = Booking_ShootDate
        exclude = ['additional_service']

    def validate(self, data):
        try:
            package = Package.objects.get(id = data['package'])
            if not package:
                serializers.ValidationError('package id not valid')
        except:
            serializers.ValidationError('package id not valid')

        try:
            user = UserAccount.objects.get(id = data['user'])
            if not user:
                serializers.ValidationError('user id not valid')
        except:
            serializers.ValidationError('user id not valid')
            
        return data
    
    def create(self, validated_data):
        pass
        print('validated', validated_data)
        # additional_service = validated_data['additional_service']
        package = validated_data['package']
        user = validated_data['user']
        # del validated_data['additional_service']
        del validated_data['package']
        del validated_data['user']
        booking = Booking_ShootDate.objects.create(**validated_data)
        # for d in additional_service:
        #     additional_service_bookings_serializer = additional_service_bookings.objects.create(additional_service= AdditionalService.objects.get(id = d['id']) ,count=d['count'] )
        #     booking.additional_service.add(additional_service_bookings_serializer)


        booking_serializer = Booking.objects.create(user = Client.objects.get(id=user), package = Package.objects.get(id=package))
        booking_serializer.shoot_date.add(booking)


        return booking_serializer
    


class UpdateBookingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model=Booking
        fields = ['booking_status']




class AddBookingSerializer(serializers.ModelSerializer):
    # shoot_date = serializers.IntegerField()
    # user = serializers.IntegerField()
    # package = serializers.IntegerField()
    # additional_service = serializers.ListField(allow_empty=True)
    # # additional_service = serializers.IntegerField(many=True)
    # shoot_date = serializers.DateField()
    class Meta:
        model = Booking
        # exclude = ['shoot_date']
        fields = '__all__'

    def validate(self, data):
        if data['user'] is None or not ['user']:
            raise serializers.ValidationError('invalid user id')
        if not Package.objects.get(package = data['package']):
            raise serializers.ValidationError('invalid package id')
        # for d in data['additional_service']:
        #     if not AdditionalService.objects.get(id = d):
        #         raise serializers.ValidationError('invalid additional service id')
        return data
    

    def create(self, validated_data):
        additional_services = validated_data['additional_service']
        shoot_date = validated_data['shoot_date']

        print(shoot_date, additional_services)

        data = validated_data
        del data['additional_service']
        del data['shoot_date']


        
        booking = Booking.objects.create(**validated_data)
        for d in additional_services:
            booking.additional_service.add(AdditionalService.objects.get(id = d))
        booking.shoot_date.add(Booking_ShootDate.objects.get(id = shoot_date))
        return booking
    
        # return super().create(validated_data)
    

class GetBookingSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    date = serializers.DateField()
    client_name = serializers.CharField()
    additional_service = serializers.ListField()
        


class UpdateBookingServiceSerializer(serializers.ModelSerializer):
    # package = serializers.ListField(allow_empty=True)
    # package
    date = serializers.DateField()
    # event_type = serializers.CharField()
    additional_service = serializers.ListField(allow_empty=True)
    class Meta:
        model = Booking
        fields = ['date', 'additional_service']

    def validate(self, data):
        # print('attrs',data)
        for d in data['additional_service']:
            count = d['count']
            try:
                additional_service = AdditionalService.objects.get(id = d['id'])
                if not additional_service:
                    serializers.ValidationError('additional service id not valid')
            except:
                    serializers.ValidationError('additional service id not valid')

            if not isinstance(count, int):
                serializers.ValidationError('count should be integer value')
        # try:
        #     package = Package.objects.get(id = d['id'])
        #     if not package:
        #         serializers.ValidationError('package id not valid')
        # except:
        #     serializers.ValidationError('package id not valid')
        return data

    def update(self, instance, validated_data):
        # instance.package = validated_data['package']
        new_date = True
        for d in instance.shoot_date.all():
            if str(d.date) == str(validated_data['date']):
                new_date = False
                # print('validated_data["event_type"]',validated_data['event_type'])
                # d.event_type = validated_data['event_type']
                d.additional_service.clear()
                for s in validated_data['additional_service']:
                    additional_service_bookings_serializer = additional_service_bookings.objects.create(additional_service=AdditionalService.objects.get(id = s['id']) ,count=s['count'] )
                    d.additional_service.add(additional_service_bookings_serializer)
                d.save()

        if new_date:

            additional_service = validated_data['additional_service']
            # instance.package = validated_data['package']
            del validated_data['additional_service']
            # del validated_data['package']

            booking = Booking_ShootDate.objects.create(**validated_data)
            for d in additional_service:
                print(booking, 'asdf', d['id'])
                additional_service_bookings_serializer = additional_service_bookings.objects.create(additional_service=AdditionalService.objects.get(id=d['id']),count=d['count'])
                booking.additional_service.add(additional_service_bookings_serializer)
            instance.shoot_date.add(booking)
        instance.save()

        # additional_service = validated_data['additional_service']

        # for d in additional_service:
        #     print('d',d)

        # instance.date = validated_data['']
        # instance.event_type = validated_data['event_type']
        # instance.additional_service.clear()


        # package = validated_data['package']
        # user = validated_data['user']
        # del validated_data['additional_service']
        # del validated_data['package']
        # del validated_data['user']
        # booking = Booking_ShootDate.objects.create(**validated_data)
        # for d in additional_service:
        #     additional_service_bookings_serializer = additional_service_bookings.objects.create(additional_service= AdditionalService.objects.get(id = d['id']) ,count=d['count'] )
        #     booking.additional_service.add(additional_service_bookings_serializer)
        # booking_serializer = Booking.objects.create(user = Client.objects.get(id=user), package = Package.objects.get(id=package))
        # booking_serializer.shoot_date.add(booking)
        # return booking_serializer

        # print('asdfasdfsadfsdf***********',validated_data)

        return instance


class UpdateBookingPreWeddingServiceSerializer(serializers.ModelSerializer):
    date = serializers.DateField()
    event_type = serializers.CharField()
    class Meta:
        model = Booking
        fields = ['date','event_type']

    # def validate(self, data):
    #     print('data',data)
    def update(self, instance, validated_data):
        print('instance **********88',instance)
        booking = Booking_ShootDate.objects.create(**validated_data)
        instance.shoot_date.add(booking)
        instance.save()

        return instance
        # return super().update(instance, validated_data)
    # return data


class PackageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['package']

        




class GetServicesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Service
        fields = '__all__'


class GetPackageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    price = serializers.IntegerField()
    package = serializers.CharField()
    segment = serializers.CharField()
    booked_package = serializers.DictField()
    service = serializers.ListField()



class AdditionalServiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    # segment = serializers.CharField()
    class Meta:
        model = AdditionalService
        exclude = ['segment']

class ServiceMainSerializer(serializers.Serializer):
    # service = serializers.ListField()
    additional_service = serializers.ListField()


# class preWeddingUploadSerializer(serializers.Serializer):
#     poster = serializers.FileField()
#     class Meta:
        

class GetBookedServicesSerializer(serializers.Serializer):
    shoot_date = serializers.DictField()
    # booked_service = serializers.ListField()
    booked_additional_service = serializers.ListField()


class GetServicesInvoiceSerializer(serializers.Serializer):
    package = serializers.CharField()
    package_price = serializers.IntegerField()
    additionals_total_price = serializers.IntegerField()
    total_price = serializers.IntegerField()
    remaining_payment = serializers.IntegerField()
    discount = serializers.IntegerField()
    service = serializers.ListField()
    additionals = serializers.ListField()



# class GenerateInvoiceSerializer(serializers.Serializer):
#     discount = serializers.IntegerField()

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'

class BookingDiscountPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class UpdateDiscountSerializer(serializers.ModelSerializer):
    discount = serializers.IntegerField()
    class Meta:
        model = Booking
        fields = ['discount']




class GenerateInvoiceSerializer(serializers.Serializer):
    invoice = serializers.FileField()

class GenerateQuotationSerializer(serializers.Serializer):
    quotation = serializers.FileField()

class SaveQuotationSerializer(serializers.Serializer):
    discount = serializers.IntegerField()


class PreWeddingSerializer(serializers.ModelSerializer):
    cover_picture = serializers.CharField()
    video_link = serializers.CharField(allow_null=True)

    class Meta:
        model = Pre_Wedding
        fields = '__all__'


class WeddingSerializer(serializers.ModelSerializer):
    cover_picture = serializers.CharField()
    video_link = serializers.CharField(allow_null=True)

    class Meta:
        model = Wedding
        fields = '__all__'


class EventsSerializer(serializers.ModelSerializer):
    cover_picture = serializers.CharField()
    video_link = serializers.CharField(allow_null=True)

    class Meta:
        model = Events
        fields = '__all__'

class SegmentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    segment = serializers.CharField()


class GetServiceSerializer(serializers.ModelSerializer):
    segment = serializers.DictField()
    class Meta:
        model = Service
        fields = '__all__'

class AddServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class AddAdditionalServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalService
        fields = '__all__'


class GetAdditionalServiceSerializer(serializers.ModelSerializer):
    segment = serializers.DictField()
    class Meta:
        model = AdditionalService
        fields = '__all__'


class GetDeliverablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deliverables
        fields = '__all__'



class GetTermsConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terms_Conditions
        fields = '__all__'



class AddPackageSerializer(serializers.ModelSerializer):
    service = serializers.ListField()
    class Meta:
        model = Package
        fields = '__all__'

    def validate(self, attrs):
        print('attrs',attrs)
        for s in attrs.get('service'):
            try:
                Service.objects.filter(id=s)
            except:
                raise serializers.ValidationError('no service found')
            
        return attrs
    
    def update(self, instance, validated_data):
        # service = validated_data['service']
        # del validated_data['service']
        instance.package = validated_data['package']
        instance.price = validated_data['price']
        instance.segment = validated_data['segment']
        instance.service.clear()
        # instance.service = validated_data['service']
        # package = Package.objects.create(**validated_data)
        print('service',instance.service.all())
        print('validated_data[service]',validated_data['service'])

        for s in validated_data['service']:
            instance.service.add(s)
        
        instance.save()
        # return super().create(validated_data)
        return instance


    #     return super().update(instance, validated_data)
    
    # def upda(self, validated_data):
    #     # print('validated_data',validated_data)

    #     # return
    

class getPackageSerializer(serializers.Serializer):
    class Meta:
        model = Package
        fields = '__all__'


class HomeBannerVideoSerializer(serializers.Serializer):
    class Meta:
        model = Banner_video
        fields = '__all__'


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team_member
        fields = '__all__'


class ConsoleDashboardSerializer(serializers.Serializer):
    total_payment = serializers.IntegerField()
    booking = serializers.IntegerField()
    client = serializers.IntegerField()
    pre_wedding = serializers.IntegerField()
    wedding = serializers.IntegerField()
    events = serializers.IntegerField()
    reels = serializers.IntegerField()


class teamAddFundSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField()
    # booking = serializers.IntegerField()
    note = serializers.CharField(max_length=100)
    class Meta:
        model = fund_history
        fields = '__all__'


class TeamDepositeSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField()
    note = serializers.CharField(max_length=100)
    class Meta:
        model = payments_history
        fields = '__all__'
    


class GetBookingAjaxSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    date = serializers.DateField()
    name = serializers.CharField()


class CreateWalkinClientSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    email_id = serializers.EmailField()
    contact_number = serializers.CharField()
    wedding_date = serializers.DateField()
    class Meta:
        model = Client
        fields = ['name', 'email_id', 'contact_number', 'wedding_date']


# class getPackageServicesSerializer(serializers.ModelSerializer):

#     class Meta:
#         model: Package
#         fields: '__all__'

    # def validate(self, attrs):
    #     print('attrs',)
        # return super().validate(attrs)

        # return super().validate(attrs)

# class TrashServiceSerializer(serializers.Serializer):
#     trash = serializers.BooleanField()


