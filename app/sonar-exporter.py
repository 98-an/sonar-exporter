import os
import sys
import datetime

from util.config import (get_sonar_config_file, get_cli_params)
from sonar.sonar import (
    export_all_sonar_users,
    export_all_sonar_groups,
    export_all_sonar_groups_members,
    export_all_sonar_projects,
    export_all_sonar_projects_metrics,
    export_all_sonar_projects_analyses,
    export_all_sonar_projects_analyses_metrics,
    export_all_sonar_projects_quality_gates,
    export_all_sonar_projects_analyses_qg,
    get_all_sonar_projects
)


if __name__ == '__main__':

    # Get command line parameters
    config_file, action = get_cli_params(sys.argv[1:])

    # Create directories if they do not exist
    export_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__))) + "/export/"
    config_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__))) + "/config/"
    current_date = datetime.datetime.now().strftime("%Y%m%d")

    if not os.path.exists(export_path):
        os.makedirs(export_path)
        print(f"{datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')} - INFO - The directory '{export_path}' has been created")
    if not os.path.exists(config_path):
        os.makedirs(config_path)
        print(f"{datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')} - INFO - The directory '{config_path}' has been created")

    # Read sonar config (including sonar_port)
    sonar_site, sonar_protocol, sonar_domain_name, sonar_token, sonar_port = None, None, None, None, None

    # Modified to expect sonar_port as fifth item in the returned tuple
    config_values = get_sonar_config_file(config_path + config_file)
    if len(config_values) == 5:
        sonar_site, sonar_protocol, sonar_domain_name, sonar_token, sonar_port = config_values
    else:
        # Fallback if sonar_port missing, default to 9000
        sonar_site, sonar_protocol, sonar_domain_name, sonar_token = config_values
        sonar_port = "9000"

    # Execute requested action
    if action == "export_all_sonar_users":
        export_all_sonar_users(
            sonar_site, sonar_protocol, sonar_domain_name, sonar_token, sonar_port,
            export_path + f"{current_date}-sonar-users-{sonar_site}.csv"
        )

    elif action == "export_all_sonar_groups_and_members":
        groups_list = export_all_sonar_groups(
            sonar_site, sonar_protocol, sonar_domain_name, sonar_token, sonar_port,
            export_path + f"{current_date}-sonar-groups-{sonar_site}.csv"
        )
        export_all_sonar_groups_members(
            sonar_site, sonar_protocol, sonar_domain_name, sonar_token, sonar_port, groups_list,
            export_path + f"{current_date}-sonar-groups-members-{sonar_site}.csv"
        )

    elif action == "export_all_sonar_projects_with_metrics":
        projects_list = export_all_sonar_projects(
            sonar_site, sonar_protocol, sonar_domain_name, sonar_token, sonar_port,
            export_path + f"{current_date}-sonar-projects-{sonar_site}.csv"
        )
        export_all_sonar_projects_metrics(
            sonar_site, sonar_protocol, sonar_domain_name, sonar_token, sonar_port, projects_list,
            export_path + f"{current_date}-sonar-projects-metrics-{sonar_site}.csv"
        )
        export_all_sonar_projects_quality_gates(
            sonar_site, sonar_protocol, sonar_domain_name, sonar_token, sonar_port, projects_list,
            export_path + f"{current_date}-sonar-projects-quality-gates-{sonar_site}.csv"
        )

    elif action == "export_all_sonar_projects_analyses":
        projects_list = get_all_sonar_projects(
            sonar_site, sonar_protocol, sonar_domain_name, sonar_token, sonar_port
        )
        export_all_sonar_projects_analyses(
            sonar_site, sonar_protocol, sonar_domain_name, sonar_token, sonar_port, projects_list,
            export_path + f"{current_date}-sonar-projects-analyses-{sonar_site}.csv"
        )
        export_all_sonar_projects_analyses_qg(
            sonar_site, sonar_protocol, sonar_domain_name, sonar_token, sonar_port, projects_list,
            export_path + f"{current_date}-sonar-projects-analyses-qg-{sonar_site}.csv"
        )

    elif action == "export_all_sonar_projects_analyses_metrics":
        export_all_sonar_projects_analyses_metrics(
            sonar_site, sonar_protocol, sonar_domain_name, sonar_token, sonar_port,
            export_path + f"{current_date}-sonar-analyses-metrics-{sonar_site}.csv"
        )
    else:
        print(f"{datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')} - ERROR - Unknown action '{action}'")
