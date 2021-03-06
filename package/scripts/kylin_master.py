import os
import base64
from time import sleep
from resource_management import *

class KylinMaster(Script):
    
    def install(self, env):      
        import params
        self.install_packages(env)
        Directory([params.install_dir],
              mode=0755,
              cd_access='a',
              create_parents=True
        )
        Execute('cd ' + params.install_dir + '; wget --no-check-certificate ' + params.downloadlocation + ' -O kylin.tar.gz  ')
        Execute('cd ' + params.install_dir + '; wget --no-check-certificate https://repo1.maven.org/maven2/com/google/guava/guava/28.0-jre/guava-28.0-jre.jar -O guava-28.0-jre.jar ')
	
	Execute('cd ' + params.install_dir + '; tar -xvf kylin.tar.gz')
        Execute('cd ' + params.install_dir + ';rm -rf latest; ln -s apache-kylin* latest')
	Execute('cd ' + params.install_dir + ';chown hdfs:hadoop -R apache-kylin* ')
	Execute('cd ' + params.install_dir + '; cp guava-28.0-jre.jar latest/tomcat/lib/guava-28.0-jre.jar;cp guava-28.0-jre.jar latest/tool/guava-28.0-jre.jar' )
	Execute('cd ' + params.install_dir + '; cd latest; mkdir /var/log/kylin;  rm -f logs;   ln -s /var/log/kylin logs; chown -R hdfs:hadoop /var/log/kylin ')
	Execute('cd ' + params.install_dir + '; cd latest/tomcat; mkdir /var/log/kylin/tomcat; rm -f logs; ln -s /var/log/kylin/tomcat logs ; chown -R hdfs:hadoop /var/log/kylin ' )
        
        #mkdir
        Execute('sudo -uhdfs hadoop fs -mkdir -p /kylin')
        Execute('sudo -uhdfs hadoop fs -chown -R kylin:kylin /kylin')
                

    def configure(self, env):  
        import params
        params.server_mode="all"
        env.set_params(params)
        kylin_properties = InlineTemplate(params.kylin_properties)   
        File(format("{install_dir}/latest/conf/kylin.properties"), content=kylin_properties)
	kylin_hive_conf=params.service_packagedir+'/configuration/kylin_hive_conf.xml'
	File(format("{install_dir}/latest/conf/kylin_hive_conf.xml"), content= kylin_hive_conf)
        find_hive_dependency=params.service_packagedir+'/configuration/find-hive-dependency.sh'
	File(format("{install_dir}/latest/bin/find-hive-dependency.sh"), content= find_hive_dependency )
	
        File(format("{tmp_dir}/kylin_init.sh"),
             content=Template("init.sh.j2"),
             mode=0o700
             )        
        File(format("{tmp_dir}/kylin_env.rc"),
             content=Template("env.rc.j2"),
             mode=0o700
             )              
        Execute(format("bash {tmp_dir}/kylin_init.sh"))
             
    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute(format(". {tmp_dir}/kylin_env.rc;su hdfs {install_dir}/latest/bin/kylin.sh start"))
        sleep(5)
        Execute("ps -ef | grep java | grep kylin | grep -v grep | awk '{print $2}' >"+format("{install_dir}/latest/pid"))
        Execute(format("rm -rf /var/run/kylin.pid;cp {install_dir}/latest/pid /var/run/kylin.pid"))
		
		
        

    def stop(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute(format(". {tmp_dir}/kylin_env.rc;su hdfs {install_dir}/latest/bin/kylin.sh stop"))


    def restart(self, env):
        self.stop(env)
        self.start(env)

    def status(self, env):
        check_process_status("/var/run/kylin.pid")


if __name__ == "__main__":
    KylinMaster().execute()
