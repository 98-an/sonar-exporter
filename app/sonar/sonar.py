import datetime
from util.export import (export_csv)
import requests
from requests.auth import HTTPBasicAuth


def export_all_sonar_users(sonar_site, sonar_protocol, sonar_domain_name, sonar_token, export_filename):
    users_list = []
    users_count = 0

    print('{} - INFO - Reading Sonar users from Sonar API of {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), sonar_site))

    response_page = 1
    while response_page > 0:
        users_response = requests.get(
            '{}://{}/api/users/search?p={}'.format(sonar_protocol, sonar_domain_name, response_page),
            auth=HTTPBasicAuth(sonar_token, "")
        ).json()

        for user in users_response["users"]:
            user_login = user.get('login')
            user_name = user.get('name')
            user_active = user.get('active')
            user_tokens_count = user.get('tokensCount')
            user_local = user.get('local')
            user_external_identity = user.get('externalIdentity')
            user_external_provider = user.get('externalProvider')
            user_email = user.get('email')
            user_last_connection_date = user.get('lastConnectionDate')

            users_list.append({
                'date': datetime.datetime.now().strftime("%Y%m%d"),
                'user_login': user_login,
                'user_name': user_name,
                'user_active': user_active,
                'user_tokens_count': user_tokens_count,
                'user_local': user_local,
                'user_external_identity': user_external_identity,
                'user_external_provider': user_external_provider,
                'user_email': user_email,
                'user_last_connection_date': user_last_connection_date
            })
            users_count = users_count + 1

        if int(int(users_response["paging"].get("total")) / int(users_response["paging"].get("pageSize"))) >= response_page:
            response_page = response_page + 1
        else:
            response_page = 0

    print('{} - INFO - Total: {} users'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), str(users_count)))

    export_csv(
        export_filename,
        users_list,
        ['date', 'user_login', 'user_name', 'user_active', 'user_tokens_count', 'user_local', 'user_external_identity', 'user_external_provider', 'user_email', 'user_last_connection_date'],
        ['date', 'user_login', 'user_name', 'user_active', 'user_tokens_count', 'user_local', 'user_external_identity', 'user_external_provider', 'user_email', 'user_last_connection_date']
    )

    return users_list


def export_all_sonar_groups(sonar_site, sonar_protocol, sonar_domain_name, sonar_token, export_filename):
    groups_list = []
    groups_count = 0

    print('{} - INFO - Reading Sonar groups from Sonar API of {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), sonar_site))

    response_page = 1
    while response_page > 0:
        groups_response = requests.get(
            '{}://{}/api/user_groups/search?p={}'.format(sonar_protocol, sonar_domain_name, response_page),
            auth=HTTPBasicAuth(sonar_token, "")
        ).json()

        for group in groups_response["groups"]:
            group_id = group.get('id')
            group_name = group.get('name')
            group_description = group.get('description')
            group_default = group.get('default')

            groups_list.append({
                'date': datetime.datetime.now().strftime("%Y%m%d"),
                'group_id': group_id,
                'group_name': group_name,
                'group_description': group_description,
                'group_default': group_default,
            })
            groups_count = groups_count + 1

        if int(int(groups_response["paging"].get("total")) / int(groups_response["paging"].get("pageSize"))) >= response_page:
            response_page = response_page + 1
        else:
            response_page = 0

    print('{} - INFO - Total: {} groups'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), str(groups_count)))

    export_csv(
        export_filename,
        groups_list,
        ['date', 'group_id', 'group_name', 'group_description', 'group_default'],
        ['date', 'group_id', 'group_name', 'group_description', 'group_default']
    )

    return groups_list


