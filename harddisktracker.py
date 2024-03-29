import os
from pprint import pprint as pp
import csv

hddtestdatapath = "/mnt/phoenix/devcifs/hddtest/disks"
all_entries = os.listdir(hddtestdatapath)

files = [entry for entry in all_entries if not os.path.isdir(hddtestdatapath + "/" + entry)]
directories = [entry for entry in all_entries if os.path.isdir(hddtestdatapath + "/" + entry)]

drive_data = {
    'drive_name': 'Directory name in //phoenix/devcifs/hddtest/disks/',
    'test_status': 'running if badblocks.out doesnt contain "Pass completed, " else completed',
    'test_results': 'pass if "Pass completed, 0 bad blocks found. (0/0/0 errors)',

}

drive_data_list = [

]

drive_data = {}
for hddtestdir in directories:
    print("Gathering data for drive: %s" % hddtestdir)
    drive_data = {}
    drive_data['drive_name'] = hddtestdir

    # Is the test still running
    badblocks_file = hddtestdatapath + '/' + hddtestdir + '/badblocks.out'
    print("Checking badblocks file: %s" % badblocks_file)
    test_complete = False
    with open(badblocks_file) as f:
        badblocks_file_lines = f.readlines()
        for row in badblocks_file_lines:
            word = "Pass completed, "
            if word in row:
                test_complete = True
                break
        if test_complete:
            print("Test appears to be complete")
            drive_data['test_status'] = 'Complete'

            # Did badblocks pass?
            badblocks_test_passed = False
            for row in badblocks_file_lines:
                word = "Pass completed, 0 bad blocks found. (0/0/0 errors)"
                if word in row:
                    badblocks_test_passed = True
                    break
            if badblocks_test_passed:
                drive_data['badblocks_test_results'] = "Pass"
            else:
                drive_data['badblocks_test_results'] = "Fail"

            # Read the post test smart report file
            post_test_smart_file = hddtestdatapath + '/' + hddtestdir + '/post-test.smart'
            print("Checking post test smart file: %s" % post_test_smart_file)
            with open(post_test_smart_file) as f2:
                for line in f2:
                    if 'Model Family:' in line:
                        drive_data['model_family'] = line.split('Model Family:')[1]
                    if 'Device Model:' in line:
                        drive_data['device_model'] = line.split('Device Model:')[1]
                    if 'Serial Number:' in line:
                        drive_data['serial_number'] = line.split('Serial Number:')[1]
                    if 'User Capacity:' in line:
                        drive_data['capacity'] = line.split('bytes')[1].split('[')[1].split(']')[0]
                    if 'Power_On_Hours' in line:
                        drive_data['power_on_hours'] = line.split()[9]

                    if 'Raw_Read_Error_Rate' in line:
                        drive_data['raw_read_error_rate'] = line.split()[9]
                    if 'Reallocated_Sector_Ct' in line:
                        drive_data['relocated_sector_count'] = line.split()[9]

                if drive_data['raw_read_error_rate'] != '0':
                    drive_data['smart_test_results'] = 'Fail'
                else:
                    if drive_data['relocated_sector_count'] != '0':
                        drive_data['smart_test_results'] = 'Fail'
                    else:
                        drive_data['smart_test_results'] = 'Pass'

            if drive_data['badblocks_test_results'] == 'Fail' or drive_data['smart_test_results'] == 'Fail':
                drive_data['test_results'] = 'Fail'
            else:
                drive_data['test_results'] = 'Pass'
        else:
            print("Test appears incomplete")
            drive_data['test_status'] = 'Incomplete'



    drive_data_list.append(drive_data)

pp(drive_data_list)

print("Do CSV Stuff")


csv_file_name = '/mnt/phoenix/devcifs/hddtest/hddtest.csv'
fields = [
    'drive_name',
    'model_family',
    'device_model',
    'serial_number',
    'bay_number',
    'capacity',
    'power_on_hours',
    'test_status',
    'test_results',
    'badblocks_test_results',
    'smart_test_results',
    'raw_read_error_rate',
    'relocated_sector_count'
]

print(fields)
with open(csv_file_name, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)

    writer.writeheader()
    writer.writerows(drive_data_list)