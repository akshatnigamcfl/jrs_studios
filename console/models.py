from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser)


# Create your models here.


class UserAccountManager(BaseUserManager):
	def create_user(self , email , password = None):
		if not email or len(email) <= 0 :
			raise ValueError("Email field is required !")
		if not password :
			raise ValueError("Password is must !")
		
		user = self.model(
			email = self.normalize_email(email) ,
		)
		user.set_password(password)
		user.save(using = self._db)
		return user
	
	def create_superuser(self , email , password):
		user = self.create_user(
			email = self.normalize_email(email),
			password = password
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using = self._db)
		return user
      


	
class UserAccount(AbstractBaseUser):
    name = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length = 200 , unique = True)
    employee_id = models.CharField(max_length=100, null=False, unique=True)
    contact_number = models.CharField(max_length=300, blank=True, default='')
    profile_picture = models.URLField(max_length=200)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = True)
    is_superuser = models.BooleanField(default=False)
    user_role = models.CharField(max_length=300, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True


class Banner_video(models.Model):
    title = models.CharField(max_length=50, default='')
    file = models.FileField(upload_to='assets/videos/Banner_video')

class Showcase_images(models.Model):
    title = models.CharField(max_length=50, default='')
    file = models.FileField(upload_to='assets/images/showcase_image')


class Reels(models.Model):
    title = models.CharField(max_length=50, default='')
    description = models.CharField(max_length=50, default='')
    file = models.FileField(upload_to='assets/videos/reels')
    created_at = models.DateField(auto_now_add=True)
    def __str__(self): return str(self.title) 


class Pre_Wedding(models.Model):
    title = models.CharField(max_length=50, default='')
    description = models.CharField(max_length=500, default='')
    date = models.DateField(auto_now=False, auto_now_add=False, default="0001-01-01")
    cover_picture = models.FileField(upload_to='assets/images/pre_wedding_poster')
    is_youtube_video = models.BooleanField()
    video_link = models.FileField(upload_to='assets/video/pre_wedding', null=True, blank=True, default='')
    video_youtube_link = models.TextField(null=True)
    views = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    def __str__(self): return str(self.title) 



class Wedding(models.Model):
    title = models.CharField(max_length=50, default='')
    description = models.CharField(max_length=500, default='')
    date = models.DateField(auto_now=False, auto_now_add=False, default="0001-01-01")
    cover_picture = models.FileField(upload_to='assets/images/wedding_poster')
    is_youtube_video = models.BooleanField()
    video_link = models.FileField(upload_to='assets/video/wedding', null=True)
    video_youtube_link = models.TextField(null=True)
    views = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    def __str__(self): return str(self.title)


class Events(models.Model):
    title = models.CharField(max_length=50, default='')
    description = models.CharField(max_length=500, default='')
    date = models.DateField(auto_now=False, auto_now_add=False, default="0001-01-01")
    cover_picture = models.FileField(upload_to='assets/images/events_poster')
    is_youtube_video = models.BooleanField()
    video_link = models.FileField(upload_to='assets/video/events', null=True)
    video_youtube_link = models.TextField(null=True)
    views = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    def __str__(self): return str(self.title)


class ClientSource(models.Model):
    title = models.CharField(max_length=50)


class Client(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    contact_number = models.CharField(max_length=500, null=False, blank=False)
    email_id = models.EmailField(max_length=254)
    wedding_date = models.DateField(null=True, blank=True, default='0001-01-01')
    groom_name = models.CharField(max_length=100, null=True, blank=True, default='')
    groom_Email_id = models.CharField(max_length=100, null=True, blank=True, default='')
    groom_contact_number = models.CharField(max_length=100, null=True, blank=True, default='')
    groom_date_of_birth = models.DateField(null=True, blank=True, default='0001-01-01')
    bride_name = models.CharField(max_length=100, null=True, blank=True, default='')
    bride_Email_id = models.CharField(max_length=100, null=True, blank=True, default='')
    bride_date_of_birth = models.DateField(null=True, blank=True, default='0001-01-01')
    wedding_venue = models.CharField(max_length=100, null=True, blank=True, default='')
    client_token = models.CharField(max_length=100, null=True, blank=True, default='')
    profile = models.FileField(upload_to='assets/images/user/profile-picture', null=True, blank=True, default='assets/images/user/profile-picture/user.png')
    booking = models.ForeignKey("console.booking", on_delete=models.CASCADE, null=True, blank=True, default='')
    source = models.ForeignKey(ClientSource, on_delete=models.CASCADE, null=True, blank=True)
    # qoutation = models.ManyToManyField("console.Quotation")
    created_at = models.DateField(auto_now_add=True)
    def __str__(self): return str(self.name)



class fund_history(models.Model):
    date = models.DateField(null=True, blank=True, auto_now=True)
    note = models.CharField(max_length=100, null=True, blank=True, default='')
    booking = models.ForeignKey("console.booking", on_delete=models.CASCADE, null=True, blank=True, default='')
    amount = models.IntegerField(default=0)


class payments_history(models.Model):
    date = models.DateField(null=True, blank=True, default='0001-01-01')
    note = models.CharField(max_length=100, null=True, blank=True, default='')
    # booking = models.ForeignKey("console.booking", on_delete=models.CASCADE, null=True, blank=True, default='')
    amount = models.IntegerField(default=0)


class Team_member(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    contact_number = models.CharField(max_length=500, null=False, blank=False)
    email_id = models.EmailField(max_length=254)
    trash = models.BooleanField(default=False)
    fund = models.ManyToManyField(fund_history)
    payments = models.ManyToManyField(payments_history)
    def __str__(self): return str(self.name)



class Segment(models.Model):
    segment = models.CharField(max_length=50)
    def __str__(self): return str(self.segment)


class Service(models.Model):
    service_name = models.CharField(max_length=100)
    # price = models.IntegerField()
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE)
    trash = models.BooleanField(default=False)
    # charges_application = models.CharField(max_length=100, null=True, default="complete_shoot")
    def __str__(self): return str(self.service_name)


class AdditionalService(models.Model):
    service_name = models.CharField(max_length=100)
    price = models.IntegerField()
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE)
    # segment = models.CharField(max_length=100)
    trash = models.BooleanField(default=False)
    # charges_application = models.CharField(max_length=100,null=True, default="per_day")
    def __str__(self): return str(self.service_name)


class Drp_booking_status(models.Model):
    title = models.CharField( max_length=50)
    def __str__(self): return str(self.title)


class additional_service_bookings(models.Model):
    additional_service = models.ForeignKey(AdditionalService, on_delete=models.CASCADE, null=True, blank=True)
    count = models.IntegerField()
    def __str__(self): return str(self.additional_service)


class Booking_ShootDate(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False)
    event_type = models.CharField(max_length=50)
    additional_service = models.ManyToManyField(additional_service_bookings)
    def __str__(self): return str(self.date)



class Package(models.Model):
    package = models.CharField(max_length=50)
    price = models.IntegerField()
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE)
    service = models.ManyToManyField(Service)
    trash = models.BooleanField(default=False)
    def __str__(self): return str(self.package)



