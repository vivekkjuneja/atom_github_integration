
import sys
import getpass
import os
import json

source_cluster=sys.argv[1].upper()
destination_cluster=sys.argv.upper()
report_directory=sys.argv[3]
#source_cluster_username=getpass.getpass('Enter source cluster username:')
#source_cluster_user_password=getpass.getpass('Enter source cluster user\'s password:')
#destination_cluster_username=getpass.getpass('Enter destination cluster username:')
#destination_cluster_user_password=getpass.getpass('Enter destination cluster user\'s password:')
source_cluster_username='junejavk'
source_cluster_user_password='mypassword'
destination_cluster_username='junejavk'
destination_cluster_user_password='mypassword'

def get_cmlink(cluster_name,username,password):

    if cluster_name=='DS':
        cm_link="curl -k -u " +username+":"+password+"http://10.$.*.#:7180/api/v11/clusters/cluster/"

        return cm_link

    elif cluster_name=='SC':
        cm_link="curl -k -u " +username+":"+password+"http://10.#.*.$:7180/api/v11/clusters/cluster/"

        return cm_link

    else:
        print "wrong input"


def get_cluster_services(cm_link,cluster_name):

        services={}

        services[cluster_name]=[]

        getServiceData=os.popen(cmlink+"services'")

        clusterServiceData=report_directory+cluster_name+"-all_services_raw.json"

        with open(clusterServiceData, 'w') as servicedata:
            servicedata.write(getServiceData.read())

        with open(clusterServiceData) as readservicedata:
            service_data=json.load(readservicedata)

        totalNumberofServices=len(service_data['items'])

        sort_service=sorted(service_data['items'], key = lambda i: (i['type'], i['name']))

        for service in range(totalNumberofServices):
            service_type=str(sort_service[service]['type'])
            service_name=str(sort_service[service]['name'])

            if service_type not in service['cluster_name'] and service_name not in service['cluster_name']:
                services[cluster_name].append({"service_type":service_type, "service_name":service_name})

        only_cluster_services=report_directory+cluster_name+"_only_services.json"

        with open(only_cluster_services, 'w') as outfile:
            json.dump(services, outfile, indent=4, sort_keys=True)


def get_common_services(source_cluster, destination_cluster):

    SourceClusterServiceFile=report_directory+source_cluster+"_only_services.json"
    DestinationClusterServiceFile=report_directory+destination_cluster+"_only_services.json"

    with open(SourceClusterServiceFile) as source_cluster_only_services:
            source_services=json.load(source_cluster_only_services)

    sourceServiceCount=len(source_services[source_cluster])

    sortSourceServices=sorted(source_services[source_cluster], key = lambda i: (i['service_type'], i['service_name']))

    with open(DestinationClusterServiceFile) as destination_cluster_only_services:
            destination_services=json.load(destination_cluster_only_services)

    destinationServiceCount=len(destination_services[destination_cluster])

    sortDestinationServices=sorted(destination_services[destination_cluster], key = lambda i: (i['service_type'], i['service_name']))

    common_services={}
    common_services['common_service_name']=[]

    for sourceservice in range(sourceServiceCount):
        source_cluster_service_type=(str(sortSourceServices[sourceservice]['service_type']))
        source_cluster_service_name=(str(sortSourceServices[sourceservice]['service_name']))

        for destinationservice in range(destinationServiceCount):
            destination_cluster_service_type=(str(sortDestinationServices[destinationservice]['service_type']))
            destination_cluster_service_name=(str(sortDestinationServices[destinationservice]['service_name']))

        if source_cluster_service_type == destination_cluster_service_type:
            common_services['common_service_name'].append({
                    source_cluster+'_service_name':source_cluster_service_name,
                    source_cluster+'_service_type':source_cluster_service_type,
                    destination_cluster+'_service_name':destination_cluster_service_name,
                    destination_cluster+'_service_type':destination_cluster_service_type
            })

    common_service_json=report_directory+'common_services.json'

    with open(common_service_json, 'w') as commonServiceFile:
        json.dump(common_services, commonServiceFile, indent=4, sort_keys=True)

    return common_services