def export_all_sonar_groups_members(sonar_site, sonar_protocol, sonar_domain_name, sonar_token, groups_list, export_filename):
    groups_members_list = []

    print('{} - INFO - Reading Sonar groups members from Sonar API of {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), sonar_site))

    for group in groups_list:

        groups_member_count = 0

        response_page = 1
        while response_page > 0:
            group_members_response = requests.get(
                '{}://{}/api/user_groups/users?name={}&p={}'.format(sonar_protocol, sonar_domain_name, group['group_name'], response_page),
                auth=HTTPBasicAuth(sonar_token, "")
            ).json()

            for group_members in group_members_response["users"]:
                user_login = group_members.get('login')
                user_name = group_members.get('name')
                group_name = group['group_name']
                group_id = group['group_id']

                groups_members_list.append({
                    'date': datetime.datetime.now().strftime("%Y%m%d"),
                    'user_login': user_login,
                    'user_name': user_name,
                    'group_name': group_name,
                    'group_id': group_id
                })

                groups_member_count = groups_member_count + 1

            if int(int(group_members_response.get("total")) / int(group_members_response.get("ps"))) >= response_page:
                response_page = response_page + 1
            else:
                response_page = 0

        print('{} - INFO - Total of {} members for Sonar group {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), str(groups_member_count), group['group_name']))

    export_csv(
        export_filename,
        groups_members_list,
        ['date', 'group_id', 'group_name', 'user_login', 'user_name'],
        ['date', 'group_id', 'group_name', 'user_login', 'user_name']
    )


def export_all_sonar_projects(sonar_site, sonar_protocol, sonar_domain_name, sonar_token, export_filename):
    projects_list = []
    projects_count = 0

    print('{} - INFO - Reading Sonar projects from Sonar API of {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), sonar_site))

    response_page = 1
    while response_page > 0:
        projects_response = requests.get(
            '{}://{}/api/projects/search?p={}'.format(sonar_protocol, sonar_domain_name, response_page),
            auth=HTTPBasicAuth(sonar_token, "")
        ).json()

        for project in projects_response["components"]:
            project_key = project.get('key')
            project_name = project.get('name')
            project_qualifier = project.get('qualifier')
            project_visibility = project.get('visibility')
            project_last_analysis_date = project.get('lastAnalysisDate')
            project_revision = project.get('revision')

            projects_list.append({
                'date': datetime.datetime.now().strftime("%Y%m%d"),
                'project_key': project_key,
                'project_name': project_name,
                'project_qualifier': project_qualifier,
                'project_visibility': project_visibility,
                'project_last_analysis_date': project_last_analysis_date,
                'project_revision': project_revision,
            })
            projects_count = projects_count + 1

        if int(int(projects_response["paging"].get("total")) / int(projects_response["paging"].get("pageSize"))) >= response_page:
            response_page = response_page + 1
        else:
            response_page = 0

    print('{} - INFO - Total: {} projects'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), str(projects_count)))

    export_csv(
        export_filename,
        projects_list,
        ['date', 'project_key', 'project_name', 'project_qualifier', 'project_visibility', 'project_last_analysis_date', 'project_revision'],
        ['date', 'project_key', 'project_name', 'project_qualifier', 'project_visibility', 'project_last_analysis_date', 'project_revision']
    )

    return projects_list


def export_all_sonar_projects_metrics(sonar_site, sonar_protocol, sonar_domain_name, sonar_token, projects_list, export_filename):
    metrics_list = ["ncloc", "comment_lines", "coverage", "bugs", "code_smells", "cognitive_complexity", "development_cost", "duplicated_blocks", "duplicated_files", "duplicated_lines", "violations", "critical_violations", "major_violations", "minor_violations", "sqale_rating", "sqale_index", "sqale_debt_ratio", "projects", "alert_status", "reliability_rating", "reliability_remediation_effort", "security_rating", "security_remediation_effort", "security_hotspots", "tests", "test_execution_time", "test_errors", "test_failures", "test_success_density", "skipped_tests", "vulnerabilities"]

    print('{} - INFO - Reading Sonar projects metrics from Sonar API of {}'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), sonar_site))
    projects_metrics_list = []

    for project in projects_list:

        project_key = project['project_key']
        project_name = project['project_name']

        for project_metric in metrics_list:
            projects_metrics_response = requests.get(
                '{}://{}/api/measures/component?component={}&metricKeys={}'.format(sonar_protocol, sonar_domain_name, project['project_name'], project_metric),
                auth=HTTPBasicAuth(sonar_token, "")
            ).json()

            if len(projects_metrics_response["component"].get("measures"))>0:
                project_metric_value = projects_metrics_response["component"].get("measures")[0].get("value")
            else:
                project_metric_value = ""

            projects_metrics_list.append({
                'date': datetime.datetime.now().strftime("%Y%m%d"),
                'project_key': project_key,
                'project_name': project_name,
                'project_metric': project_metric,
                'project_metric_value': project_metric_value
            })

    print('{} - INFO - Total: {} Projects and {} metrics per Project'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), len(projects_list), len(metrics_list)))

    export_csv(
        export_filename,
        projects_metrics_list,
        ['date', 'project_key', 'project_name', 'project_metric', 'project_metric_value'],
        ['date', 'project_key', 'project_name', 'project_metric', 'project_metric_value']
    )
