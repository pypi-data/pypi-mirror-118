from json.decoder import JSONDecodeError
from typing import IO
import requests
import json
import os
import logging
import sys

from requests.api import request
from requests.models import encode_multipart_formdata, requote_uri

# from requests.api import get
# sys.path.insert(0, 'Deliveries')
# from Deliveries.deliveries import *
# import Deliveries.deliveries
#### These functions are to ensure that the core/critical SDK features are working, eventually these funtions will be formatted/reorganized

# This handler is currently under testing much like many of the endpoints: CAUTION ADVISED FOR USAGE
def response_handler(response):
    code = response.status_code
    try:
        json.loads(response.content)
    except JSONDecodeError as e:
        # print("Error: Invalid Request")
        raise RuntimeError("Failed to send Invalid Request") from e

    if code < 200 or code >= 300:
        error_message = json.loads(response.content)
        error_message = error_message["message"]
        # print(f"Error {code}: {error_message}")
        raise Exception(f"Error {code}: {error_message}")
    return 0


# This class as of the current, keeps track of the baseURL and eventually the API token - once they login
# class IonChannel(Deliv):
#     def __init__(self, baseURL):
#         self.baseURL = baseURL
#         self.token = None

class IonChannel():
    def __init__(self, baseURL):
        self.baseURL = baseURL
        self.token = None

# This function will create a new client object so that the user can interact with the API
def new_client(baseURL):
    client = IonChannel(baseURL)
    return client


# This function will allow the user to login
def login(self, username=None, password=None):
    try:
        token = os.environ["IONTOKEN"]

    except KeyError:
        if username is None:
            try:
                username = os.environ["IONUSER"]
            except KeyError as e:
                # username = input(
                #     "Since you have not set ENV variable (IONUSER): What is your username: "
                # )
                raise KeyError("You have not set ENV variable (IONUSER)") from e
        if password is None:
            try:
                password = os.environ["IONPASSWORD"]
            except KeyError as e:
                # password = input(
                #     "Since you have not set ENV variable (IONPASSWORD): What is your password: "
                # )
                raise KeyError("You have not set ENV variable (IONPASSWORD)") from e

        endpoint = "sessions/login"
        URL = self.baseURL + endpoint
        logging.debug(f"Http Destination: {URL}")
        r = requests.post(URL, json={"username": username, "password": password})
        logging.debug(f"Request Type: {r.request}")
        logging.debug(f"Status Code: {r.status_code}")
        check = response_handler(r)
        # if check is not None:
        #    return -1
        if check != 0:
            return -1

        try:
            token = r.json()["data"]["jwt"]
        except KeyError as e:
            # print("login Error: Invalid authentication credentials - An account doesn't exist with this username or password")

            raise RuntimeError(
                "Invalid authentication credentials - An account doesn't exist with this username or password"
            ) from e

            # return -1

    self.token = token
    # return token
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.login = login

# This function will list all the teams
def get_teams(self):
    endpoint = "teams/getTeams"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1

    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_teams = get_teams

# This endpoint allows a list of projects to be viewed by a user
def get_projects(self, teamid):
    endpoint = "project/getProjects"
    URL = self.baseURL + endpoint
    head = {"Authorization": "Bearer " + self.token}
    ids = {"team_id": teamid}

    r = requests.get(URL, headers=head, params=ids)

    check = response_handler(r)
    if check != 0:
        return -1

    json_data = json.loads(r.content)
    meta_data = json_data["meta"]

    total_count = meta_data["total_count"]
    updated_req = {"team_id": teamid, "limit": total_count}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=updated_req)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    dictionary_data = json.loads(r.content)
    return dictionary_data
    # content = json_data["data"]
    # print(content)
    # for i in content:
    #     print(f'{i["name"]} and id: {i["id"]} \n')


IonChannel.get_projects = get_projects

# This endpoint allows an analysis to be run on a selected project
def analyze_project(self, teamid, projectid, branch=None):
    endpoint = "scanner/analyzeProject"
    head = {"Authorization": "Bearer " + self.token}
    if branch != 0:
        json_data = json.dumps(
            {"team_id": teamid, "project_id": projectid, "branch": branch}
        )
    else:
        json_data = json.dumps({"team_id": teamid, "project_id": projectid})
    URL = self.baseURL + endpoint
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1

    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.analyze_project = analyze_project

# This endpoint will return the status of an analysis
def analysis_status(self, teamid, projectid, analysisid):
    endpoint = "scanner/getAnalysisStatus"
    head = {"Authorization": "Bearer " + self.token}
    parameters = {"team_id": teamid, "project_id": projectid, "id": analysisid}
    URL = self.baseURL + endpoint
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1

    json_data = json.loads(r.content)
    return json_data
    # return r.content


IonChannel.analysis_status = analysis_status

# This endpoint will return analysis data
def get_analysis(self, teamid, projectid, analysisid):
    endpoint = "animal/getAnalysis"
    head = {"Authorization": "Bearer " + self.token}
    parameters = {"team_id": teamid, "project_id": projectid, "id": analysisid}
    URL = self.baseURL + endpoint
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1

    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_analysis = get_analysis

# This endpoint will return raw analysis data
def get_raw_analysis(self, teamid, projectid, analysisid):
    endpoint = "animal/getAnalysis"
    head = {"Authorization": "Bearer " + self.token}
    parameters = {"team_id": teamid, "project_id": projectid, "id": analysisid}
    URL = self.baseURL + endpoint
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1

    return r.content


IonChannel.get_raw_analysis = get_raw_analysis


# This endpoint will get the data about an applied ruleset
def get_applied_ruleset(self, teamid, projectid, analysisid):
    endpoint = "ruleset/getAppliedRulesetForProject"
    head = {"Authorization": "Bearer " + self.token}
    parameters = {"team_id": teamid, "project_id": projectid, "analysis_id": analysisid}
    URL = self.baseURL + endpoint
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1

    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_applied_ruleset = get_applied_ruleset


