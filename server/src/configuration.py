import os

import gumo
import gumo.core._configuration
from gumo import datastore

def app_configure():
    gumo.core._configuration.configure_once(
        google_cloud_project=os.environ.get('PROJECT_NAME'),
        google_cloud_location=os.environ.get('PROJECT_LOCATION'),
    )

    datastore.configure_once(
        use_local_emulator='DATASTORE_EMULATOR_HOST' in os.environ,
        emulator_host=os.environ.get('DATASTORE_EMULATOR_HOST'),
        namespace=os.environ.get('DATASTORE_NAMESPACE'),
    )