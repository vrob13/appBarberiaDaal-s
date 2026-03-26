import streamlit as st
from streamlit_option_menu import option_menu
from google_calendar_class import GoogleCalendar
from google_sheets import GoogleSheet
from send_email import send
import numpy as np
import datetime as dt
from zoneinfo import ZoneInfo


# Session state
if "reserva_ok" not in st.session_state:
    st.session_state.reserva_ok = False

if "ultima_reserva" not in st.session_state:
    st.session_state.ultima_reserva = None


# Funciones
def add_30_minutes(time_str):
    time_format = "%H:%M"
    parsed_time = dt.datetime.strptime(time_str, time_format).time()
    time_datetime = dt.datetime.combine(dt.date.today(), parsed_time)
    new_time_datetime = time_datetime + dt.timedelta(minutes=30)
    return new_time_datetime


# Variables
servicios = [
    "corte degradado - $15.000",
    "Corte y Barba - $25.000",
    "Barba - $10.000",
    "cejas - $12.000",
]

empleados = ["Tadeo", "Matias"]

horas_disponibles = [
    "10:00", "10:30", "11:00", "11:30",
    "12:00", "12:30", "13:00", "13:30",
    "14:00", "14:30", "15:00", "15:30",
    "16:00", "16:30", "17:00", "17:30",
    "18:00", "18:30", "19:00"
]

calendarid1 = "9c63048600e350693680c531e5fa7aa16e46eb68d65de4948fa850e942751b61@group.calendar.google.com"
calendarid2 = "1b4db0e2f8e14a3c43ac85164158db4dde1e85a7c8e6f908ed75acb82471255d@group.calendar.google.com"
timezone = "America/Santiago"

document = "app-citas"
sheet = "citas"


# Page config
st.set_page_config(page_title="App de citas barberia", page_icon="💈", layout="centered")

st.image("assets/barberia.png")
st.title("Daal's Barber shop")
st.text("Av. Alameda 482, Región Metropolitana, Santiago de Chile")

selected = option_menu(
    menu_title=None,
    options=["Servicios", "Reseñas", "Portafolio", "Detalles"],
    icons=["scissors", "chat-dots", "file-text", "pin"],
    orientation="horizontal",
)


if selected == "Portafolio":
    st.image("assets/corte-1.jpg", caption="Degradado básico")
    st.image("assets/corte-2.jpg", caption="Corte")
    st.image("assets/corte-3.jpg", caption="Raya personalizada")
    st.image("assets/corte-4.jpg", caption="Afeitado Personalizado")
    st.image("assets/corte-5.jpg", caption="Corte tupe")


if selected == "Detalles":
    st.image("assets/map-banner.jpg")
    st.markdown("Pulsa [aquí](https://maps.app.goo.gl/KK4Q1FNCKb9UcV7n7) para ver la dirección en Google Maps.")

    st.subheader("Empleados")
    column1, column2 = st.columns(2)
    column1.image("assets/barber1.png", caption="Tadeo")
    column2.image("assets/barber2.png", caption="Matias")

    st.subheader("Horarios de apertura y contacto")
    st.write("----")
    st.markdown("**Teléfono:** +56 9 9724 3140")
    st.write("----")

    c1, c2 = st.columns(2)
    c1.text("Lunes")
    c2.text("10:00 - 19:00")
    c1.text("Martes")
    c2.text("10:00 - 19:00")
    c1.text("Miércoles")
    c2.text("10:00 - 19:00")
    c1.text("Jueves")
    c2.text("10:00 - 19:00")
    c1.text("Viernes")
    c2.text("10:00 - 19:00")
    c1.text("Sábado")
    c2.text("10:00 - 19:00")
    c1.text("Domingo")
    c2.text("Cerrado")

    st.write("---")
    st.markdown(
        """
        <a href="https://www.instagram.com/tadeodaal_?igsh=MTg2cHU0YzJ5MXdzNA==" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" width="32">
        </a>
        """,
        unsafe_allow_html=True
    )


if selected == "Reseñas":
    st.image("assets/review-1.jpg")
    st.image("assets/review-2.jpg")
    st.image("assets/review-3.jpg")
    st.image("assets/review-4.jpg")


if selected == "Servicios":
    st.subheader("Reservar cita")

    if st.session_state.reserva_ok:
        st.success("Su cita ha sido creada correctamente")
        st.session_state.reserva_ok = False

    with st.form("form_reserva", clear_on_submit=True):
        a1, a2 = st.columns(2)

        nombre = a1.text_input("Tu Nombre*")
        email = a2.text_input("Tu email*")
        fecha = a1.date_input("Fecha")
        servicio = a1.selectbox("Servicio*", servicios)
        empleado = a2.selectbox("Empleado", empleados)

        if empleado == "Tadeo":
            calendarid = calendarid1
        else:
            calendarid = calendarid2

        try:
            calendar = GoogleCalendar(calendarid)
            hours_blocked = calendar.get_start_times(str(fecha))
            result_hours = np.setdiff1d(horas_disponibles, hours_blocked).tolist()
        except Exception:
            result_hours = horas_disponibles

        hora = a2.selectbox("Horas disponibles", result_hours)
        nota = st.text_area("Nota (opcional)")

        enviar = st.form_submit_button("Reservar")

    if enviar:
        if not nombre or not email or not servicio:
            st.warning("Tienes que rellenar todos los campos obligatorios antes de reservar tu cita")
        else:
            reserva_actual = f"{nombre}|{email}|{fecha}|{hora}|{servicio}|{empleado}"

            if st.session_state.ultima_reserva == reserva_actual:
                st.warning("Esta cita ya fue registrada. No se volverá a crear.")
            else:
                with st.spinner("Cargando ..."):
                    try:
                        precio = servicio.split("-")[1].strip()

                        tz = ZoneInfo("America/Santiago")
                        parsed_time = dt.datetime.strptime(hora, "%H:%M").time()
                        end_hours = add_30_minutes(hora)

                        start_dt = dt.datetime(
                            fecha.year, fecha.month, fecha.day,
                            parsed_time.hour, parsed_time.minute,
                            tzinfo=tz
                        )

                        end_dt = dt.datetime(
                            fecha.year, fecha.month, fecha.day,
                            end_hours.hour, end_hours.minute,
                            tzinfo=tz
                        )

                        start_time = start_dt.isoformat()
                        end_time = end_dt.isoformat()

                        summary = f"{servicio} - {nombre}"

                        # Google Calendar
                        calendar_manager = GoogleCalendar(calendarid)
                        calendar_manager.create_event(summary, start_time, end_time, timezone)

                        # Envío de correo
                        send(email, nombre, fecha, hora, servicio, empleado)

                        # Google Sheets
                        data = [[
                            nombre,
                            email,
                            str(fecha),
                            str(hora),
                            servicio,
                            empleado,
                            nota,
                            precio
                        ]]
                        google = GoogleSheet(document, sheet)
                        rango = google.get_last_row_range()
                        google.write_data(rango, data)

                        st.session_state.ultima_reserva = reserva_actual
                        st.session_state.reserva_ok = True
                        st.rerun()

                    except Exception as e:
                        st.error(f"Ocurrió un error al reservar la cita: {e}")