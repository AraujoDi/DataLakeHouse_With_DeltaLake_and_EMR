import boto3

def handler(event, contex):
    """
    Lambda function that starts a job flow in EMR
    """

    client = boto3.client('emr', region_name='us_east-2')

    cluster_id = client.run_job_flow(
        Name='EMR-Di-Delta',
        ServiceRole='EMR_DefaultRole',
        JobFlowRole='EMR_EC2_DefaultRole',
        VisibleToAllUsers=True,
        LogUri='s3://datalake-di-igti-edc-tf/emr-logs',
        ReleaseLabel='emr-6.3.0',
        Instances={
            'InstanceGroup': [
                {
                    'Name': 'Master nodes',
                    'Market': 'SPOT',
                    'InstanceRole': 'MASTER',
                    'InstanceType': 'm5.xlarge',
                    'InstanceCount': 1,
                },
                {
                    'Name': 'Worker nodes',
                    'Market': 'Spot',
                    'InstanceRole': 'CORE',
                    'InstanceType': 'm5.xlarge',
                    'InstanceCount': 1,
                }
            ],
            'Ec2KeyName': 'di-key-pair22',
            'KeepJobFlowAliveWhenNoSteps': True,
            'TerminationProtected': False,
            'Ec2SubnetId': 'subnet-0f74175c93bf50854'
        },

        Applications=[
            {'Name': 'Spark'},
            {'Name': 'Hive'},
            {'Name': 'Pig'},
            {'Name': 'Hue'},
            {'Name': 'JupyterHub'},
            {'Name': 'JupyterEnterpriseGateway'}
            {'Name': 'Livy'},
        ],

        Configurations=[{
            "Classification": "spark-env",
            "Properties": {},
            "Configuration": [{
                "Classification": "export",
                "Properties": {
                    "PYSPARK_PYTHON": "/usr/bin/python3",
                    "PYSPARK_DRIVER_PYTHON": "/usr/bin/python3"
                }
            }]
        },
            {
                "Classification": "spark-hive-site",
                "Properties": {
                    "hive.metastore.client.factory.class": "com.amazonaws.glue.catalog.metastore"
                }
            },
            {
                "Classification": "spark-defaults",
                "Properties": {
                    "spark.submit.deployMode": "cluster",
                    "spark.speculation": "false",
                    "spark.sql.adaptive.enebled": "true",
                    "spark.serializer": "or.apache.spark.serializer.KryoSerializer",
                }
            },
            {
                "Classification": "spark",
                "Properties": {
                    "maximizeResoureceAllocation": "true"
                }
            }
        ],

        StepConcurrencyLevel=1,

        Steps=[{
            'Name': 'Delta Insert do ENEM',
            'ActionOnFailure': 'CONTINUE',
            'HadoopJarStep': {
                'Jar': 'command-runner.jar',
                'Args': ['spark-submit',
                '--packages', 'io.delta:delta-core_2.12:1.0.0',
                '--conf', 'spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension',
                '--conf', 'spark.sql.catalog.saprk_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog',
                '--master', 'yarn',
                '--deploy-mode', 'cluster',
                's3://datalake-di-igti-edc-tf/emr-code/pyspark/01_delta_spark_insert.py'
                ]
            }
        },
        {
            'Name': 'Simulacao e UPSERT do ENEM',
            'ActionOnFailure': 'CONTINUE',
            'HadoopJarStep': {
                'Jar': 'command-runner.jar',
                'Args': ['spark-submit',
                '--packages', 'io.delta:delta-core_2.12:1.0.0',
                '--conf', 'spark.sql.extentions=io.delta.sql.DeltaSparkSessionExtension',
                '--conf', 'spark.sql.catalog.spark_catalog=org.apache.spark.delta.catalog.DeltaCatalog',
                '--master', 'yarn',
                '--deploy-mode', 'cluster',
                's3://datalake-di-igti-edc-tf/emr-code/pyspark/02_delta_spark_upsert.py'
                ]
            }
        }],
    )

return{
    'statusCode': 200,
    'body':f"Started job flow {cluster_id['JobFlowId']}"
}