sourceCluster=$1
destinationCluster=$2
report_date="$(date +"%Y%m%d")"
report_dir="../report/$report_date/"
cm_user=$3
in_host=$4
in_port=$5
db_name=$6
user_name=$7
user_pass=$8

mkdir -p $report_dir

python 1_get_data.py $sourceCluster $destinationCluster $report_dir $cm_user

python 2_consolidate.py $sourceCluster $destinationCluster $report_dir

python 3_comp_v1.py $sourceCluster $destinationCluster $report_dir

python 4_filter.py $sourceCluster $destinationCluster $report_dir

python 5_report.py $sourceCluster $destinationCluster $report_dir
