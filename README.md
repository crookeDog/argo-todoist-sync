# 📚 Argo Todoist Sync

This Python script automates your school organization by syncing homework assignments from the **Argo Didup (Famiglia)** electronic register directly to your **Todoist** task manager.

## 🚀 Features
* **Automatic Connection:** Securely connects to the Argo Famiglia API.
* **Smart Scanning:** Scans for homework assigned over the next **6 days**.
* **Todoist Integration:** Creates tasks automatically with:
    * **Title:** School subject name.
    * **Description:** Full homework details/instructions.
    * **Priority:** Sets priority for immediate visibility.

## 🛠️ Prerequisites

Ensure you have Python installed. You will need the following libraries:

* `argofamiglia` (Unofficial Argo API wrapper)
* `todoist-api-python` (Official Todoist API client)

Install them via pip:

```bash
pip install argofamiglia todoist-api-python
