import json
import boto3
import os
import datetime
import calendar
from datetime import date

def lambda_handler(event, context):
    # Initialize an ec2 client
    ec2_client = boto3.client('ec2')

    # Determine what day of the week it is. Start of week is Monday which equals 0
    week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    today = datetime.datetime.today()
    week_day_value = calendar.weekday(today.year, today.month, today.day)
    week_day = week[week_day_value]

    search_time_range = int(os.environ['search_time_range'])
    begin_datetime = today - datetime.timedelta(minutes=search_time_range)

    # Determine current hour and minutes and format to 0:00
    current_time = '{0}:{1:02d}'.format(today.hour, today.minute)
    begin_time = '{0}:{1:02d}'.format(begin_datetime.hour, begin_datetime.minute)
    
    # Build the range of times to search for systems
    times = []
    for minute_count in range(0, search_time_range + 1):
        time_adjust = today - datetime.timedelta(minutes=minute_count)
        time_string = '{0}:{1:02d}'.format(time_adjust.hour, time_adjust.minute)
        mil_time_string = '{0:02d}:{1:02d}'.format(time_adjust.hour, time_adjust.minute)
        hour_string = '{0}'.format(time_adjust.hour)
        mil_hour_string = '{0:02d}'.format(today.hour)
        # For Debugging the times
        #print(time_string, mil_time_string, hour_string, mil_hour_string)
        times.append(time_string)
        if mil_time_string not in times:
            times.append(mil_time_string)
        if time_adjust.minute == 0:
            if hour_string not in times:
                times.append(hour_string)
            if mil_hour_string not in times:
                times.append(mil_hour_string)
    # Used for Debugging
    #print(times)

    # Used for Debugging
    print('Current Time is: ' + current_time)
    print('Function will check times between ' + begin_time + ' and ' + current_time + '. (Time difference is ' + str(search_time_range) + ' minutes)')

    # Query for instances that are using either the Startup or Shutdown tags. 
    # This query returns a filtered list of instances using the tag name 
    # Shutdown or Startup and has a value equal to the current time and includes
    # a prior window of time set by environement variable search_time_range
    # Tag names are case senestive
    ec2_instances_response = ec2_client.describe_instances(Filters=[{'Name': 'tag-key', 'Values': ['Shutdown', 'Startup']},{'Name': 'tag-value', 'Values': times}])

    # Used for Debugging
    #print('Number of instance groups returned from query: ' + str(len(ec2_instances_response['Reservations'])))

    # Iterate through instance response and determine what action to take
    instance_count = 0
    exclude_count = 0
    exclude_ids = []
    for instances in ec2_instances_response['Reservations']:
        for instance in instances['Instances']:
            #print(instance)
            exclude_days = ''
            shut_down = ''
            start_up = ''
            exclude = False
            # The state code will be used to determine if the action is really needed
            state_code = int(instance['State']['Code'])
            # loop through all tags on the instance
            for tag in instance['Tags']:
                if tag['Key'] == 'ExcludeDays':
                    exclude_days = tag['Value']
                    # Determine if excluded
                    if week_day in exclude_days:
                        exclude = True
                if tag['Key'] == 'Shutdown':
                    shut_down = tag['Value']
                    if not ':' in shut_down:
                        try:
                            shut_down = int(shut_down) + 0
                        except:
                            print('Shutdown value is not valid. Please supply a 24 hour time value: hh:mm')
                        shut_down = str(shut_down) + ':00'
                if tag['Key'] == 'Startup':
                    start_up = tag['Value']
                    if not ':' in start_up:
                        try:
                            start_up = int(start_up) + 0
                        except:
                            print('Startup value is not valid. Please supply a 24 hour time value: hh:mm')
                        start_up = str(start_up) + ':00'
    
            # Used for Debugging
            #print(exclude_days, shut_down,  start_up, state_code)
    
            # Check tag value to see if a shutdown is needed
            instance_id = instance['InstanceId']
            if (shut_down in times) and exclude == False:
                # State 80 : stopped
                if state_code != 80:
            
                    print('Shutting down: ' + instance_id)
            
                    # Issue a shutdown
                    action_response = ec2_client.stop_instances(InstanceIds = [instance_id])
                else:
                    print('Instance: ' + instance_id + ' is already in a stopped state')

            # Check tag values to see if a startup is needed
            if (start_up in times) and exclude == False:
                # State 16 : running
                if state_code != 16:
                    # Used for debugging
                    print('Starting up:   ' + instance_id)

                    # Issue a startup
                    try:
                        action_response = ec2_client.start_instances(InstanceIds = [instance_id])
                    except:
                        print('Error starting instance: ' + instance_id)
                else:
                    print('Instance: ' + instance_id + ' is already in a running state')


            # Counter for number of instance evaluated
            instance_count += 1
            # Counter for number of excluded instances
            if exclude == True:
                exclude_count += 1
                exclude_ids.append(instance_id)
    print('Number of instances evaluated: ' + str(instance_count))
    if instance_count > 0 and exclude_count > 0:
        print('Number of instances excluded: ' + str(exclude_count))
    if exclude_count > 0:
        print('Excluded Instance Ids: ' + str(exclude_ids))