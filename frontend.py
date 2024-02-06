import streamlit as st
import pandas as pd
import requests

BASE_URL = "http://localhost:8000"


# Función para cargar una infracción
def cargar_infraccion(data):
    response = requests.post(f"{BASE_URL}/persons/", json=data)
    return response


def datos_ordenados_id(datos):
    datos_ordenados = sorted(datos, key=lambda x: x["id"])

    # Convertir los datos ordenados a un DataFrame de pandas
    df = pd.DataFrame(datos_ordenados)
    if "id" in df.columns:
        cols = ["id"] + [col for col in df.columns if col != "id"]
        df = df[cols]
    return datos


def obtener_datos(endpoint):
    # 
    response = requests.get(f"{BASE_URL}/{endpoint}/")
    return response.json() if response.status_code == 200 else None


# Función para generar un informe
def create_data(data, endpoint):
    # 
    response = requests.post(f"{BASE_URL}/{endpoint}/", json=data)
    return response.json()


def delete_data(person_id, endpoint):
    response = requests.delete(f"{BASE_URL}/{endpoint}/{person_id}")
    return response


def update_data(endpoint, item_id, data):

    response = requests.put(f"{BASE_URL}/{endpoint}/{item_id}", json=data)
    return response


def actualizar_campos(person_id, nuevo_nombre, nuevo_email):
    data = {}
    if nuevo_nombre:
        data["name"] = nuevo_nombre
    if nuevo_email:
        data["email"] = nuevo_email
    response = update_data("persons", person_id, data)
    return response


def actualizar_campos_actualizados(
    person_id, nuevo_nombre, nuevo_owner_name, nuevo_brand, nuevo_color
):
    data_actualizado = {}

    if nuevo_nombre:
        data_actualizado["name"] = nuevo_nombre
    if nuevo_owner_name:
        data_actualizado["owner_name"] = nuevo_owner_name
    if nuevo_brand:
        data_actualizado["brand"] = nuevo_brand
    if nuevo_color:
        data_actualizado["color"] = nuevo_color
    response = update_data("vehicles", person_id, data_actualizado)
    return response


def actualizar_campos_officer(person_id, nuevo_nombre, nuevo_badge_number):
    data = {}
    if nuevo_nombre:
        data["name"] = nuevo_nombre
    if nuevo_badge_number:
        data["badge_number"] = nuevo_badge_number
    response = update_data("officers", person_id, data)
    return response


operaciones_persona = ["Crear", "Mostrar", "Actualizar", "Borrar"]
operaciones_vehiculo = ["Crear", "Mostrar", "Actualizar", "Borrar"]
operaciones_oficial = ["Crear", "Mostrar", "Actualizar", "Borrar"]


