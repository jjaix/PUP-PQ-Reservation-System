from typing import Literal

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton, MDButtonIcon
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogSupportingText, \
    MDDialogContentContainer, MDDialogButtonContainer, MDDialogIcon
from kivymd.uix.divider import MDDivider
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.widget import Widget
from kivymd.uix.pickers import MDModalDatePicker, MDTimePickerDialHorizontal, MDTimePickerDialVertical
from kivy.properties import ObjectProperty
from kivymd.theming import ThemeManager
from kivy.clock import Clock
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemLeadingIcon, \
    MDListItemSupportingText, MDListItemTertiaryText
from datetime import datetime
from db import db
from model import ReservationRequests


class CustomIconButton(MDIconButton):
    def __init__(self, icon, style, theme_icon_color, icon_color, reservation_item: ReservationRequests,
                 btn_pressed, app_root, **kwargs):
        super(CustomIconButton, self).__init__(**kwargs)
        self.icon = icon
        self.style = style
        self.theme_icon_color = theme_icon_color
        self.icon_color = icon_color
        self.reservation_item = reservation_item
        self.btn_pressed = btn_pressed
        self.app_root = app_root

    def on_release(self):
        if self.btn_pressed == "approve":
            self.on_approve_btn_pressed()
        else:
            self.on_deny_btn_pressed()

    def on_approve_btn_pressed(self):
        print(f"Approve button pressed: {self.reservation_item.id}")
        md = MDDialog(
            MDDialogIcon(icon="check-circle"),
            MDDialogHeadlineText(
                text="Reservation Request Approved!",
            ),
            MDDialogSupportingText(
                text=f"You approved the reservation request for a {self.reservation_item.item}.",
            ),
            MDDialogContentContainer(
                MDDivider(),
                orientation="vertical"
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(
                        text="Close",
                        theme_text_color="Custom",
                        text_color=(0, 0, 1, 1)
                    ),
                    style="text",
                    on_release=lambda _: md.dismiss()
                ),
                spacing="10"
            ),
            auto_dismiss=False,
        )

        md.open()

    def on_deny_btn_pressed(self):
        print(f"Deny button pressed: {self.reservation_item.id}")
        md = MDDialog(
            MDDialogIcon(icon="close-thick"),
            MDDialogHeadlineText(
                text="Reservation Request Denied.",
            ),
            MDDialogSupportingText(
                text=f"You denied the reservation request for a {self.reservation_item.item}.",
            ),
            MDDialogContentContainer(
                MDDivider(),
                orientation="vertical"
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(
                        text="Close",
                        theme_text_color="Custom",
                        text_color=(0, 0, 1, 1)
                    ),
                    style="text",
                    on_release=lambda _: md.dismiss()
                ),
                spacing="10"
            ),
            auto_dismiss=False,
        )

        md.open()


class WelcomeScreen(MDScreen):
    pass


class WindowManager(MDScreenManager):
    pass


class StudentLoginScreen(MDScreen):
    pass


class StudentDashboardScreen(MDScreen):
    pass


class AdminLoginScreen(MDScreen):
    pass


class AdminDashboardScreen(MDScreen):
    pass


class ReservationFormScreen(MDScreen):
    pass