class Booking(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateField(auto_now_add=True)
    booking_status = models.ForeignKey(Drp_booking_status, on_delete=models.CASCADE, default=1)
    shoot_date = models.ManyToManyField(Booking_ShootDate)
    #  package = models.ManyToManyField(Package)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True, blank=True)
    discount = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    # deliverables = models.ManyToManyField("console.Deliverables")
    # terms_conditions = models.ManyToManyField("console.Terms_Conditions")

    #  pre_wedding_shoot = models.BooleanField(default=False)
    #  additional_service = models.ManyToManyField(AdditionalService)
    def __str__(self): return str(self.user.name)



class Payments(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    amount = models.IntegerField()
    payment_mode = models.CharField(max_length=20, null=True, blank=True)
    payment_note = models.CharField(max_length=300, null=True, blank=True)
    def __str__(self): return str(self.user)


class Invoice(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    # total_price = models.IntegerField()
    # discount = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    payment = models.ForeignKey(Payments, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self): return str(self.user.name)


class Deliverables(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    trash = models.BooleanField(default=False)
    def __str__(self): return str(self.title)


class Terms_Conditions(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    trash = models.BooleanField(default=False)
    def __str__(self): return str(self.title)



# class Quotation(models.Model):
#     # user = models.ForeignKey(Client, on_delete=models.CASCADE)
#     # total_price = models.IntegerField()
#     # discount = models.IntegerField()
#     date = models.DateField(auto_now_add=True)
#     # package = 
#     total_price = models.IntegerField(default=0)
#     additional_price = models.IntegerField(default=0)
#     discount = models.IntegerField(default=0)
#     payment = models.ForeignKey(Payments, on_delete=models.CASCADE, null=True, blank=True)
#     def __str__(self): return str(self.date)


class canned_email(models.Model):
    email = models.TextField()
    email_type = models.CharField( max_length=50, null=True, blank=True)
    def __str__(self): return str(self.email_type)

    

# class mouFile(models.Model):
#     file = models.FileField(upload_to='mou')

# class paymentProofFile(models.Model):
#     file = models.FileField(upload_to='payment_proof')