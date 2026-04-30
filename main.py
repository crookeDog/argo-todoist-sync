"""from argofamiglia import ArgoFamiglia 
import datetime
from password import ARGO_SCHOOL_CODE,ARGO_PASS,ARGO_USER,API
from todoist_api_python.api import TodoistAPI

def get_compiti(giorno):
    
    try:
        tasks = API.get_tasks()
        log = ArgoFamiglia(ARGO_SCHOOL_CODE,ARGO_USER,ARGO_PASS)
        compiti = log.getCompitiByDate()
        keys = list(compiti.keys())
        if giorno in keys:
            key = keys.index(giorno)
            
            for k in keys[key:]:
                diz = compiti[k]
                materia = (str(diz['materie']).strip("['")).strip("']")
                compiti_assegnati = (str(diz['compiti']).strip("['")).strip("']")

                if check_task(compiti_assegnati,tasks) == True:
                    set_task(materia,compiti_assegnati,k)
        else:
            print("giorno non presente")
    except Exception as e:
        print(f"Error:{e}")
def check_task(compiti,task_esistenti):
    try:
        for task in task_esistenti:
            for el in task:
                if el.description == compiti:
                    return False 
                
        return True
            
    except Exception as e:
        print(f"Errore nel controllo dei task: {e}")
        return False
def set_task(materia,compiti,scadenza):
    task = API.add_task(
        content=materia,
        description=compiti,
        due_date=scadenza
    )
    print(f"task creata con id: {task.id}")

"""
from argofamiglia import ArgoFamiglia 
from datetime import date
from password import ARGO_SCHOOL_CODE, ARGO_PASS, ARGO_USER, API
from todoist_api_python.api import TodoistAPI

def sincronizza_compiti():
    try:
        # 1. Scarichiamo i task ESISTENTI (una volta sola)
        print("Recupero i task da Todoist...")
        tasks_esistenti = API.get_tasks()

        # 2. Login ad Argo (una volta sola)
        print("Accesso ad ArgoFamiglia in corso...")
        log = ArgoFamiglia(ARGO_SCHOOL_CODE, ARGO_USER, ARGO_PASS)
        
        # 3. Otteniamo TUTTI i compiti
        compiti = log.getCompitiByDate()
        keys = list(compiti.keys())
        
        # 4. Otteniamo la data di OGGI in formato stringa testuale (es. "2024-05-20")
        oggi_stringa = date.today().isoformat()
        
        # 5. Filtriamo le date di Argo: prendiamo solo oggi e i giorni futuri
        # Invece di un ciclo da 100, prendiamo direttamente tutti i giorni utili che Argo ci dà
        giorni_futuri = [giorno for giorno in keys if giorno >= oggi_stringa]
        
        if not giorni_futuri:
            print("Nessun compito futuro trovato su Argo.")
            return

        # 6. Processiamo i compiti per tutti i giorni futuri trovati
        for giorno in giorni_futuri:
            diz = compiti[giorno]
            
            # Pulizia sicura delle stringhe
            materia = ", ".join(diz['materie']) if isinstance(diz['materie'], list) else str(diz['materie'])
            compiti_assegnati = ", ".join(diz['compiti']) if isinstance(diz['compiti'], list) else str(diz['compiti'])

            # Controllo e creazione
            if check_task(compiti_assegnati, tasks_esistenti) == True:
                set_task(materia, compiti_assegnati, giorno)
                
    except Exception as e:
        print(f"Errore Generale: {e}")

def check_task(compiti, task_esistenti):
    try:
        for task in task_esistenti:
            if task.description == compiti:
                return False # Il task esiste già
        return True # Il task NON esiste, creiamolo
            
    except Exception as e:
        print(f"Errore nel controllo dei task: {e}")
        return False

def set_task(materia, compiti, scadenza_stringa):
    try:
        # Convertiamo la stringa di Argo in una vera e propria Data per Todoist
        scadenza_date = date.fromisoformat(scadenza_stringa)
        
        task = API.add_task(
            content=materia,
            description=compiti,
            due_date=scadenza_date
        )
        print(f"Nuovo task creato: [{materia}] per il {scadenza_stringa} (ID: {task.id})")
    except Exception as e:
        print(f"Errore creazione task per {materia}: {e}")

# ESECUZIONE:
# Basta chiamare questa funzione UNA sola volta. 
# Farà tutto da sola da oggi in poi!
sincronizza_compiti()

