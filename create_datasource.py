import json

import requests
import yaml
from grafanalib._gen import DashboardEncoder
from grafanalib.core import Dashboard

from panels import dashboard_panels

GRAFANA_TOKEN = "eyJrIjoiRG1WMldUODJyWmExbk1XZTdXUTVvak1tYVFkcnJ3Y3EiLCJuIjoiYXMtY29kZSIsImlkIjoxfQ=="
GRAFANA_DATASOURCE_URL = "http://localhost:3000/api/datasources"
GRAFANA_DASHBOARD_URL = "http://localhost:3000/api/dashboards"
# with open('config.yml') as file:
#     grafana_config = yaml.load(file, Loader=yaml.FullLoader)
#     for index, source in enumerate(grafana_config["datasources"]):
#         resp = requests.post(url=GRAFANA_URL,
#                              json={
#                                  "name": f"simplejson_test_{index}",
#                                  "type": "grafana-simple-json-datasource",
#                                  "url": "http://mydatasource.com",
#                                  "access": "proxy",
#                                  "basicAuth": True,
#                                  "basicAuthUser": "basicuser"
#                              },
#                              headers={
#                                  'Authorization': f'Bearer {GRAFANA_TOKEN}',
#                                  'Content-Type': 'application/json',
#                                  'Accept': 'application/json'
#                              })

import grafanalib


def build_dashboards_from_config(yaml_filename):
    with open(yaml_filename) as file:
        grafana_config = yaml.load(file, Loader=yaml.FullLoader)
        dashboards = grafana_config['dashboards']
        for dashboard in dashboards:
            dash = Dashboard(title=dashboard)
            dash.description = dashboards[dashboard]['description']
            dash.panels = dashboard_panels[dashboard]
            upload_dashboard_to_grafana(get_dashboard_json(dash.auto_panel_ids(), overwrite=True), GRAFANA_TOKEN)


def upload_dashboard_to_grafana(dashboard_json, api_key, verify=True):
    """
    upload_to_grafana tries to upload dashboard to grafana and prints response

    :param verify:
    :param dashboard_json - dashboard json generated by grafanalib
    :param api_key - grafana api key with read and write privileges
    """

    headers = {'Authorization': f"Bearer {api_key}", 'Content-Type': 'application/json'}
    r = requests.post(f"{GRAFANA_DASHBOARD_URL}/db", data=dashboard_json, headers=headers, verify=verify)
    # TODO: add error handling
    print(f"{r.status_code} - {r.content}")


def get_dashboard_json(dashboard, overwrite=False, message="Updated by grafanlib"):
    """
    get_dashboard_json generates JSON from grafanalib Dashboard object

    :param message:
    :param overwrite:
    :param dashboard - Dashboard() created via grafanalib
    """

    # grafanalib generates json which need to pack to "dashboard" root element
    return json.dumps(
        {
            "dashboard": dashboard.to_json_data(),
            "overwrite": overwrite,
            "message": message
        }, sort_keys=True, indent=2, cls=DashboardEncoder)


build_dashboards_from_config('config.yml')