def get_cluster_config(cm_link,source_cluster,destination_cluster,cluster_name):

    common_services=get_common_services(source_cluster,destination_cluster)

    common_services_range=len(common_services['common_service_name'])

    cluster_common_services={}
    cluster_common_services['services']=[]

    for service in range (common_services_range):
        service_name=common_services['common_service_name'][service][cluster_name+"_service_name"]
        service_type=common_services['common_service_name'][service][cluster_name+"_service_type"]
        cluster_common_services['services'].append({
            cluster_name+'_service_name':service_name,
            cluster_name+'_service_type':service_type
        })

    unique_services=[]

    for s in cluster_common_services['services']:

        if s not in unique_services:
            unique_services.append(s)

    unique_services_range=len(unique_services)

    cluster_services_roles={}
    cluster_services_roles[cluster_name]=[]

    for cluster_service in range(unique_services_range):
        cluster_service_name=unique_services[cluster_service][cluster_name+'_service_name']
        cluster_service_type=unique_services[cluster_service][cluster_name+'_service_type']


        getServiceWideConfig=os.popen(cm_link+"services/"+cluster_service_name+"/config?view=FULL'")

        with open(report_directory+cluster_name+"-"+cluster_service_type+"-"+cluster_service_name+"-service_wide_config.json",'w') as serviceWideConfig:
            serviceWideConfig.write(getServiceWideConfig.read())

            getroles=os.popen(cm_link+"services/"+cluster_service_name+"/roleConfigGroups'")

            with open(report_directory+cluster_name+"-"+cluster_service_type+"-"+cluster_service_name+"-roles.json",'w') as getallrole:
                getallrole.write(getroles.read())

            with open(report_directory+cluster_name+"-"+cluster_service_type+"-"+cluster_service_name+"-roles.json") as roleconfigfile:
                pop_data9=json.load(roleconfigfile)

                rolerangelen=len(pop_data9['items'])

                sort_roles=sorted(pop_data9['items'], key = lambda x:(x['name']))

                for r in range(rolerangelen):
                    role_name=(str(sort_roles[r]['name']))
                    role_type=(str(sort_roles[r]['roleType']))

                    cluster_services_roles[cluster_name].append({
                        'service_type':cluster_service_type,
                        'service_name':cluster_service_name,
                        'service_wide_config_file':report_directory+cluster_name+"-"+cluster_service_type+"-"+cluster_service_name+"-service_wide_config.json",
                        'role_type':(str(sort_role[r]['roleType'])),
                        'role_name':(str(sort_roles[r]['name'])),
                        'role_config_file':report_directory+cluster_name+"-"+cluster_service_type+"-"+role_type+"-"+role_name+"-config.json"
                    })

                    roleconfiglen=len(pop_data9['items'][r]['config']['items'])

                    for rc in range(roleconfiglen):
                        getRoleConfigs=os.popen(cmlink+"services/"+cluster_service_name+"/roleConfigGroups/"+role_name+"/config?view=FULL'")

                        with open(report_directory+cluster_name+"-"+cluster_service_type+"-"+role_type+"-config.json", 'w') as roleconfigfile:
                            roleconfigfile.write(getRoleConfigs.read())

    cluster_role_meta=report_directory+cluster_name+"-all_roles_meta.json"

    with open(cluster_role_meta, 'w') as roleoutfile:
        json.dump(cluster_services_roles, roleoutfile, indent=4, sort_keys=True)

        return cluster_services_roles


def get_role_config(cluster_name):

    diff={}
    diff['config']={}

    servicefile=report_directory+'common_services.json'
    meta_file=report_directory+cluster_name+"-all_roles_meta.json"

    with open(servicefile) as servicedata:
        serviceread=json.load(servicedata)

    numberofsevices=len(serviceread['common_service_name'])

    with open(meta_file) as metafile:
        metaread=json.load(metafile)

    numberofmetadata=len(metaread[cluster_name])

    for service in range(numberofsevices):
        service_type=serviceread['common_service_name'][service][cluster_name+'_service_type']
        service_name=serviceread['common_service_name'][service][cluster_name+'_service_name']

        if service_type not in diff['config']:
            diff['config'][service_type]={}

        for meta in range(numberofmetadata):
            meta_service_type=metaread[cluster_name][meta]['service_type']

            if meta_service_type==service_type:
                meta_role_type=metaread[cluster_name][meta]['role_type']
                meta_role_name=metaread[cluster_name][meta]['role_name']
                meta_role_config_file=metaread[cluster_name][meta]['role_config_file']

                if meta_role_type not in diff['config']['service_type']:
                    diff['config']['service_type'][meta_role_type]=[]

                try:

                    with open(meta_role_config_file) as roleconfigdata:
                        roledata=json.load(roleconfigdata)

                except Exception:
                    continue

                numberofroleconfig=len(roledata['items'])

                for roleconfig in range(numberofroleconfig):
                    role_config_parameter=roledata['items'][roleconfig]['name']

                    if "value" in roledata['items'][roleconfig]:
                        role_config_value=roledata['items'][roleconfig]['value']

                        if (
                            role_config_paramater not in diff['config'][service_type][meta_role_type] and
                            role_config_value not in diff['config'][service_type][meta_role_type]
                        ):
                            diff['config'][service_type][meta_role_type].append({
                                "parameter":role_config_parameter,
                                "value":role_config_value
                            })
                    else:

                        role_config_value='default'

                        if (
                            role_config_parameter not in diff['config'][service_type][meta_role_type] and
                            role_config_value not in diff['config'][service_type][meta_role_type]
                        ):
                            diff['config'][service_type][meta_role_type].append({
                                "parameter":role_config_parameter,
                                "value":role_config_value
                            })

    cluster_role_config_data=report_directory+cluster_name+"_role_config_data.json"

    with open (cluster_role_config_data, 'w') as clusterconfigdatafile:
        json.dump(diff, clusterconfigdatafile, indent=4, sort_keys=True)



#####Calling Function
source_cm_link=get_cmlink(source_cluster,source_cluster_username,source_cluster_user_password)

destination_cm_link=get_cmlink(destination_cluster,destination_cluster_username,destination_cluster_user_password)

get_cluster_services(source_cm_link,source_cluster)

get_cluster_services(destination_cm_link,destination_cluster)

get_common_services(source_cluster,destination_cluster)

get_cluster_config(source_cm_link,source_cluster,destination_cluster,source_cluster)

get_cluster_config(destination_cm_link,source_cluster,destination_cluster,destination_cluster)

get_role_config(source_cluster)

get_role_config(destination_cluster)
