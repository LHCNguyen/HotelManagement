from app import admin
from app.models import *
from flask_admin.contrib.sqla import ModelView

class UserView(ModelView):
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True
    column_filters = ['citizen_id', 'address', 'email', 'username', 'phone_number', 'fullname']
    column_searchable_list = ['citizen_id', 'address', 'email', 'username', 'phone_number', 'fullname']


class RoleView(ModelView):
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True


class RoomView(ModelView):
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True



class PolicyView(ModelView):
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True


class BookingView(ModelView):
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True



class BookingDetailView(ModelView):
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True


admin.add_view(UserView(User, db.session))
admin.add_view(RoleView(Role, db.session))
admin.add_view(RoomView(Room, db.session))
admin.add_view(PolicyView(Policy, db.session))
admin.add_view(BookingView(Booking, db.session))
admin.add_view(BookingDetailView(BookingDetail, db.session))
