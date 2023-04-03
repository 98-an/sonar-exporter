import datetime
import json
import sys, getopt
import os


def show_help():
    print("sonar-exporter is a free and open source tool intended to export some Sonarqube data,")
    print("like users, groups, projects, project metrics, and so on.")
    print()
    print("Usage: sonar-exporter.py -c <configfile> -a <action>")
    print()
    print("Mandatory arguments to long options are mandatory for short options too.")
    print("  -h, --help           Display this help and exit")
    print("  -c, --configfile     Atlassian config file or Bitbucket config file, depending on the action selected")
    print("                       configFile must be located in the ./config directory")
    print("  -a, --action         Action to be executed. Exported data will be located in the ./export directory")
    print("                       The action selected must be one of the following:")
    print()
    print("                       export_all_sonar_users")
    print("                       export_all_sonar_groups_and_members")
    print("                       export_all_sonar_projects_with_metrics")
    print()
    print("Examples:")
    print("sonar-exporter.py -c sonar_conn_mysite.json -a export_all_sonar_users")
    print("sonar-exporter.py --configfile sonar_conn_mysite.json --action export_all_sonar_groups_and_members")
    print("sonar-exporter.py --configfile=sonar_conn_mysite.json --action=export_all_sonar_projects_with_metrics")
    print()
    print("More info at: https://github.com/ElWillieES/sonar-exporter")
    print()


def get_cli_params(cli_args):
    config_file = ""
    action = ""

    try:
        opts, args = getopt.getopt(cli_args, "hc:a:", ["help", "configfile=", "action="])
    except getopt.GetoptError:
        show_help()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_help()
            sys.exit()
        elif opt in ("-c", "--configfile"):
            config_file = arg
        elif opt in ("-a", "--action"):
            action = arg

    if action != "" and action not in ("export_all_sonar_users", "export_all_sonar_groups_and_members", "export_all_sonar_projects_with_metrics"):
        print("The action specified as parameter, is not valid.")
        print()
        action = ""

    if config_file == "" or action == "":
        show_help()
        sys.exit(2)

    return config_file, action


def get_config_file(config_filename):
    print("{} - INFO - Reading config file {}".format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), config_filename))
    config = {}
    try:
        file = open(config_filename)
        config = json.load(file)
        file.close()
        return config
    except Exception as e:
        print("{} - ERROR - Error reading file {}".format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), e))
        exit()


def get_sonar_config_file(config_filename):

    config_conn = get_config_file(config_filename)
    sonar_site = config_conn["sonar-site"]
    sonar_protocol = config_conn["sonar-protocol"]
    sonar_domain_name = config_conn["sonar-domain-name"]
    sonar_token = config_conn["sonar-token"]

    return sonar_site, sonar_protocol, sonar_domain_name, sonar_token


