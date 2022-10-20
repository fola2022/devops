import json
import boto3
import datetime
import calendar
from datetime import date
from botocore.exceptions import ClientError, WaiterError

def lambda_handler(event, context):
    # Initialize an ec2 client
    ec2_client = boto3.client('ec2')

    # Determine what day of the week it is. Start of week is Monday which equals 0
    week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    today = datetime.datetime.today()
    week_day_value = calendar.weekday(today.year, today.month, today.day)
    week_day = week[week_day_value]

    # Determine current hour and minutes and format to 0:00
    current_time = '{0}:{1:02d}'.format(today.hour, today.minute)
    current_date = '{0}-{1:02d}-{2:02d}'.format(today.year, today.month, today.day)
    
    # Used for Debugging
    print('Current Date/Time is: ' + str(today))

    # Find all instances with the Backup tag
    response = ec2_client.describe_instances(Filters=[{'Name':'tag:Backup','Values':['yes']}])

    if response['Reservations']:
        # Loop over each instance
        for instances in response['Reservations']:
            for instance in instances['Instances']:
                # For debugging
                print(instance['InstanceId'])
                retention_days_found = False
                # Modify existing tags
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        hostname = tag['Value']
                        tag['Key'] = 'HostName'
                    if tag['Key'] == 'CreatedBy':
                        host_created_by = tag['Value']
                        tag['Key'] = 'HostCreatedBy'
                    if tag['Key'].startswith('aws:'):
                        tag['Key'] = 'internal:' + tag['Key']
                    # Update the number of days snapshot should live
                    if tag['Key'] == 'BackupRetentionDays':
                        try:
                            expire_number_days = int(tag['Value'])
                            retention_days_found = True
                        except:
                            print('Error: ' + instance['InstanceId'] + ' has a bad value for BackupRentionDays. Current Value ' + tag['Value'])
                            print('Expecting value to be an integer. Defaulting to default number of days.')
                            # Add an error tag
                            error_tag = { 'Key':'RetentionError', 'Value':'BackupRentionDays value should be only a whole number.' }
                            instance['Tags'].append(error_tag)
                if not retention_days_found:
                    expire_number_days = 30
        
                # Create new global tag Key Value pairs for the instance
                future_datetime = today + datetime.timedelta(expire_number_days)
                expires = '{0}-{1:02d}-{2:02d}'.format(future_datetime.year, future_datetime.month, future_datetime.day)
                expires_date = { 'Key':'ExpiresOn', 'Value':expires }
                create_date = { 'Key':'CreatedOn', 'Value':current_date }
                create_by = { 'Key':'CreatedBy', 'Value':'ec2-automated-backup' }
                number_volumes = { 'Key':'NumberofVolumes', 'Value':str(len(instance['BlockDeviceMappings'])) }

                # Append new global tags
                instance['Tags'].append(expires_date)
                instance['Tags'].append(create_date)
                instance['Tags'].append(create_by)
                instance['Tags'].append(number_volumes)

                # Remove backup tag key value pair
                back_up = { 'Key':'Backup', 'Value':'yes' }
                instance['Tags'].remove(back_up)

                # Loop through the volumes and create specific tags and the snapshot for each volume
                for index, volume in enumerate(instance['BlockDeviceMappings'], 1):
                    print(volume['Ebs']['VolumeId'], hostname, volume['DeviceName'], current_date)
                    device_name = { 'Key':'DeviceName', 'Value':volume['DeviceName'] }
                    volume_id = volume['Ebs']['VolumeId']
                    description = hostname + '_' + volume['DeviceName'] + '_' + current_date
                    snapshot_name = { 'Key':'Name', 'Value':description }

                    if index == 1:
                        # Append new volume specific tags
                        instance['Tags'].append(device_name)
                        instance['Tags'].append(snapshot_name)
                        # These varialbes will be used to remove the appended value should there be another volume
                        previous_device_name = device_name
                        previous_snapshot_name = snapshot_name
                    else:
                        # Remove previous values before appending new value
                        instance['Tags'].remove(previous_device_name)
                        instance['Tags'].remove(previous_snapshot_name)
                        # Append new volume specific tags
                        instance['Tags'].append(device_name)
                        instance['Tags'].append(snapshot_name)
                        # These varialbes will be used to remove the appended value should there be another volume
                        previous_device_name = device_name
                        previous_snapshot_name = snapshot_name
            
                    tags = instance['Tags']
                    # For debugging
                    #print(json.dumps(tags, indent = 4))

                    # Create Snapshot for the volume
                    snapshot_response = ec2_client.create_snapshot(Description = description, VolumeId = volume_id, TagSpecifications = [{'ResourceType':'snapshot','Tags': tags}])
                    print(snapshot_response)
                print()

    else:
        print('No instances tagged to be backup up.')