# Interfaz administrativa
def main():
    st.title("Sistema de Registro de Infracciones de Tráfico")
    st.title("Gestión de Registros")

    # Selección de operación para la entidad Persona
    # st.subheader("Gestión de Personas")
    seleccion = st.sidebar.radio("Ir a:", ["Personas", "Policias", "Patentes"])

    if seleccion == "Personas":
        st.subheader("Gestión de Personas")
        operacion_persona = st.selectbox(
            "Seleccione una operación", operaciones_persona
        )

        if operacion_persona == "Mostrar":
            st.subheader("Mostrar")
            datos = obtener_datos("persons")
            if datos:
                df = datos_ordenados_id(datos)
                st.write("Datos obtenidos:")
                st.table(df)

        elif operacion_persona == "Crear":
            st.subheader("crear")
            name = st.text_input("Ingrese nombre completo")
            email = st.text_input("Ingrese correo electronico")
            if st.button("crear"):
                response = create_data({"name": name, "email": email}, "persons")
                # 
                st.success(f"Item created successfully!{response}")

        elif operacion_persona == "Actualizar":
            st.subheader("Actualizar")
            datos = obtener_datos("persons")

            if datos:
                dict_personas = {
                    persona["id"]: f"{persona['name']} - {persona['email']}"
                    for persona in datos
                }

                selected_person_id = st.selectbox(
                    "Seleccione una persona para actualizar:",
                    list(dict_personas.keys()),
                    format_func=lambda id: dict_personas[id],
                )
                persona_seleccionada = next(
                    persona for persona in datos if persona["id"] == selected_person_id
                )
                # 
                st.write(f"Nombre actual: {persona_seleccionada['name']}")
                st.write(f"Email actual: {persona_seleccionada['email']}")
                nuevo_nombre = st.text_input("Nuevo nombre (opcional):")
                nuevo_email = st.text_input("Nuevo email (opcional):")
                if st.button("Actualizar"):
                    if not nuevo_nombre and not nuevo_email:
                        st.warning(
                            "Por favor, ingrese al menos un campo para actualizar."
                        )
                    elif nuevo_nombre and not nuevo_email:
                        update_response = actualizar_campos(
                            selected_person_id, nuevo_nombre, nuevo_email
                        )
                        if update_response.status_code == 200:
                            st.success(
                                f"Los campos de la persona con ID {selected_person_id} se actualizaron correctamente."
                            )
                        else:
                            st.error(
                                f"No se pudo actualizar los campos de la persona con ID {selected_person_id}."
                            )
                    elif nuevo_email and not nuevo_nombre:
                        update_response = actualizar_campos(
                            selected_person_id, nuevo_nombre, nuevo_email
                        )
                        if update_response.status_code == 200:
                            st.success(
                                f"Los campos de la persona con ID {selected_person_id} se actualizaron correctamente."
                            )
                        else:
                            st.error(
                                f"No se pudo actualizar los campos de la persona con ID {selected_person_id}."
                            )
            else:
                st.error("No se pudieron obtener los datos de personas desde la API.")

        elif operacion_persona == "Borrar":
            st.subheader("Borrar")
            datos = obtener_datos("persons")
            if datos:
                personas = {
                    persona["id"]: f"{persona['name']} - {persona['email']}"
                    for persona in datos
                }
                selected_person_id = st.selectbox(
                    "Seleccione una persona para borrar",
                    list(personas.keys()),
                    format_func=lambda id: personas[id],
                )
                if st.button("Borrar"):
                    delete_response = delete_data(selected_person_id, "persons")
                    if delete_response.status_code == 200:
                        st.success(
                            f"Registro con ID {selected_person_id} eliminado correctamente"
                        )
                    else:
                        st.error(
                            f"No se pudo eliminar el registro con ID {selected_person_id}"
                        )

    if seleccion == "Policias":
        st.subheader("Gestión de Policias")
        policia = st.selectbox("Elija una operación para Policias", operaciones_oficial)
        if policia == "Crear":
            st.subheader("crear")
            name = st.text_input("Ingrese nombre completo")
            badge_number = st.text_input("Ingrese numero de placa")
            if st.button("crear"):
                response = create_data(
                    {"name": name, "badge_number": badge_number}, "officers"
                )
                # 
                st.success(f"Item created successfully!{response}")
        elif policia == "Mostrar":
            st.subheader("officers")
            datos = obtener_datos("officers")
            if datos:
                df = datos_ordenados_id(datos)
                st.write("Datos obtenidos:")
                # 
                st.table(df)

        elif policia == "Actualizar":
            st.subheader("Actualizar")
            datos = obtener_datos("officers")

            if datos:
                dict_officer = {
                    officer["id"]: f"{officer['name']} - {officer['badge_number']}"
                    for officer in datos
                }

                selected_officer_id = st.selectbox(
                    "Seleccione un policia para actualizar:",
                    list(dict_officer.keys()),
                    format_func=lambda id: dict_officer[id],
                )
                officer_seleccionada = next(
                    officer for officer in datos if officer["id"] == selected_officer_id
                )
                # 
                st.write(f"Nombre actual: {officer_seleccionada['name']}")
                st.write(f"Placa actual: {officer_seleccionada['badge_number']}")
                nuevo_nombre = st.text_input("Nuevo nombre (opcional):")
                nuevo_badge_number = st.text_input("Nuevo badge_number (opcional):")
                if st.button("Actualizar"):
                    if not nuevo_nombre and not nuevo_badge_number:
                        st.warning(
                            "Por favor, ingrese al menos un campo para actualizar."
                        )
                    elif nuevo_nombre and not nuevo_badge_number:
                        update_response = actualizar_campos_officer(
                            selected_officer_id, nuevo_nombre, nuevo_badge_number
                        )
                        if update_response.status_code == 200:
                            st.success(
                                f"Los campos del policia con ID {selected_officer_id} se actualizaron correctamente."
                            )
                        else:
                            st.error(
                                f"No se pudo actualizar los campos del policia con ID {selected_officer_id}."
                            )
                    elif nuevo_badge_number and not nuevo_nombre:
                        update_response = actualizar_campos_officer(
                            selected_officer_id, nuevo_nombre, nuevo_badge_number
                        )
                        if update_response.status_code == 200:
                            st.success(
                                f"Los campos del policia con ID {selected_officer_id} se actualizaron correctamente."
                            )
                        else:
                            st.error(
                                f"No se pudo actualizar los campos del policia con ID {selected_officer_id}."
                            )
            else:
                st.error("No se pudieron obtener los datos del poilicia desde la API.")

        elif policia == "Borrar":
            st.subheader("Borrar")
            datos = obtener_datos("officers")
            if datos:
                oficiales = {
                    oficial["id"]: f"{oficial['name']} - {oficial['badge_number']}"
                    for oficial in datos
                }
                selected_person_id = st.selectbox(
                    "Seleccione un policia para borrar",
                    list(oficiales.keys()),
                    format_func=lambda id: oficiales[id],
                )
                if st.button("Borrar"):
                    delete_response = delete_data(selected_person_id, "officers")
                    if delete_response.status_code == 200:
                        st.success(
                            f"Registro con ID {selected_person_id} eliminado correctamente"
                        )
                    else:
                        st.error(
                            f"No se pudo eliminar el registro con ID {selected_person_id}"
                        )
    ########################## patentes ###########################
    if seleccion == "Patentes":
        st.subheader("Gestión de patentes")
        patente = st.selectbox("Elija una operación para Patentes", operaciones_oficial)
        if patente == "Crear":
            st.subheader("crear")
            license_plate = st.text_input("Ingrese patente")
            brand = st.text_input("Ingrese marca")
            color = st.text_input("Ingrese color")
            owner_name = st.text_input("Ingrese nombre del dueño")

            if st.button("crear"):
                response = create_data(
                    {
                        "license_plate": license_plate,
                        "brand": brand,
                        "color": color,
                        "owner_name": owner_name,
                    },
                    "vehicles",
                )
                # 
                st.success(f"Item created successfully!{response}")
        elif patente == "Mostrar":
            st.subheader("vehicles")
            datos = obtener_datos("vehicles")
            if datos:
                df = datos_ordenados_id(datos)
                st.write("Datos obtenidos:")
                # 
                st.table(df)

        elif patente == "Actualizar":
            st.subheader("Actualizar")
            datos = obtener_datos("vehicles")

            if datos:
                vehicles = {
                    vehicl["id"]: f"{vehicl['license_plate']} - {vehicl['owner_name']}"
                    for vehicl in datos
                }

                selected_patente_id = st.selectbox(
                    "Seleccione un patente para actualizar:",
                    list(vehicles.keys()),
                    format_func=lambda id: vehicles[id],
                )
                officer_seleccionada = next(
                    officer for officer in datos if officer["id"] == selected_patente_id
                )
                # 
                st.write(f"Placa actual: {officer_seleccionada['license_plate']}")
                st.write(
                    f"Nombre de dueño actual: {officer_seleccionada['owner_name']}"
                )
                st.write(f"Marca actual: {officer_seleccionada['brand']}")
                st.write(f"Color actual: {officer_seleccionada['color']}")

                nuevo_patente = st.text_input("Nueva patente (opcional):")
                nuevo_owner_name = st.text_input("Nuevo nombre de dueño (opcional):")
                nuevo_brand = st.text_input("Nueva marca (opcional):")
                nuevo_color = st.text_input("Nuevo color (opcional):")
                if st.button("Actualizar"):
                    if (
                        not nuevo_patente
                        and not nuevo_owner_name
                        and not nuevo_brand
                        and not nuevo_color
                    ):
                        st.warning(
                            "Por favor, ingrese al menos un campo para actualizar."
                        )
                    else:
                        update_response = actualizar_campos_actualizados(
                            selected_patente_id,
                            nuevo_patente,
                            nuevo_owner_name,
                            nuevo_brand,
                            nuevo_color,
                        )

                        if update_response.status_code == 200:
                            st.success(
                                f"Los campos del patente con ID {selected_patente_id} se actualizaron correctamente."
                            )
                        else:
                            st.error(
                                f"No se pudo actualizar los campos del patente con ID {selected_patente_id}."
                            )
            else:
                st.error("No se pudieron obtener los datos del poilicia desde la API.")

        elif patente == "Borrar":
            st.subheader("Borrar")
            datos = obtener_datos("vehicles")
            if datos:
                vehicles = {
                    vehicl["id"]: f"{vehicl['license_plate']} - {vehicl['owner_name']}"
                    for vehicl in datos
                }
                selected_patente_id = st.selectbox(
                    "Seleccione un patente para borrar",
                    list(vehicles.keys()),
                    format_func=lambda id: vehicles[id],
                )
                if st.button("Borrar"):
                    delete_response = delete_data(selected_patente_id, "vehicles")
                    if delete_response.status_code == 200:
                        st.success(
                            f"Registro con ID {selected_patente_id} eliminado correctamente"
                        )
                    else:
                        st.error(
                            f"No se pudo eliminar el registro con ID {selected_patente_id}"
                        )


if __name__ == "__main__":
    main()