class MainApp(MDApp):
    dialog = None
    reservations = []

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.bind(device_orientation=self.check_orientation)
        return Builder.load_file("main.kv")

    def on_start(self):
        self.load_reservations()

    def student_login(self):
        student_screen = self.root.get_screen("student_login_screen")
        student_email = student_screen.ids.student_email.text
        student_password = student_screen.ids.student_password.text

        # Example authentication logic
        if student_email == "student@gmail.com" and student_password == "password":
            self.root.current = "student_dashboard_screen"
        else:
            if not self.dialog:
                self.dialog = MDDialog(
                    MDDialogHeadlineText(
                        text="Login Failed",
                    ),
                    MDDialogSupportingText(
                        text=f"The username or password you entered is incorrect. Please try again.",
                    ),
                    MDDialogContentContainer(
                        MDDivider(),
                        orientation="vertical"
                    ),
                    MDDialogButtonContainer(
                        Widget(),
                        MDButton(
                            MDButtonText(
                                text="Close",
                                theme_text_color="Custom",
                                text_color=(0, 0, 1, 1)
                            ),
                            style="text",
                            on_release=lambda _: self.dialog.dismiss()
                        ),
                        spacing="10"
                    ),
                    auto_dismiss=False,
                )

            self.dialog.open()

    def show_date_picker(self, focus):
        self.theme_cls.primary_palette = "Maroon"

        if not focus:
            return

        date_dialog = MDModalDatePicker()
        date_dialog.bind(on_ok=self.on_get_date, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_get_date(self, instance):
        dt = str(instance.get_date()[0])
        self.root.get_screen("reservation_form_screen").ids.date.text = dt
        instance.dismiss()

    # TIME PICKER
    ORIENTATION = Literal["portrait", "landscape"]
    time_picker_horizontal: MDTimePickerDialHorizontal = ObjectProperty(
        allownone=True
    )
    time_picker_vertical: MDTimePickerDialHorizontal = ObjectProperty(
        allownone=True
    )

    def check_orientation(
            self, instance: ThemeManager, orientation: ORIENTATION
    ):
        if orientation == "portrait" and self.time_picker_horizontal:
            self.time_picker_horizontal.dismiss()
            hour = str(self.time_picker_horizontal.time.hour)
            minute = str(self.time_picker_horizontal.time.minute)
            Clock.schedule_once(
                lambda x: self.open_time_picker_vertical(hour, minute),
                0.1,
            )
        elif orientation == "landscape" and self.time_picker_vertical:
            self.time_picker_vertical.dismiss()
            hour = str(self.time_picker_vertical.time.hour)
            minute = str(self.time_picker_vertical.time.minute)
            Clock.schedule_once(
                lambda x: self.open_time_picker_horizontal(hour, minute),
                0.1,
            )

    def open_time_picker_horizontal(self, focus):
        self.theme_cls.primary_palette = "Maroon"

        if not focus:
            return

        self.time_picker_vertical = None
        self.time_picker_horizontal = MDTimePickerDialHorizontal()
        self.time_picker_horizontal.bind(on_ok=self.on_ok, on_cancel=self.on_cancel)
        self.time_picker_horizontal.open()

    def open_time_picker_vertical(self, focus):
        self.theme_cls.primary_palette = "Maroon"

        if not focus:
            return

        self.time_picker_horizontal = None
        self.time_picker_vertical = MDTimePickerDialVertical()
        self.time_picker_vertical.bind(on_ok=self.on_ok, on_cancel=self.on_cancel)
        self.time_picker_vertical.open()

    def on_ok(self, instance):
        tm = str(f"{int(instance.hour):02d}:{int(instance.minute):02d} {instance.am_pm.upper()}")
        self.root.get_screen("reservation_form_screen").ids.time.text = tm
        instance.dismiss()

    def on_cancel(self, instance):
        instance.dismiss()

    def admin_login(self):
        admin_screen = self.root.get_screen("admin_login_screen")
        admin_email = admin_screen.ids.admin_email.text
        admin_password = admin_screen.ids.admin_password.text

        # Example authentication logic
        if admin_email == "admin@pup.edu.ph" and admin_password == "admin":
            self.root.current = "admin_dashboard_screen"
        else:
            if not self.dialog:
                self.dialog = MDDialog(
                    MDDialogHeadlineText(
                        text="Login Failed",
                    ),
                    MDDialogSupportingText(
                        text=f"The username or password you entered is incorrect. Please try again.",
                    ),
                    MDDialogContentContainer(
                        MDDivider(),
                        orientation="vertical"
                    ),
                    MDDialogButtonContainer(
                        Widget(),
                        MDButton(
                            MDButtonText(
                                text="Close",
                                theme_text_color="Custom",
                                text_color=(0, 0, 1, 1)
                            ),
                            style="text",
                            on_release=lambda _: self.dialog.dismiss()
                        ),
                        spacing="10"
                    ),
                    auto_dismiss=False,
                )

            self.dialog.open()

    def add_reservation(self):
        item = self.root.get_screen("reservation_form_screen").ids.item
        name = self.root.get_screen("reservation_form_screen").ids.name
        program_year_section = self.root.get_screen("reservation_form_screen").ids.program_year_section
        contact_number = self.root.get_screen("reservation_form_screen").ids.contact_number
        email = self.root.get_screen("reservation_form_screen").ids.email
        date = self.root.get_screen("reservation_form_screen").ids.date
        time = self.root.get_screen("reservation_form_screen").ids.time
        prof = self.root.get_screen("reservation_form_screen").ids.prof

        today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        if (item.text != "" and name.text != "" and program_year_section.text != "" and contact_number.text != ""
                and email.text != "" and date.text != "" and time.text != "" and prof.text != ""):
            payload = {
                "item": item.text,
                "name": name.text,
                "program_year_section": program_year_section.text,
                "contact_number": contact_number.text,
                "email": email.text,
                "date": date.text,
                "time": time.text,
                "prof": prof.text,
                "updated": today
            }

            res = db.insert_reservation(list(payload.values()))

            if res:
                item.text = ""
                name.text = ""
                program_year_section.text = ""
                contact_number.text = ""
                email.text = ""
                date.text = ""
                time.text = ""
                prof.text = ""

                self.load_reservations()

                self.root.current = "admin_dashboard_screen"

    def load_reservations(self):
        reservations = db.select_all_reservations()
        container = self.root.get_screen("admin_dashboard_screen").ids.container
        container.clear_widgets()

        if len(reservations) > 0:
            for reservation in reservations:
                row: ReservationRequests = ReservationRequests(*reservation)
                reservation_item = MDListItem(
                    MDListItemLeadingIcon(
                        icon="note-text"
                    ),
                    MDListItemHeadlineText(
                        text=f"Reservation for: {row.item} | ID: {row.id}",
                    ),
                    MDListItemSupportingText(
                        text=f"Requested by: {row.name} ({row.program_year_section})",
                    ),
                    MDListItemTertiaryText(
                        text=f"Date of Reservation: {row.date} | Time of Using: {row.time}",
                    )
                )

                approve_btn = CustomIconButton(
                    icon="check-circle",
                    style="standard",
                    theme_icon_color="Custom",
                    icon_color=(0, 0, 1, 1),
                    btn_pressed="approve",
                    reservation_item=row,
                    app_root=self.root
                )

                deny_btn = CustomIconButton(
                    icon="close-circle",
                    style="standard",
                    theme_icon_color="Custom",
                    icon_color=(1, 0, 0, 1),
                    btn_pressed="deny",
                    reservation_item=row,
                    app_root=self
                )

                gl = MDGridLayout(
                    cols=2,
                    adaptive_width=True,
                )
                gl.add_widget(approve_btn)
                gl.add_widget(deny_btn)
                reservation_item.add_widget(gl)
                container.add_widget(reservation_item)
        else:
            container.add_widget(
                MDListItem(
                    MDListItemHeadlineText(
                        text="There are no reservation requests yet"
                    )
                )
            )

    # def updated_reservation_status(self, reservation, status):
    #     db.update_reservation_by_id(reservation, status)
    #
    #     for res in self.reservations:
    #         if res == reservation:
    #             res.status = status
    #
    #     self.load_reservations()
    #
    #     if status == "Approved":
    #         reservations = db.select_all_reservations()
    #         container = self.root.get_screen("admin_dashboard_screen").ids.container
    #         container.clear_widgets()
    #
    #         if len(reservations) > 0:
    #             for reservation in reservations:
    #                 row: ReservationRequests = ReservationRequests(*reservation)
    #                 reservation_item = MDListItem(
    #                     MDListItemLeadingIcon(
    #                         icon="note-text"
    #                     ),
    #                     MDListItemHeadlineText(
    #                         text=f"Reservation for: {row.item} | ID: {row.id}",
    #                     ),
    #                     MDListItemSupportingText(
    #                         text=f"Requested by: {row.name} ({row.program_year_section})",
    #                     ),
    #                     MDListItemTertiaryText(
    #                         text=f"Date of Reservation: {row.date} | Time of Using: {row.time}",
    #                     )
    #                 )
    #
    #                 status_info = MDButton(
    #                     MDButtonIcon(
    #                         icon="check-circle",
    #                         theme_icon_color="Custom",
    #                         icon_color=(0, 0, 1, 1)
    #                         ),
    #                     MDButtonText(
    #                         style="tonal",
    #                         text="Request Approved!",
    #                         halign="center",
    #                         theme_width="Custom",
    #                         height="56dp",
    #                         size_hint_x=.5,
    #                         theme_text_color="Custom",
    #                         text_color=(0, 0, 1, 1)
    #                     ),
    #                     style="text"
    #                 )
    #
    #                 gl = MDGridLayout(
    #                     cols=2,
    #                     adaptive_width=True,
    #                 )
    #                 gl.add_widget(status_info)
    #                 reservation_item.add_widget(gl)
    #                 container.add_widget(reservation_item)
    #
    #     elif status == "Denied":
    #         message = f"Reservation Denied for {reservation.first_name} {reservation.last_name}."
    #         self.show_popup(message)


if __name__ == '__main__':
    MainApp().run()
