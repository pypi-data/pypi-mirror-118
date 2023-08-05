application = None
distributive = None
telemetry = None


def get_application():
    global application
    return application


def set_application(application_new):
    global application
    application = application_new


def get_distributive():
    global distributive
    return distributive


def set_distributive(distributive_new):
    global distributive
    distributive = distributive_new


def get_telemetry():
    global telemetry
    return telemetry


def set_telemetry(telemetry_new):
    global telemetry
    telemetry = telemetry_new
