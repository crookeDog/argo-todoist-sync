from argofamiglia import ArgoFamiglia 
import datetime
import time
from password import ARGO_SCHOOL_CODE, ARGO_PASS, ARGO_USER, API
from todoist_api_python.api import TodoistAPI
def get_description_task():
    tasks = API.get_tasks()
    description_tasks = []
    for task in tasks:
        for ts in task:
            if ts.description:
                description_tasks.append(ts.description)
    return description_tasks
def get_compiti(tasks):
    try:
        log = ArgoFamiglia(ARGO_SCHOOL_CODE, ARGO_USER, ARGO_PASS)
        compiti = log.getCompitiByDate()
        keys = list(compiti.keys())
        
        oggi = datetime.date.today().isoformat()
        giorni_futuri = [data_compito for data_compito in keys if data_compito >= oggi]

        if not giorni_futuri:
            return

        for day in giorni_futuri:
            diz = compiti[day]
            
            materia = ", ".join(diz['materie']) if isinstance(diz['materie'], list) else str(diz['materie'])
            compiti_assegnati = ", ".join(diz['compiti']) if isinstance(diz['compiti'], list) else str(diz['compiti'])

            if not check_task(compiti_assegnati, tasks):
                set_task(materia, compiti_assegnati, day)
                
    except Exception as e:
        print(f"Error: {e}")

def check_task(compiti, tasks):
    try:
        for descrizione in tasks:  
            if compiti in descrizione or descrizione in compiti:
                
                return True
                
        return False
    except Exception as e:
        print(f"Errore nel controllo dei task: {e}")
        return True

def set_task(materia, compiti, scadenza):
    try:
        scadenza_date = datetime.date.fromisoformat(scadenza)
        
        task = API.add_task(
            content=materia,
            description=compiti,
            due_date=scadenza_date
        )
    except Exception as e:
        print(f"Errore durante la creazione del task: {e}")

get_compiti(get_description_task())
def main():
    while True:
        description = get_description_task()
        get_compiti(description)
        time.sleep(1800)