# This endpoint will return raw data about an applied ruleset
def get_raw_applied_ruleset(self, teamid, projectid, analysisid):
    endpoint = "ruleset/getAppliedRulesetForProject"
    head = {"Authorization": "Bearer " + self.token}
    parameters = {"team_id": teamid, "project_id": projectid, "analysis_id": analysisid}
    URL = self.baseURL + endpoint
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1

    return r.content


IonChannel.get_raw_applied_ruleset = get_raw_applied_ruleset


# This endpoint will get information regarding a specific ruleset
def get_ruleset(self, teamid, rulesetid):
    endpoint = "ruleset/getRuleset"
    head = {"Authorization": "Bearer " + self.token}
    parameters = {"team_id": teamid, "id": rulesetid}
    URL = self.baseURL + endpoint
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1

    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_ruleset = get_ruleset


# This endpoint will create a project object
def create_project(self, teamid, project):
    endpoint = "project/createProject"
    head = {"Authorization": "Bearer " + self.token}
    project["team_id"] = teamid

    json_data = json.dumps(project)
    URL = self.baseURL + endpoint
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.create_project = create_project

# This endpoint will update a project and its contents based on the values within the JSON project parameter,
# also handles the nauture of the project - whether it should be archived or not, add "active" setting (boolean) to JSON
# object as either True or False depending on whether the project needs to be archived or not
def update_project(self, teamid, project):
    endpoint = "project/updateProject"
    head = {"Authorization": "Bearer " + self.token}
    project["team_id"] = teamid

    json_data = json.dumps(project)
    URL = self.baseURL + endpoint
    logging.debug(f"Http Destination: {URL}")
    r = requests.put(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1

    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.update_project = update_project

# This endpoint will add a scan result to an analysis
def add_scan(self, analysisid, teamid, projectid, param_value, scan="coverage"):
    endpoint = "scanner/addScanResult"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps(
        {
            "team_id": teamid,
            "project_id": projectid,
            "analysis_id": analysisid,
            "scan_type": scan,
            "status": "accepted",
            "results": {"value": param_value},
        }
    )
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1

    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.add_scan = add_scan

# This endpoint will export an SBOM report
def get_SBOM(self, id_set, team_id, options):
    sbom_type = options["sbom_type"]
    include_dependencies = options["include_dependencies"]

    endpoint = (
        "report/getSBOM?sbom_type="
        + str(sbom_type)
        + "&include_dependencies="
        + str(include_dependencies)
    )
    head = {"Authorization": "Bearer " + self.token}
    json_data = json.dumps({"team_id": team_id, "ids": id_set})

    URL = self.baseURL + endpoint
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_SBOM = get_SBOM

# This endpoint will result a series of analyses run on a project
def get_analyses(self, teamid, projectid):
    endpoint = "animal/getAnalyses"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"team_id": teamid, "project_id": projectid}

    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_analyses = get_analyses

# This endpoint will result a series of raw analyses data run on a project
def get_raw_analyses(self, teamid, projectid):
    endpoint = "animal/getAnalyses"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"team_id": teamid, "project_id": projectid}

    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    return r.content


IonChannel.get_raw_analyses = get_raw_analyses


# This endpoint will return the results of the latest run analysis
def get_latest_analysis(self, teamid, projectid):
    endpoint = "animal/getLatestAnalysis"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"team_id": teamid, "project_id": projectid}

    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_latest_analysis = get_latest_analysis


def get_latest_public_analysis(self, projectid, branch):
    endpoint = "animal/getLatestPublicAnalysisSummary"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"project_id": projectid, "branch": branch}

    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    # logging.debug(f"Request Type: {r.request}")
    # logging.debug(f"Status Code: {r.status_code}")
    # check = response_handler(r)
    # if check != 0:
    #     return -1
    # dictionary_data = json.loads(r.content)
    # return dictionary_data
    return r.content


IonChannel.get_latest_public_analysis = get_latest_public_analysis


# This endpoint will return the latest analysis IDs for a project
# projectids must be passed through as an array of strings
def get_latest_ids(self, teamid, projectids):
    endpoint = "animal/getLatestAnalysisIDs"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps({"team_id": teamid, "IDs": projectids})

    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_latest_ids = get_latest_ids

# This endpoint will return the summary for the latest analysis run on a project
def get_latest_analysis_summary(self, teamid, projectid):
    endpoint = "animal/getLatestAnalysisSummary"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"team_id": teamid, "project_id": projectid}

    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_latest_analysis_summary = get_latest_analysis_summary

# This endpoint will return raw summary data for the latest analysis run on a project
def get_raw_latest_analysis_summary(self, teamid, projectid):
    endpoint = "animal/getLatestAnalysisSummary"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"team_id": teamid, "project_id": projectid}

    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    return r.content


IonChannel.get_raw_latest_analysis_summary = get_raw_latest_analysis_summary

# This endpoint will return a series of summaries for an analysis run on a project
# projectids must be passed through as an array of strings
def get_latest_analysis_summaries(self, teamid, projectids):
    endpoint = "animal/getLatestAnalysisSummaries"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps({"team_id": teamid, "IDs": projectids})

    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_latest_analysis_summaries = get_latest_analysis_summaries

# This endpoint will return a sliced portion of the data exported from an analysis
# analysisids must be passed through as an array of strings
def get_analyses_export_data(self, teamid, analysisids):
    endpoint = "animal/getAnalysesExportData"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps({"team_id": teamid, "IDs": analysisids})

    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_analyses_export_data = get_analyses_export_data

# This endpoint will return a sliced portion of vulnerabilities data exported from an analysis
def get_analyses_vulnerability_export_data(self, teamid, analysisids):
    endpoint = "animal/getAnalysesVulnerabilityExportData"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps({"team_id": teamid, "IDs": analysisids})

    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_analyses_vulnerability_export_data = (
    get_analyses_vulnerability_export_data
)

# This endpoint will extract information about a certain repository repo_name must be path
# after https://github.com/
def get_repository(self, repo_name):
    endpoint = "repo/getRepo"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"repo": repo_name}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_repository = get_repository

