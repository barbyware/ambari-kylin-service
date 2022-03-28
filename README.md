ambari-kylin-service
===

## To download the Kylin service folder, run below    

```
VERSION=`hdp-select status hadoop-client | sed 's/hadoop-client - \([0-9]\.[0-9]\).*/\1/'`
sudo git clone https://github.com/barbyware/ambari-kylin-service.git /var/lib/ambari-server/resources/stacks/HDP/$VERSION/services/KYLIN
```
## Restart Ambari
\#sandbox  
service ambari restart

\#non sandbox  
sudo service ambari-server restart

## Kylin install notes

https://kylin.apache.org/docs31/install/index.html

You can try download guava-28.0-jre.jar, put it into $KYLIN_HOME/tool/ and $KYLIN_HOME/tomcat/lib/ and restart kylin bin/kylin.sh restart.
## Kylin remove before reinstall

VERSION=`hdp-select status hadoop-client | sed 's/hadoop-client - \([0-9]\.[0-9]\).*/\1/'` 

rm -rf /var/lib/ambari-server/resources/stacks/HDP/$VERSION/services/KYLIN


## SUMMARY
![Image](../master/screenshots/kylin.png?raw=true)
