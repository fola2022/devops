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

    response = ec2_client.describe_snapshots(Filters=[{'Name':'tag:CreatedBy','Values':['ec2-automated-backup']},{'Name':'tag-key','Values':['ExpiresOn']}])
    #print(response)

    counter = 0
    totalcount = 0
    for snapshot in response['Snapshots']:
        for tag in snapshot['Tags']:
            if tag['Key'] == 'ExpiresOn':
                # Try and convert the string into a datetime object for evaluation
                try:
                    expires = datetime.datetime.strptime(tag['Value'], '%Y-%m-%d')
                    # For debugging
                    #print(expires)
                except:
                    print('Error: Unexpected value in ExpiresOn. Snapshot Id: ' + snapshot['SnapshotId'])
                    print('Value in ExpiresOn expects a date string of YYYY-MM-DD. Skipping until fixed.')
                    # use some rediculusly future date for comparison because we do not want to assume a date
                    expires = datetime.datetime(3999, 12, 31 )
                if expires <= today:
                    print('---')
                    print('Snapshot: ' + snapshot['SnapshotId'] + ' has expired. Cleaning up snapshot ...')
                    print('    ' + str(snapshot['Tags']))
                    try:
                        delete_response = ec2_client.delete_snapshot(SnapshotId = snapshot['SnapshotId'])
                        print('Snapshot: ' + snapshot['SnapshotId'] + ' has been deleted')
                        counter += 1
                    except ClientError as e:
                        image_response = ec2_client.describe_images(Filters=[{'Name':'block-device-mapping.snapshot-id','Values':[snapshot['SnapshotId']]}])
                        if len(image_response['Images']) > 0:
                            print('ERROR: Snapshot was not deleted because it is part of an AMI. ImageId: ' + image_response['Images'][0]['ImageId'])
                            print('    To Resolve: Remove CreatedBy and ExpiresOn tags from this snapshot or deregister the image')
                        else:
                            print('Unexpected error: %s' % e)
                    except e:
                        print('Unknown error deleting snapshot: ' + snapshot['SnapshotId'] )
                        print(e)
                    totalcount += 1
                    print()
    print('Number of snapshots successfully deleted: ' + str(counter))
    print('Total number of snapshots evalutated for deletion: ' + str(totalcount))
    print()