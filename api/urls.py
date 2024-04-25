from django.urls import path
from .views import *


urlpatterns = [
    
path('admin_login', api_login.as_view(), name='admin_login'),
path('upload_reels', upload_reels.as_view(), name='upload_reels'),
path('delete_reels/<int:id>', delete_reels.as_view(), name='delete_reels'),

path('upload_pre_wedding', upload_pre_wedding.as_view(), name='upload_pre_wedding'),
path('get_pre_wedding/<int:id>', get_pre_wedding_indv.as_view(), name='get_pre_wedding_indv'),
path('edit_pre_wedding/<int:id>', edit_pre_wedding_indv.as_view(), name='edit_pre_wedding_indv'),
path('delete_pre_wedding/<int:id>/', delete_pre_wedding.as_view(), name='delete_pre_wedding'),


path('upload_wedding', upload_wedding.as_view(), name='upload_wedding'),
path('get_wedding/<int:id>', get_wedding_indv.as_view(), name='get_wedding_indv'),
path('edit_wedding/<int:id>', edit_wedding_indv.as_view(), name='edit_wedding_indv'),
path('delete_wedding/<int:id>', delete_wedding.as_view(), name='delete_wedding'),

path('upload_events', upload_events.as_view(), name='upload_events'),
path('get_events/<int:id>', get_events_indv.as_view(), name='get_events_indv'),
path('edit_events/<int:id>', edit_events_indv.as_view(), name='edit_events_indv'),
path('delete_events/<int:id>', delete_events.as_view(), name='delete_events'),


path('add_client', AddClient.as_view(), name='add_client'),
path('edit_client/<int:id>', EditClient.as_view(), name='edit_client'),
path('edit_client_user_edit/<int:id>', EditClientUserEdit.as_view(), name='edit_client_user_edit'),

path('add_booking/<int:id>', AddBooking.as_view(), name='add_booking'),
path('cancle_booking', CancleBooking.as_view(), name='cancle_booking'),
path('get_bookings/<str:date>/<int:page>', getBookings.as_view(), name='get_bookings'),

path('confirm_bookings/<int:id>/', confirmBooking.as_view(), name='confirm_bookings'),

path('submit_package/<int:id>', SubmitPackage.as_view(), name='submit_package'),

path('update_booking_status/<int:id>', UpdateBookingStatus.as_view(), name='update_booking_status'),


path('get_packages/<int:id>', GetPackages.as_view(), name='get_packages'),

path('get_additional_services', GetAdditionalServices.as_view(), name='get_additional_services'),
path('get_booked_services/<int:id>', GetBookedServices.as_view(), name='get_booked_services'),


path('get_services_invoice/<int:id>', GetServicesInvoice.as_view(), name='get_services_invoice'),


path('get_segment_service_admin', GetSegmentServicesAdmin.as_view(), name='get_segment_service_admin'),

path('add_service_admin', AddServicesAdmin.as_view(), name='add_service_admin'),
path('get_service_admin/<int:id>', GetServicesAdmin.as_view(), name='get_service_admin'),
path('update_service_admin/<int:id>', UpdateServicesAdmin.as_view(), name='update_service_admin'),
path('trash_service_admin/<int:id>', TrashServicesAdmin.as_view(), name='trash_service_admin'),


path('add_additional_service_admin', AddAdditionalServicesAdmin.as_view(), name='add_additional_service_admin'),
path('get_additional_service_admin/<int:id>', GetAdditionalServicesAdmin.as_view(), name='get_additional_service_admin'),
path('update_additional_service_admin/<int:id>', UpdateAdditionalServicesAdmin.as_view(), name='update_additional_service_admin'),
path('trash_additional_service_admin/<int:id>', TrashAdditionalServicesAdmin.as_view(), name='trash_additional_service_admin'),

path('add_package_admin', AddPackageAdmin.as_view(), name='add_package_admin'),
path('get_package_admin/<int:id>', GetPackageAdmin.as_view(), name='get_package_admin'),

path('get_all_package_admin/<int:id>', GetAllPackageAdmin.as_view(), name='get_all_package_admin'),
path('update_package_admin/<int:id>', UpdatePackageAdmin.as_view(), name='update_package_admin'),

path('add_banner_video_admin', AddHomeBannerVideoAdmin.as_view(), name='add_banner_video_admin'),
path('delete_banner_video_admin/<int:id>', DeleteHomeBannerVideoAdmin.as_view(), name='delete_banner_video_admin'),
path('add_showcase_image_admin', AddShowcaseImageAdmin.as_view(), name='add_showcase_image_admin'),
path('delete_showcase_image_admin/<int:id>', DeleteShowcaseImageAdmin.as_view(), name='delete_showcase_image_admin'),

path('add_team_member_admin', AddTeamMemberAdmin.as_view(), name='add_team_member_admin'),
path('get_team_member_indv_admin/<int:id>', GetTeamMemberIndvAdmin.as_view(), name='get_team_member_indv_admin'),
path('update_team_member_admin/<int:id>', UpdateTeamMemberIndvAdmin.as_view(), name='update_team_member_admin'),
path('delete_team_member_admin/<int:id>', DeleteTeamMemberIndvAdmin.as_view(), name='delete_team_member_admin'),



# path('get_package_service_admin/<int:id>', GetPackageServicesAdmin.as_view(), name='get_package_service_admin'),


path('payment_submit/<int:id>', PaymentSubmit.as_view(), name='payment_submit'),

path('generate_invoice/<int:id>', GenerateInvoice.as_view(), name='generate_invoice'),
path('generate_quotation/<int:id>', GenerateQuotation.as_view(), name='generate_quotation'),
path('save_quotation/<int:id>', SaveQuotation.as_view(), name='save_quotation'),
path('email_quotation/<int:id>/<int:discount>', EmailQuotation.as_view(), name='email_quotation'),


path('console_dashboard', ConsoleDashboard.as_view(), name='console_dashboard'),


path('trash_deliverables_admin/<int:id>', TrashDeliverablesAdmin.as_view(), name='trash_deliverables_admin'),
path('get_deliverables_admin/<int:id>', GetDeliverablesAdmin.as_view(), name='get_deliverables_admin'),
path('update_deliverables_admin/<int:id>', UpdateDeliverables.as_view(), name='update_deliverables_admin'),
path('add_deliverables_admin', AddDeliverablesAdmin.as_view(), name='add_deliverables_admin'),



path('trash_terms_conditions_admin/<int:id>', TrashTermsConditionAdmin.as_view(), name='trash_terms_conditions_admin'),
path('get_terms_conditions_admin/<int:id>', GetTermsConditionAdmin.as_view(), name='get_terms_conditions_admin'),
path('update_terms_conditions_admin/<int:id>', UpdateTermsCondition.as_view(), name='update_terms_conditions_admin'),
path('add_terms_conditions_admin', AddTermsConditionAdmin.as_view(), name='add_terms_conditions_admin'),



path('get_booking_ajax', GetBookingAjax.as_view(), name='get_booking_ajax'),
path('team_add_fund', teamAddFund.as_view(), name='team_add_fund'),
path('team_deposite', TeamDeposite.as_view(), name='team_deposite'),


path('create_walkin_client', CreateWalkinClient.as_view(), name='create_walkin_client'),




# path('vp', vp.as_view()),

# path('dashboard', api_login.as_view(), name='admin_login'),

]