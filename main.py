import flet as ft
from alert import AlertManager
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    # TODO

    input_marca = ft.TextField(label = "marca")
    input_modello = ft.TextField(label = "modello")
    input_anno = ft.TextField(label = "anno")
    input_contatore_posti = ft.TextField(value=str(0), width=50)



    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    # TODO
    def incrementaposti(e):
        input_contatore_posti.value = str(int(input_contatore_posti.value) + 1)
        page.update()
    def decrementaposti(e):
        input_contatore_posti.value = str(int(input_contatore_posti.value) - 1)
        page.update()
    def inseriscidati(e):
        #POTREBBE ESSERE UNA SOLUZIONE MA ANDREBBE GESTITO MEGLIO L'OUTPUT DELL'ERRORE
        #try:
        #    autonoleggio.aggiungi_automobile(input_marca.value, input_modello.value, input_anno.value, input_contatore_posti.value)
        #    aggiorna_lista_auto()
        #   page.update()
        #except Exception as e:
        #    alert.show_alert(f"❌ {e}")

        if input_marca.value.isalpha() and input_modello.value.isalpha() and input_anno.value.isdigit() and input_contatore_posti.value.isdigit() and int(input_contatore_posti.value) > 1:
            autonoleggio.aggiungi_automobile(input_marca.value, input_modello.value, input_anno.value, input_contatore_posti.value)
            aggiorna_lista_auto()
            input_marca.value = ""
            input_modello.value = ""
            input_anno.value = ""
            input_contatore_posti.value = str(0)
            page.update()
        else:
            if not input_marca.value.isalpha():
                alert.show_alert("Descrizione dell'errore: valore non valido per la marca")
            elif not input_modello.value.isalpha():
                alert.show_alert("Descrizione dell'errore: valore non valido per il modello")
            elif not input_anno.value.isdigit():
                alert.show_alert("Descrizione dell'errore: valore non valido per l'anno")
            elif not input_contatore_posti.value.isdigit():
                alert.show_alert("Descrizione dell'errore: valore non valido per il numero di posti")
            elif not int(input_contatore_posti.value) > 1:
                alert.show_alert("Descrizione dell'errore: valore non valido per il numero di posti")

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto
    # TODO
    bottone_aggiunta = ft.ElevatedButton(text="Aggiungi automobile", on_click=inseriscidati)
    bottone_incrementa_posti = ft.ElevatedButton(text="+", on_click=incrementaposti)
    bottone_decrementa_posti = ft.ElevatedButton(text="-", on_click=decrementaposti)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO
        ft.Text("Aggiungi nuova automobile", size=20),
        ft.Row(spacing = 20,
               controls=[input_marca, input_modello, input_anno, bottone_decrementa_posti, input_contatore_posti,bottone_incrementa_posti],
               alignment = ft.MainAxisAlignment.CENTER),
        bottone_aggiunta,

        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)