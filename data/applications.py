applications = []

def add_application(name, phone, comment):
    applications.append({
        "name": name,
        "phone": phone,
        "comment": comment
    })

def get_applications():
    return applications
