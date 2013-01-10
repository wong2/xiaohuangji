#!/bin/bash
# Help ./workers.sh num_of_workers logging_directory
PREV_WORKERS_HASH=`md5sum $0 | cut -d' ' -f1`
if [ ! -f "rqworker.py" ]; then
	echo 'workers.sh must be run in the directory of rqworker.py'
	echo '# Help ./workers.sh num_of_workers logging_directory'
	exit 1
fi
if [ -z $2 ]; then
	echo 'You must specify a logging directory'
	echo '# Help ./workers.sh num_of_workers logging_directory'
	exit 1
fi
if [ "$1" -gt "0" ]; then
	echo >/dev/null
else
	echo "The first argument must be greater than zero"
	echo '# Help ./workers.sh num_of_workers logging_directory'
	exit 1
fi
set -x
ps aux | grep rqworker | grep -v grep |  awk '{ print $2 }' | xargs kill
sleep 20
ps aux | grep rqworker | grep -v grep |  awk '{ print $2 }' | xargs kill
for ((i=1;i<=$1;i++)); do
	python -u rqworker.py -c settings 2>&1 | tee -a "$2/log.$i" | egrep "([Jj]ob|Caused)" &
done
while true; do
	git fetch >/dev/null 2>/dev/null
	CUR_WORKER_COUNT=`ps aux | grep rqworker | grep -v grep | wc -l | cut -d' ' -f 1`
	if [ "$CUR_WORKER_COUNT" -lt "$1" ]; then
		for ((i=$CUR_WORKER_COUNT;i<$1;i++)); do
			python -u rqworker.py -c settings 2>&1 | tee -a "$2/log.$i" | egrep "([Jj]ob|Caused)" &
		done
	fi
	if git status 2>/dev/null | grep origin >/dev/null; then
		NEW_WORKERS_HASH=`md5sum $0 | cut -d' ' -f1`
		if [ "$PREV_WORKERS_HASH" !=  "$NEW_WORKERS_HASH" ]; then
			bash $0 $1 $2 &
			exit 0
		fi
		ps aux | grep rqworker | grep -v grep |  awk '{ print $2 }' | xargs kill
		sleep 20
		ps aux | grep rqworker | grep -v grep |  awk '{ print $2 }' | xargs kill
		git pull >/dev/null 2>/dev/null
		for ((i=1;i<=$1;i++)); do
			python -u rqworker.py -c settings 2>&1 | tee -a "$2/log.$i" | egrep "([Jj]ob|Caused)" &
		done
	fi
	sleep 60;
done