# Will need more information before commenting on this endpoints functionality
def get_repositories_in_common(self, options):
    endpoint = "repo/getReposInCommon"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps(options)
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_repositories_in_common = get_repositories_in_common

# Will need more information before commenting on this endpoints functionality
def get_repositories_for_actor(self, name):
    endpoint = "repo/getReposForActor"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"name": name}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_repositories_for_actor = get_repositories_for_actor

# Will need more information before commenting on this endpoints functionality
def search_repository(self, query):
    endpoint = "repo/search"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"q": query}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.search_repository = search_repository

# Will need more information before commenting on this endpoints functionality
def get_delivery_destinations(self, team_id):
    endpoint = "teams/getDeliveryDestinations"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"id": team_id}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_delivery_destinations = get_delivery_destinations

# Will need more information before commenting on this endpoints functionality
def delete_delivery_destination(self, teamid):
    endpoint = "teams/deleteDeliveryDestination"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"id": teamid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.delete(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    # check = response_handler(r)
    # if check != 0:
    #     return -1
    # dictionary_data = json.loads(r.content)
    return r.content


IonChannel.delete_delivery_destination = delete_delivery_destination

# Will need more information before commenting on this endpoints functionality
def create_delivery_destination(self, teamid, location, region, name, desttype):
    endpoint = "teams/createDeliveryDestination"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    logging.debug(f"Http Destination: {URL}")
    json_data = json.dumps(
        {
            "team_id": teamid,
            "Location": location,
            "Region": region,
            "Name": name,
            "type": desttype,
        }
    )
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.create_delivery_destination = create_delivery_destination


def get_versions_for_dependency(self, package_name, ecosystem):
    endpoint = "dependency/getVersions"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"name": package_name, "type": ecosystem}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_versions_for_dependency = get_versions_for_dependency


def search_dependencies(self, org):
    endpoint = "dependency/search"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"q": org}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.search_dependencies = search_dependencies


def get_latest_version_for_dependency(self, package_name, ecosystem):
    endpoint = "dependency/getLatestVersionForDependency"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"name": package_name, "type": ecosystem}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_latest_version_for_dependency = get_latest_version_for_dependency


def add_alias(self, teamid, projectid, name, version, org):
    endpoint = (
        "project/addAlias?team_id=" + str(teamid) + "&project_id=" + str(projectid)
    )
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps({"Name": name, "Version": version, "Org": org})
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.add_alias = add_alias

# This endpoint needs verification
def resolve_dependencies_in_file(self, file, flatten, ecosystem):
    endpoint = (
        "dependency/resolveDependenciesInFile?"
        + "Flatten="
        + str(flatten)
        + "&type="
        + str(ecosystem)
    )
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    # json_data = {"file": file}
    file_data = {"file": open(file, "r")}
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, files=file_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.resolve_dependencies_in_file = resolve_dependencies_in_file

# This endpoint will return vulnerability statistics from a series of projects
def get_vulnerability_statistics(self, projectids):
    endpoint = "animal/getVulnerabilityStats"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps({"ids": projectids})
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_vulnerability_statistics = get_vulnerability_statistics

# This endpoint will return raw vulnerability statistics from a series of projects
def get_raw_vulnerability_statistics(self, projectids):
    endpoint = "animal/getVulnerabilityStats"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps({"ids": projectids})
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    return r.content


IonChannel.get_raw_vulnerability_statistics = get_raw_vulnerability_statistics


# This endpoint will return a pass fail summary for a series of projects
def get_portfolio_pass_fail_summary(self, projectids):
    endpoint = "ruleset/getStatuses"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps({"ids": projectids})
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_portfolio_pass_fail_summary = get_portfolio_pass_fail_summary

# This endpoint will return information regarding the analysis status' for a series of projects
def get_portfolio_started_errored_summary(self, projectids):
    endpoint = "scanner/getStatuses"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps({"ids": projectids})
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_portfolio_started_errored_summary = get_portfolio_started_errored_summary


def get_portfolio_affected_projects(self, teamid, externalid):
    endpoint = "animal/getAffectedProjectIds"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"id": teamid, "external_id": externalid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_portfolio_affected_projects = get_portfolio_affected_projects


def get_portfolio_affected_projects_info(self, ids):
    endpoint = "project/getAffectedProjectsInfo"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps({"ids": ids})
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_portfolio_affected_projects_info = get_portfolio_affected_projects_info


def get_vulnerability_metrics(self, metric, projectids):
    endpoint = "animal/getScanMetrics"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps({"metric": metric, "project_ids": projectids})
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_vulnerability_metrics = get_vulnerability_metrics


def get_raw_vulnerability_metrics(self, metric, projectids):
    endpoint = "animal/getScanMetrics"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps({"metric": metric, "project_ids": projectids})
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    return r.content


IonChannel.get_raw_vulnerability_metrics = get_raw_vulnerability_metrics


# IONUI endpoints below
# ---------------------------------------------------------------------------------------------------------

# This endpoint will return project data from the API when passed a teamid and projectid
def get_project_report(self, teamid, projectid):
    endpoint = "report/getProject"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"team_id": teamid, "project_id": projectid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_project_report = get_project_report

# This endpoint will return raw project data from the API when passed a teamid and projectid
def get_raw_project(self, teamid, projectid):
    endpoint = "report/getProject"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"team_id": teamid, "project_id": projectid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    return r.content


IonChannel.get_raw_project = get_raw_project

