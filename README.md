# Daal's Barber Shop 💈

Sistema web de reservas para barbería desarrollado con **Streamlit**, con integración a **Google Calendar**, **Google Sheets** y envío de **correos de confirmación**.

---

## Descripción

**Daal's Barber Shop** es una aplicación diseñada para gestionar reservas de citas de forma simple y automatizada.  
El sistema permite a los clientes seleccionar un servicio, escoger un barbero, elegir un horario disponible y registrar su cita en tiempo real.

Además, cada reserva:

- se registra en **Google Calendar**
- se almacena en **Google Sheets**
- envía un **correo de confirmación**
- evita duplicados en la misma reserva

---

## Características principales

- Reserva de citas desde una interfaz web sencilla
- Validación de horarios disponibles
- Selección de empleado/barbero
- Registro automático en Google Calendar
- Almacenamiento de datos en Google Sheets
- Envío de correo de confirmación al cliente
- Prevención de reservas duplicadas
- Secciones informativas de:
  - Servicios
  - Reseñas
  - Portafolio
  - Detalles del negocio

---

## Tecnologías utilizadas

- **Python**
- **Streamlit**
- **Google Calendar API**
- **Google Sheets API**
- **gspread**
- **SMTP / Gmail**
- **NumPy**
- **Pandas**

---

## Vista general del proyecto

Este proyecto fue creado como una aplicación funcional para una barbería, con enfoque en:

- automatización del proceso de reservas
- organización de citas
- experiencia simple para el usuario
- integración con herramientas reales de trabajo

---

## Estructura del proyecto

```bash
appBarberiaDaal-s/
├── assets/
├── styles/
├── .streamlit/
├── app.py
├── google_calendar_class.py
├── google_sheets.py
├── send_email.py
├── requirements.txt
├── .gitignore
└── README.md