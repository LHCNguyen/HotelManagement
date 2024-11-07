from flask_admin.contrib.sqla import ModelView

from app import admin, db, app
from app.models import User, Role, CustomerType, Room, Floor, Comment, Evaluation, Policy, Booking, PaymentMethod, Style, BookingDetail
from flask import session

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


class CustomerStyleView(ModelView):
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


class FloorView(ModelView):
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True


class CommentView(ModelView):
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True


class EvaluationView(ModelView):
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


class PaymentMethodView(ModelView):
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True


class StyleView(ModelView):
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
admin.add_view(CustomerStyleView(CustomerType, db.session))
admin.add_view(RoomView(Room, db.session))
admin.add_view(FloorView(Floor, db.session))
admin.add_view(CommentView(Comment, db.session))
admin.add_view(EvaluationView(Evaluation, db.session))
admin.add_view(PolicyView(Policy, db.session))
admin.add_view(BookingView(Booking, db.session))
admin.add_view(PaymentMethodView(PaymentMethod, db.session))
admin.add_view(StyleView(Style, db.session))
admin.add_view(BookingDetailView(BookingDetail, db.session))