# This endpoint will update a ruleset over a set of projects - projectids
def update_ruleset_for_project(self, rulesetid, projectids):
    endpoint = "project/updateRulesetForProjects"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps({"ruleset_id": rulesetid, "project_ids": projectids})
    logging.debug(f"Http Destination: {URL}")
    r = requests.put(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.update_ruleset_for_project = update_ruleset_for_project

# This endpoint takes an array of projectids as well as a project dictionary
# and updates all projects based on the proposed content in the dictionary.
# Example project content would be {"monitor": True}
def update_projects(self, projectids, project):
    endpoint = "project/updateProjects"
    head = {"Authorization": "Bearer " + self.token}

    parameters = project
    json_data = json.dumps({"project_ids": projectids})

    URL = self.baseURL + endpoint
    logging.debug(f"Http Destination: {URL}")
    r = requests.put(URL, headers=head, params=parameters, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.update_projects = update_projects

# This endpoint takes in a projectid, teamid, and analysisid and
# returns the respective digest
def get_digests(self, projectid, teamid, analysisid):
    endpoint = "report/getDigests"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"project_id": projectid, "team_id": teamid, "id": analysisid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_digests = get_digests

# This endpoint takes in a teamid and will return the state of the projects
# within the corresponding team
def get_portfolio(self, teamid):
    endpoint = "report/getPortfolio"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"id": teamid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_portfolio = get_portfolio

# This endpoint takes in a teamid and will return a list of vulnerabilities
# that were found for any of the projects belonging to that team
def get_vulnerability_list(self, teamid):
    endpoint = "report/getVulnerabilityList"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"id": teamid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_vulnerability_list = get_vulnerability_list

# This endpoint will fetch a list of projects that have been tagged with a specific
# vulnerability within a team. The specified vulnerability is listed as the externalid
def get_affected_projects(self, teamid, externalid):
    endpoint = "report/getAffectedProjects"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"id": teamid, "external_id": externalid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_affected_projects = get_affected_projects

# This endpoint will retun a project's history (pass/fail state, ruleset changes, etc.)
# based on an inputted teamid and projectid
def get_project_history(self, teamid, projectid):
    endpoint = "report/getProjectHistory"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"team_id": teamid, "project_id": projectid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_project_history = get_project_history

# This endpoint is still in the works, use CAUTIOUSLY
def get_public_analysis(self, analysisid):
    endpoint = "report/getPublicAnalysis"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"analysis_id": analysisid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_public_analysis = get_public_analysis

# This endpoint will output a set of rules that could potentially used in a ruleset
def get_rules(self):
    endpoint = "ruleset/getRules"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_rules = get_rules

# This endpoint fetches all rulesets that were in use for a given team
def get_rulesets(self, teamid):
    endpoint = "ruleset/getRulesets"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"team_id": teamid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_rulesets = get_rulesets

# This ednpoint will fetch the analysis history of a project
def get_pass_fail_history(self, projectid):
    endpoint = "ruleset/getProjectHistory"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"project_id": projectid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_pass_fail_history = get_pass_fail_history

# This endpoint takes in a teamid, projectid, and analysis id and outputs the
# corresponding analysis report
def get_analysis_report(self, teamid, projectid, analysisid):
    endpoint = "report/getAnalysis"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"team_id": teamid, "project_id": projectid, "analysis_id": analysisid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_analysis_report = get_analysis_report

# This endpoint takes in a teamid, projectid, and analysis id and outputs the
# raw corresponding analysis report
def get_raw_analysis_report(self, teamid, projectid, analysisid):
    endpoint = "report/getAnalysis"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"team_id": teamid, "project_id": projectid, "analysis_id": analysisid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1

    return r.content


IonChannel.get_raw_analysis_report = get_raw_analysis_report

# This endpoint takes in a teamid and will return a list of projects
# that belong to the corresponding team
def get_projects_report(self, teamid):
    endpoint = "report/getProjects"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"team_id": teamid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_projects_report = get_projects_report

# This endpoint will take in a teamid, ruleset name, ruleset description, and
# a set of rules - ruleids, and return a created ruleset
def create_ruleset(self, teamid, name, description, ruleids):
    endpoint = "ruleset/createRuleset"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps(
        {
            "team_id": teamid,
            "rule_ids": ruleids,
            "name": name,
            "description": description,
        }
    )
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.create_ruleset = create_ruleset

# This endpoint will delete a ruleset when inputted with a corresponding team - teamid,
# and ruleset - rulesetid
def delete_ruleset(self, teamid, rulesetid):
    endpoint = "ruleset/deleteRuleset"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"team_id": teamid, "ruleset_id": rulesetid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.delete(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.delete_ruleset = delete_ruleset

# This endpoint will return vulnerabiltity data for a series of projects - projectids
# within a corresponding team - teamid
def get_exported_vulnerability_data(self, teamid, projectids):
    endpoint = "report/getExportedVulnerabilityData"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps({"team_id": teamid, "ids": projectids})
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_exported_vulnerability_data = get_exported_vulnerability_data


# This endpoint will get exported projects data for a list of projects - ids, based
# on an inputted team - teamid
def get_exported_projects_data(self, teamid, ids):
    endpoint = "report/getExportedData"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps({"team_id": teamid, "ids": ids})
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_exported_projects_data = get_exported_projects_data

# This endpoint will return the latest analysis status of a given project,
# when inputted with a corresponding teamid and projectid
def get_latest_analysis_status(self, teamid, projectid):
    endpoint = "scanner/getLatestAnalysisStatus"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"team_id": teamid, "project_id": projectid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_latest_analysis_status = get_latest_analysis_status

# This endpoint returns information corresponding to a specific team
# (based on teamid)
def get_team(self, teamid):
    endpoint = "teams/getTeam"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"id": teamid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_team = get_team

# This endpoint will logout and a user's running session
def logout(self):
    endpoint = "sessions/logout"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    logging.debug(f"Http Destination: {URL}")
    r = requests.delete(URL, headers=head)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    if str(r.content) == "b''":
        return r.content
    else:
        check = response_handler(r)
        if check != 0:
            return -1
        dictionary_data = json.loads(r.content)
        return dictionary_data


IonChannel.logout = logout

# This endpoint takes a series of projectids and performs an analysis
# on each of the corresponding projects
def analyze_projects(self, projectids):
    endpoint = "scanner/analyzeProjects"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint

    for index in range(len(projectids)):
        projectids[index] = {"project_id": projectids[index]}

    json_data = json.dumps(projectids)
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.analyze_projects = analyze_projects

# This endpoint performs a search based on a series of parameters
# "query" parameter is required is the text that the search will be applied upon.
# "tbs" parameter is optional and indicates that the search will query for repositories.
# "offset" parameter is optional and is for pagination purposes, it indicates at what
# record to begin returning results on.
# "limit" parameter is optional and describes the number of records to return for
# pagination purposes.
def search(self, query, tbs=None, offset=None, limit=None):
    endpoint = "search"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"q": query}

    if tbs is not None:
        parameters["tbs"] = tbs

    if offset is not None:
        parameters["offset"] = offset

    if limit is not None:
        parameters["limit"] = limit

    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.search = search

# This endpoint will return an array of users that are on a team
# when inputted with the corresponding teamid
def get_team_users(self, teamid):
    endpoint = "teamUsers/getTeamUsers"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"team_id": teamid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_team_users = get_team_users

# This endpoint will create a new team when inputted with a name,
# pocname, pocemail, and username
def create_team(self, name, pocname, pocemail, username):
    endpoint = "teams/establishTeam"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps(
        {"name": name, "poc_name": pocname, "poc_email": pocemail, "username": username}
    )
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.create_team = create_team

# This endpoint will update a team when inputted with teamid, name, pocname
# pocemail, and a default deoploy key (openssh key / rsa key)
def update_team(self, teamid, name, pocname, pocemail, defaultdeploykey):
    endpoint = "teams/updateTeam"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"id": teamid}
    json_data = json.dumps(
        {
            "name": name,
            "poc_name": pocname,
            "poc_email": pocemail,
            "default_deploy_key": defaultdeploykey,
        }
    )
    logging.debug(f"Http Destination: {URL}")
    r = requests.put(URL, headers=head, params=parameters, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.update_team = update_team

# This endpoint will invite a user to a team, this endpoint requires a teamid
# role and user id. Role can be 'memeber', 'admin', 'sysadmin' etc.
def invite_team_user(self, teamid, role, userid, email=None):
    endpoint = "teamUsers/inviteTeamUser"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = {"team_id": teamid, "role": role, "user_id": userid}
    if email is not None:
        json_data["email"] = email

    json_data = json.dumps(json_data)
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.invite_team_user = invite_team_user

# This endpoint will return information regarding an invite when passed
# a corresponding userid and invite token. The latter bearer token is then
# passed through for authentication
def get_team_invite(self, inviteid, invitetoken):
    endpoint = "teamUsers/getInvite"
    head = {"Authorization": "Bearer " + invitetoken}
    URL = self.baseURL + endpoint
    parameters = {"someid": inviteid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_team_invite = get_team_invite

# This endpoint will accept an invite when passed with
# a corresponding userid and invite token. The latter bearer token is then
# passed through for authentication
def accept_team_invite(self, inviteid, invitetoken):
    endpoint = "teamUsers/acceptInvite"
    head = {"Authorization": "Bearer " + invitetoken}
    URL = self.baseURL + endpoint
    json_data = json.dumps({"someid": inviteid})
    logging.debug(f"Http Destination: {URL}")
    r = requests.put(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    if str(r.content) == "b''":
        return r.content
    else:
        check = response_handler(r)
        if check != 0:
            return -1
        dictionary_data = json.loads(r.content)
        return dictionary_data


IonChannel.accept_team_invite = accept_team_invite

# This endpoint will delete a user for a specific team based on the
# corresponding teamuserid
def delete_team_user(self, teamuserid):
    endpoint = "teamUsers/deleteTeamUser"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps({"someid": teamuserid})
    logging.debug(f"Http Destination: {URL}")
    r = requests.delete(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.delete_team_user = delete_team_user

# This endpoint will resend an invite for a team user based on
# a correspoinding invited
def resend_invite_team_user(self, inviteid):
    endpoint = "teamUsers/resendInvite"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps({"someid": inviteid})
    logging.debug(f"Http Destination: {URL}")
    r = requests.put(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.resend_invite_team_user = resend_invite_team_user

# This endpoint will update a users role/status based on a corresponding
# teamuserid, role = 'admin', 'member', 'sys_admin'?, etc.
def update_team_user(self, teamuserid, role, status):
    endpoint = "teamUsers/updateTeamUser"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps({"someid": teamuserid, "role": role, "status": status})
    logging.debug(f"Http Destination: {URL}")
    r = requests.put(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.update_team_user = update_team_user

# This endpoint will return a series of tokens created by a corresponding user.
# The cli parameter has a default value of True
def get_tokens(self, cli=True):
    endpoint = "tokens/getTokens"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    if cli:
        cli = "true"
    elif not cli:
        cli = "false"
    parameters = {"cli": cli}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_tokens = get_tokens

# This enpoint will return a series of projects based on the corresponding
# inputted dependency name, organization, and version
def get_projectids_by_dependency(self, teamid, name, organization, version):
    endpoint = "report/getProjectsByDependency"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {
        "team_id": teamid,
        "name": name,
        "org": organization,
        "version": version,
    }
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_projectids_by_dependency = get_projectids_by_dependency

# This endpoint will return exported vulnerability data for a series of projects - projectids,
# within a corresponding team - teamid, in a CSV formatted list
def get_exported_vulnerability_data_csv(self, teamid, projectids):
    endpoint = "report/getExportedVulnerabilityData"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps({"team_id": teamid, "ids": projectids})
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_exported_vulnerability_data_csv = get_exported_vulnerability_data_csv

# This endpoint will create a new token for a user and will return corresponding information.
# The cli parameter has a default value of True
def create_token(self, name, cli=True):
    endpoint = "tokens/createToken"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    if cli:
        cli = "true"
    elif not cli:
        cli = "false"
    parameters = {"name": name, "cli": cli}

    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.create_token = create_token

# This endpoint will delete a token when inputted with a corresponding token id
def delete_token(self, tokenid):
    endpoint = "tokens/deleteToken"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"id": tokenid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.delete(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    if str(r.content) == "b''":
        return r.content
    else:
        check = response_handler(r)
        if check != 0:
            return -1
        dictionary_data = json.loads(r.content)
        return dictionary_data


IonChannel.delete_token = delete_token

# Fetches information corresponding to a user during an authenticated session
def get_self(self):
    endpoint = "users/getSelf"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_self = get_self

# This endpoint will fetch a list of users on a team, this information can only be viewed
# by users with an admin or sysadmin status
def get_users(self):
    endpoint = "users/getUsers"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_users = get_users

# This endpoint will refresh a corresponding user token
def refresh_token(self):
    endpoint = "tokens/refreshToken"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.refresh_token = refresh_token

# This endpoint will get usage information when inputted with a corresponding
# team - teamid
def get_usage_information(self, teamid):
    endpoint = "usage/info"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"team_id": teamid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_usage_information = get_usage_information

# This endpoint will reset an account password, based on the user's
# corresponding email
def reset_password(self, email):
    endpoint = "users/resetPassword"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps({"email": email})
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.reset_password = reset_password

# This endpoint will complete signup by allowing a user to set a password after
# they have been invited. This endpoint requires the invited user's username,
# alongside corresponding password information
def complete_signup(self, username, password, passwordConfirmation):
    endpoint = "users/complete"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps(
        {
            "username": username,
            "password": password,
            "password_confirmation": passwordConfirmation,
        }
    )
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.complete_signup = complete_signup

# This endpoint will update information corresponding to a specific user - userid,
# If values are to be left unchanged, pass empty string: "" or don't pass the parameter
# through to this function.
def update_user(self, userid, email=None, username=None, password=None):
    endpoint = "users/updateUser"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = {"someid": userid}
    if email is not None and email != "":
        json_data["email"] = email
    if username is not None and username != "":
        json_data["username"] = username
    if password is not None and password != "":
        json_data["password"] = password
    json_data = json.dumps(json_data)
    logging.debug(f"Http Destination: {URL}")
    r = requests.put(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.update_user = update_user

# This endpoint will return information regarding a given vulnerability
# based on its correspondingly inputted vulnerabilityid
def get_vulnerability(self, vulnerabilityid):
    endpoint = "vulnerability/getVulnerability"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"external_id": vulnerabilityid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_vulnerability = get_vulnerability

# This endpoint will return raw information regarding a given vulnerability
# based on its correspondingly inputted vulnerabilityid
def get_raw_vulnerability(self, vulnerabilityid):
    endpoint = "vulnerability/getVulnerability"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"external_id": vulnerabilityid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    return r.content


IonChannel.get_raw_vulnerability = get_raw_vulnerability


# This endpoint will reuturn a set of vulnerabilities attached to a specific
# product with a corresponding version number. Offset - for pagination purposes -
# describes where the starting point would be to return records, is by default 0.
# Limit - for pagination purposes - describes how many possible records to be returned,
# is by default 10
def get_vulnerabilities(self, product, version, offset=0, limit=10):
    endpoint = "vulnerability/getVulnerabilities"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {
        "product": product,
        "version": version,
        "offset": offset,
        "limit": limit,
    }
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_vulnerabilities = get_vulnerabilities

# This endpoint takes in a product name and returns information with
# regards to the corresponding product
def get_product(self, productname):
    endpoint = "vulnerability/getProducts"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"product": productname}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_product = get_product

# This endpoint will return depenency statisitics for a set of corresponding
# inputted projects - projectids
def get_dependency_statistics(self, projectids):
    endpoint = "animal/getDependencyStats"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps({"Ids": projectids})
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_dependency_statistics = get_dependency_statistics

# This endpoint will return raw dependency information for a set of projects - projectids,
# can be sorted by listType - name/impact - and a limit of returned results can also
# be passed through - limit. ListType and limit are optional and are default set to None.
def get_raw_dependency_list(self, projectids, listType=None, limit=None):
    endpoint = "animal/getDependencyList"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint

    json_data = {"ids": projectids}

    if listType is not None:
        json_data["list_type"] = listType

    if limit is not None:
        json_data["limit"] = limit

    json_data = json.dumps(json_data)
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    return r.content


IonChannel.get_raw_dependency_list = get_raw_dependency_list

# This endpoint will return dependency information for a set of projects - projectids,
# can be sorted by listType - name/impact - and a limit of returned results can also
# be passed through - limit. ListType and limit are optional and are default set to None.
def get_dependency_list(self, projectids, listType=None, limit=None):
    endpoint = "animal/getDependencyList"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint

    json_data = {"ids": projectids}

    if listType is not None:
        json_data["list_type"] = listType

    if limit is not None:
        json_data["limit"] = limit

    json_data = json.dumps(json_data)
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_dependency_list = get_dependency_list

# This endpoint will return the project status history for a set of
# corresponding projects - projectids
def get_projects_status_history(self, projectids):
    endpoint = "ruleset/getStatusesHistory"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps({"Ids": projectids})
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_projects_status_history = get_projects_status_history

# This endpoint takes in a teamid and an optional projectid. If projectid is given the
# endpoint will return corresponding mttr information for the respective project, if projectid
# is not given - defaut case set to None - the endpoint will return mttr information for all active
# projects on the team
def get_mttr(self, teamid, projectid=None):
    endpoint = "report/getMttr"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"team_id": teamid}
    if projectid is not None:
        parameters["project_id"] = projectid
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_mttr = get_mttr

# This endpoint will return a set of projectids within a team that have the
# corresponding dependency - name, organization, and version
def get_projects_by_dependency(self, teamid, name, organization, version):
    endpoint = "animal/getProjectIdsByDependency"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {
        "team_id": teamid,
        "name": name,
        "org": organization,
        "version": version,
    }
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_projects_by_dependency = get_projects_by_dependency

# This endpoint will return product versions with a correspondingly specific name and version.
# The name parameter is required, however, the version parameter is optional with a default set to None
def get_product_versions(self, name, version=None):
    endpoint = "product/getProductVersions"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"name": name}
    if version is not None:
        parameters["version"] = version
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_product_versions = get_product_versions

# This endpoint will take in a search query - searchInput - and return all
# corresponding matching products within the Bunsen Dependencies Table
def get_product_search(self, searchInput):
    endpoint = "product/search"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"q": searchInput}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_product_search = get_product_search


# This endpoint takes in a product name and returns raw information with
# regards to the corresponding product
def get_raw_product(self, productname):
    endpoint = "vulnerability/getProducts"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"product": productname}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    return r.content


IonChannel.get_raw_product = get_raw_product

# This endpoint will create a project, or a series of projects from a
# correspondingly uploaded CSV file
def create_projects_from_csv(self, teamid, csvfile):
    endpoint = "project/createProjectsCSV"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"team_id": teamid}
    file_data = {"file": open(csvfile, "r")}
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, params=parameters, files=file_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.create_projects_from_csv = create_projects_from_csv

# This endpoint will return project information when inputted with a corresponding
# teamid and projectid
def get_project(self, teamid, projectid):
    endpoint = "project/getProject"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"team_id": teamid, "id": projectid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_project = get_project


# This endpoint will return raw project information when inputted with a corresponding
# teamid and projectid
def get_raw_project(self, teamid, projectid):
    endpoint = "project/getProject"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"team_id": teamid, "id": projectid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    return r.content


IonChannel.get_raw_project = get_raw_project

# This endpoint will return project information based on a corresponding uri
# and teamid
def get_project_by_url(self, teamid, uri):
    endpoint = "project/getProjectByUrl"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"url": uri, "team_id": teamid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_project_by_url = get_project_by_url

# This endpoint will return used rulesetids for a corresponding team - teamid
def get_used_ruleset_ids(self, teamid):
    endpoint = "project/getUsedRulesetIds"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"team_id": teamid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_used_ruleset_ids = get_used_ruleset_ids

# This endpoint will return projectnames for all correspondingly inputted projects - projectids
# and the team in which they are located - teamid
def get_projects_names(self, teamid, projectids):
    endpoint = "project/getProjectsNames"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps({"team_id": teamid, "IDs": projectids})
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_projects_names = get_projects_names

# This endpoint will return the related/tangential analysis to the analysis provided
# when inputted with the corresponding teamid, projectid, and analysisid
# This endpoint might be DEPRECATED
def get_analysis_navigation(self, teamid, projectid, analysisid):
    endpoint = "report/getAnalysisNav"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"team_id": teamid, "project_id": projectid, "analysis_id": analysisid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_analysis_navigation = get_analysis_navigation

# This endpoint takes an array of tuples (a, b), where index "a" (0) of the tuple is
# the teamid, and index "b" (1) of the tuple is the projectid, the endpoint will then
# return respective applied rulesets on inputted projects
def get_applied_rulesets(self, appliedRequestBatch):
    endpoint = "ruleset/getAppliedRulesets"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = []
    for item in appliedRequestBatch:
        json_data.append({"team_id": item[0], "project_id": item[1]})

    json_data = json.dumps(json_data)
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_applied_rulesets = get_applied_rulesets

# This endpoint takes an array of tuples (a, b), where index "a" (0) of the tuple is
# the teamid, and index "b" (1) of the tuple is the projectid, the endpoint will then
# return briefed results on the corresponding applied rulesets
def get_applied_rulesets_brief(self, appliedRequestBatch):
    endpoint = "ruleset/getAppliedRulesets"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"summarized": "true"}
    json_data = []
    for item in appliedRequestBatch:
        json_data.append({"team_id": item[0], "project_id": item[1]})

    json_data = json.dumps(json_data)
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, params=parameters, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_applied_rulesets_brief = get_applied_rulesets_brief

# This endpoint will return True if the ruleset exists, and False if the ruleset
# doesn't exist or an error occurs
def ruleset_exists(self, teamid, rulesetid):
    endpoint = "ruleset/getRuleset"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"team_id": teamid, "id": rulesetid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")

    if r.status_code < 200 or r.status_code >= 300:
        return False

    return True


IonChannel.ruleset_exists = ruleset_exists

# This endpoint will return the names of rulesets when passed through with their corresponding
# rulesetids - array
def get_ruleset_names(self, rulesetids):
    endpoint = "ruleset/getRulesetNames"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps({"IDs": rulesetids})
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_ruleset_names = get_ruleset_names

# This endpoint will return the status of a series of analyses when inputted with the
# corresponding teamid and analysisids - array
def get_analyses_statuses(self, teamid, analysisids):
    endpoint = "ruleset/getAnalysesStatuses"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps({"team_id": teamid, "IDs": analysisids})
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_analyses_statuses = get_analyses_statuses

# This endpoint will return the latest analysis statuses when inputted with
# the corresponding team - teamid
def get_latest_analysis_statuses(self, teamid):
    endpoint = "scanner/getLatestAnalysisStatuses"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"team_id": teamid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_latest_analysis_statuses = get_latest_analysis_statuses

# This endpoint will return project states when inputted with a corresponding list of projects - projectids
# This endpoint has an optional filter parameter which allows users to pass a string to filter state results
def get_project_states(self, projectids, filter=None):
    endpoint = "scanner/getProjectsStates"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = {"IDs": projectids}

    if filter is not None:
        json_data["Filter"] = filter

    json_data = json.dumps(json_data)

    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_project_states = get_project_states

# This endpoint will search for a series of scans within a  team - teamid
# and return corresponding data, this endpoint has a searchParams parameters
# which takes in a dictionary, that has two fields to help filter search results.
# Search Parameter Example:
# {
#     "analysis_ids": ["analysisid1", "analysisid2"],
#     "scan_types": ["scanfilter1", "scanfilter2"]
# }
def find_scans(self, searchParams, teamid):
    endpoint = "animal/findScans"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"team_id": teamid}
    json_data = json.dumps(searchParams)
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, params=parameters, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.find_scans = find_scans

# This endpoint will return any matching secrets to the inputted text,
# the return type - if successful - will have three fields:
# Rule: This field describes the defined rule that was matched
# Match: This field describes the subtext that was matched
# Confidence: This field describes the trust in the returned result from 0.0 to 1.0
def get_secrets(self, text):
    endpoint = "metadata/getSecrets"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    text_data = text
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=text_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_secrets = get_secrets

# This endpoint will create a new tag when inputted with a corresponidng team - teamid,
# name, and description
def create_tag(self, teamid, name, description):
    endpoint = "tag/createTag"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps(
        {"team_id": teamid, "Name": name, "description": description}
    )
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.create_tag = create_tag

# This endpoint will update a tag's information when inputted with a corresponding, tagid,
# teamid, name, and description
def update_tag(self, tagid, teamid, name, description):
    endpoint = "tag/updateTag"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps(
        {"ID": tagid, "team_id": teamid, "Name": name, "Description": description}
    )
    logging.debug(f"Http Destination: {URL}")
    r = requests.put(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.update_tag = update_tag

# This endpoint will return information about a respective tag when inputted with a correspondiing
# tagid - tag identifier, and teamid - team identifier
def get_tag(self, tagid, teamid):
    endpoint = "tag/getTag"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"id": tagid, "team_id": teamid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_tag = get_tag

# This endpoint will return raw information about a respective tag when inputted with a correspondiing
# tagid - tag identifier, and teamid - team identifier
def get_raw_tag(self, tagid, teamid):
    endpoint = "tag/getTag"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"id": tagid, "team_id": teamid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    return r.content


IonChannel.get_raw_tag = get_raw_tag

# This endpoint will return information regarding all tags for a corrsponding
# team - takes in teamid
def get_tags(self, teamid):
    endpoint = "tag/getTags"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"team_id": teamid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_tags = get_tags

# This endpoint will return raw information regarding all tags for a corrsponding
# team - takes in teamid
def get_raw_tags(self, teamid):
    endpoint = "tag/getTags"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"team_id": teamid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    return r.content


IonChannel.get_raw_tags = get_raw_tags


# def create_user(self, email, username=None, password=None):
#     endpoint = "users/createUser"
#     head = {"Authorization": "Bearer " + self.token}
#     URL = self.baseURL + endpoint
#     json_data = {"email": email}
#     if username is not None:
#         json_data["username"] = username
#     if password is not None:
#         json_data["password"] = password
#         json_data["password_confirmation"] = password

#     json_data = json.dumps(json_data)
#     logging.debug(f"Http Destination: {URL}")
#     r = requests.post(URL, headers=head, data=json_data)

#     logging.debug(f"Request Type: {r.request}")
#     logging.debug(f"Status Code: {r.status_code}")
#     check = response_handler(r)
#     if check != 0:
#         return -1
#     dictionary_data = json.loads(r.content)
#     return dictionary_data

# IonChannel.create_user = create_user

# This endpoint will create a new user when inputted with an email, name
# username, and password
def create_user(self, email, name, username, password):
    endpoint = "users/signup"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps(
        {
            "email": email,
            "name": name,
            "username": username,
            "password": password,
            "password_confirmation": password,
        }
    )
    r = requests.post(URL, headers=head, data=json_data)

    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.create_user = create_user


# This endpoint takes in a dictionary with the fields:
# status, role, team_id, and user_id, and adds a user to the latter corresponding
# team
def create_team_user(self, teamuseroptions):
    endpoint = "teamUsers/createTeamUser"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    json_data = json.dumps(teamuseroptions)
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.create_team_user = create_team_user

# This endpoint will return information regarding a user when inputted with a
# corresponding userid
def get_user(self, userid):
    endpoint = "users/getUser"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"id": userid}
    logging.debug(f"Http Destination: {URL}")
    r = requests.get(URL, headers=head, params=parameters)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_user = get_user

# This endpoint takes in an array of userids and a corresponding teamid,
# and will return a set of respective usernames
def get_user_names(self, userids, teamid):
    endpoint = "users/getUserNames"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    parameters = {"team_id": teamid}
    json_data = json.dumps({"IDs": userids})
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, params=parameters, data=json_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_user_names = get_user_names


# def add_vulnerability(self, vulnerability):
#     endpoint = "internal/vulnerability/addVulnerability"
#     head = {"Authorization": "Bearer " + self.token}
#     URL = self.baseURL + endpoint
#     json_data = json.dumps(vulnerability)
#     r = requests.post(URL, headers=head, data=json_data)

#     print(f"{r.status_code}\n\n\n")
#     return r.content

# IonChannel.add_vulnerability = add_vulnerability

# This endpoint takes in a dependency file path and will return vulnerabilities within the file
def get_vulnerabilities_in_file(self, file):
    endpoint = "vulnerability/getVulnerabilitiesInFile"
    head = {"Authorization": "Bearer " + self.token}
    URL = self.baseURL + endpoint
    file_data = {"file": open(file, "r")}
    logging.debug(f"Http Destination: {URL}")
    r = requests.post(URL, headers=head, files=file_data)
    logging.debug(f"Request Type: {r.request}")
    logging.debug(f"Status Code: {r.status_code}")
    check = response_handler(r)
    if check != 0:
        return -1
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_vulnerabilities_in_file = get_vulnerabilities_in_file


# FILE REROUTING TESTING:
# ion_client = new_client("https://api.test.ionchannel.io/v1/")
# token = ion_client.login()
# print(ion_client.get_delivery_destinations("646fa3e5-e274-4884-aef2-1d47f029c289"))

# def scan_report(self, analysisid, teamid, projectid):
#     endpoint = 'animal/findScans'
#     head = {'Authorization': 'Bearer ' + self.token}
#     URL = self.baseURL + endpoint
#     parameters = {'scan_id': analysisid}
#     r = requests.get(URL, headers=head, params=parameters)

#     return r.text
# IonChannel.scan_report = scan_report


# This is a test commit to ensure everything is working
# This is another modified test commit for build pipeline
