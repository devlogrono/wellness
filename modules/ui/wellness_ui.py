import time
import streamlit as st
from modules.db.db_records import search_existing_record, upsert_record_db
from modules.schema import new_base_record
from modules.ui.check_in_ui import checkin_form
from modules.ui.check_out_ui import checkout_form
from modules.i18n.i18n import t
from modules.ui.ui_components import preview_record

def wellness_form(jugadora, tipo, turno):
    """
    Lógica completa y segura para crear, validar y guardar Wellness/RPE.
    Versión corregida para evitar reruns globales y conflictos entre usuarios.
    """

    # ---------------------------------------
    # 1. Validación inicial
    # ---------------------------------------
    if not jugadora:
        st.info(t("Selecciona una jugadora para continuar."))
        return
    
   
    # ---------------------------------------
    # 2. Crear record base
    # ---------------------------------------
    record = new_base_record(
        id_jugadora=str(jugadora["id_jugadora"]),
        username=st.session_state["auth"]["name"].lower(),
        tipo="checkin" if tipo == "Check-in" else "checkout",
    )
    #preview_record(record)
    record["turno"] = turno or ""

    # ID seguro por navegador
    session_id = st.session_state["client_session_id"]
    redirect_key = f"redirect_{session_id}"

    # ---------------------------------------
    # ---------------------------------------
    form_key = f"form_wellness_{session_id}"

    #with st.form(key=form_key, border=False):

    # ---- Check-in ----
    if tipo == "Check-in":
        record, is_valid, validation_msg = checkin_form(record, jugadora["genero"])

    # ---- Check-out ----
    else:
        record, is_valid, validation_msg = checkout_form(record)

        # ---- Botón seguro ----
        #submitted = st.form_submit_button(t("Guardar"))


    # ===============================
    # 🔸 Diálogo de confirmación de registro
    # ===============================
    @st.dialog(t("Confirmar registro"), width="small")
    def dialog_confirmar_registro(record, jugadora, tipo):
        nombre = jugadora["nombre_jugadora"]
        modo = t("Check-in") if tipo == "Check-in" else t("Check-out")

        st.warning(
            f"{t('¿Desea confirmar el registro de')} **{modo}** "
            f"{t('para la jugadora')} **{nombre}**?"
        )

        _, col2, col3 = st.columns([1.6, 1, 1])

        with col2:
            if st.button(t(":material/cancel: Cancelar")):
                st.rerun()

        with col3:
            if st.button(t(":material/check: Confirmar"), type="primary"):
                modo_db = "checkin" if tipo == "Check-in" else "checkout"
                success = upsert_record_db(record, modo_db)

                if success:
                    st.session_state["submitted"] = True
                    st.session_state[f"redirect_{st.session_state['client_session_id']}"] = True
                else:
                    st.session_state["save_error"] = True

                st.rerun()

    # ---------------------------------------
    # 5. Procesamiento del guardado
    # ---------------------------------------
    #st.dataframe(jugadora)
    if st.button(f":material/save: {t('Guardar')}", key="btn_reg_wellness", disabled=not is_valid):
        dialog_confirmar_registro(record, jugadora, tipo)
        #preview_record(record)

        # ---------------------------------------
        # 3. Revisar si ya existe Check-in hoy
        # ---------------------------------------
        # existing_today = search_existing_record(record)
        # if existing_today:
        #     st.error(t("Existe un registro de check-in previo para esta jugadora, fecha y turno."))
        #     st.stop()
        
        # if not existing_today:
        #     st.error(t("No existe un registro de check-in previo para esta jugadora, fecha y turno."))
        #     st.stop()

        # # Validación previa
        # if not is_valid and validation_msg:
        #     st.error(validation_msg)
        #     return

        # modo = "checkin" if tipo == "Check-in" else "checkout"
        # success = upsert_record_db(record, modo)

        # if success:
        #     st.success(t("Registro guardado correctamente."))
        #     time.sleep(2)  # Pequeña pausa para mejor UX
        #     st.session_state[redirect_key] = True
        #     st.session_state["submitted"] = True
        # else:
        #     st.error(t("Error al guardar el registro."))
        #     return

    # ---------------------------------------
    # 6. Vista de previsualización (solo developers)
    # ---------------------------------------
    if st.session_state["auth"]["rol"].lower() == "developer":
        st.divider()
        if st.checkbox(t("Previsualización")):
            preview_record(record)

    if st.session_state.pop("save_error", False):
        st.error(t("Error al guardar el registro."))

    if st.session_state.get("submitted"):
        st.success(t("Registro guardado correctamente."))

    # ---------------------------------------
    # 7. Redirección segura SOLO para este navegador
    # ---------------------------------------
    if st.session_state.get(redirect_key):
        del st.session_state[redirect_key]
        st.session_state["target_page"] = "registro"
        #time.sleep(5)  # Pequeña pausa para evitar conflictos
        st.switch_page("pages/switch.py")
        #st.rerun()

def resolver_jugadora_final(jugadora_header, jug_df_filtrado, jug_df, tipo):

    # Si no hay NINGUNA jugadora disponible → fin
    if jug_df_filtrado.empty:
        st.session_state["last_selected_player_id"] = None
        st.error(f"No hay más jugadoras disponibles para registrar {tipo}")
        st.stop()

    # ID actual entregado por el header
    new_id = str(jugadora_header["id_jugadora"]) if jugadora_header else None

    # IDs válidos en el filtrado actual
    current_ids = jug_df_filtrado["id_jugadora"].astype(str).tolist()

    # ID bloqueado previamente
    prev_id = st.session_state.get("last_selected_player_id")

    # ------------------------------
    # 1. Primera asignación
    # ------------------------------
    if prev_id is None:
        if new_id is not None:
            st.session_state["last_selected_player_id"] = new_id
        else:
            # Si no había selección, tomamos la PRIMERA jugadora disponible
            st.session_state["last_selected_player_id"] = current_ids[0]

    else:
        # ------------------------------
        # 2. Si cambia la jugadora del header
        # ------------------------------
        if new_id != prev_id:

            # Si la jugadora anterior ya no existe → reset a la primera disponible
            if prev_id not in current_ids:
                st.session_state["last_selected_player_id"] = current_ids[0]
                st.warning("La jugadora seleccionada ya no se encontraba disponible.")
                st.rerun()

            # Cambio manual → actualizar bloqueada
            st.session_state["last_selected_player_id"] = new_id

    # ------------------------------
    # 3. Jugadora final bloqueada
    # ------------------------------
    locked_id = st.session_state.get("last_selected_player_id")

    if locked_id is None:
        st.error("Error interno: No se pudo resolver la jugadora seleccionada.")
        st.stop()

    # Buscar jugadora final exacta
    jugadora_rows = jug_df[jug_df["id_jugadora"].astype(str) == locked_id]

    if jugadora_rows.empty:
        st.session_state["last_selected_player_id"] = None
        st.error("La jugadora seleccionada ya no se encuentra disponible.")
        st.stop()

    # Devolver jugadora final
    return jugadora_rows.iloc[0].to_dict()

