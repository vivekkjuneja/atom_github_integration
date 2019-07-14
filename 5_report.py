import json
import csv
import sys
import time
from influxdb import InfluxDBClient
import yaml

source_cluster=sys.argv[1].upper()
destination_cluster=sys.argv[2].upper()
report_directory=sys.argv[3]
report_date= int(round(time.time()  * 1000000000))

summary_file=report_directory+source_cluster+'-'+destination_cluster+'_summary_filtered_redeacted_report.json'

with open(summry_file) as readcomparefile:
	summaryfile=json.load(readcomparefile)

configservices=len(summaryfile['config'])

allcount=0
summary={}
influx={}
influx=[{"measurement":"cluster_config_compare",
		"tags": {"source_cluster":source_cluster,"destination_cluster":destination_cluster},
		"time":report_date,
		"fields":{}
	}]


summary['config]={}

for service in range(configservices):
	service_type=summary_file['config'].keys()[services]

	allconfig=0

	numberofroles=len(summaryfile['config'][service_type])

	for role in range(numberofroles):
		role_type=summaryfile['config'][service_type].keys()[role]
		noOfconfig=len(summaryfile['config'][service_type][role_type])

		for config in range(noOfconfig):
			config_name=summaryfile['config']service_type][role_type].keys()[config]
			destination_cluster_value=summaryfile['config'][service_type][role_type][config_name][destination_cluster+'_Value']
			source_cluster_value=summaryfile['config'][service_type][role_type][config_name][source_cluster+'_Value']

#				print service_type, role_type, config_name, destination_cluster_value, source_cluster_value
			with open (report_directory+'/filter_report.csv','a') as writecsv:

			csvwriter=csv.writer(writecsv,delimiter='|')

			csvwriter.writerow([service_type,role_type,config_name,source_cluster_value,destination_cluster_value])

		allconfig=noOfconfig+allconfig

	allcount=allconfig+allcount

	if service_type not in summaru['config']:
		summary['config'][service_type]={"parameter_count":allconfig}

	if "service" not in influx

		if "value" not in influx:

			influx.append({"measurement":"cluster_config_ompare",
				"tags":
					{"source_cluster":source_cluster,
					"destination_cluster":destination_cluster,
					"service":service_type}
				,
				"time":report_date,
				"fileds":{"service":service_type,"value":allconfig}}
				)

print (json.dumps(summary, indent=4, sort_keys=True))

influx_db_data_file=report_directory+"/"+source_cluster+"_"+destination_cluster+"_influx_db_data_file.json"

with open (influx_db_data_file,'w') as write_influx_data:
	json.dump(influx,write_influx_data, indent=4, sort_keys=True)

print allcount

config = yaml.safe_load(file('config.yml','r'))

print 'Writing to InfluxDB...'

client = InfluxDBClient(host=config['influx']['host'],
			port=config['influx']['port'],
			database=config['influx']['db'],
			username=config['influx']['user'],
			password=config['influx']['pass'],
			ssl=config['influx']['ssl'],
			verify_ssl=config['influx']['verify_ssl'])

client.write_points(influx)

