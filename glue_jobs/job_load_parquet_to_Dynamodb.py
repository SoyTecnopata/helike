import sys

from pyspark.sql.session import SparkSession
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import col
from pyspark.sql.functions import concat, lit

class BucketToDynamodb:
    def __init__(self):
        builder = SparkSession.builder
        self.spark = builder.getOrCreate()
        self.context = GlueContext(self.spark)

    def run(self):
        dynamicFrame = self.context.create_dynamic_frame.from_options(
            connection_type = "s3", 
            connection_options = {"paths": ["s3://google-sheets-input/input/clients_to_contact.parquet"]}, 
            format = "parquet"
        )
        dynamicFrame = dynamicFrame.resolveChoice(specs = [('cedula_identificacion','cast:String')])
        df = dynamicFrame.toDF()
        
        print(df.show())
        print(df.printSchema())
        
        df = df.withColumn('celular', concat(lit("+"), col('celular')))
        dynamicFrame= DynamicFrame.fromDF(df, self.context, "google_dyn")
        print(dynamicFrame.toDF().show())
        print(dynamicFrame.toDF().printSchema())

        self.context.write_dynamic_frame_from_options(
            frame=dynamicFrame,
            connection_type="dynamodb",
            connection_options={
            "dynamodb.output.tableName": "pulsar_retargeting"})
            
        self.context.purge_s3_path("s3://google-sheets-input/input/", options={}, transformation_ctx="")
        print("Done")

if __name__ == "__main__":
    BucketToDynamodb().run()
