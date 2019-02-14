import os
import shutil
from collections import defaultdict

class _mapping:


    """List all profiles"""
    def get_profiles(self):
        profile_set = set()
        dir_name = os.path.dirname(__file__)+'\Templates'
        for files in os.listdir(dir_name):
            profile_set.add(os.path.splitext(files)[0])
        return profile_set

    # def default_map(self, header_list,profile_set):
    #     print("default mapping")
    #     patient_default = ['gender', 'age', 'deadstat']
    #     mapping_dict = dict.fromkeys(profile_set)
    #     count = 0
    #     for entry in header_list:
    #         if entry in patient_default:
    #             mapping_dict['patient_default'][count]==entry
    #         count+=1


       # print(mapping_dict)

    def add_profiles(self, filepath):
        print("add profiles")  # Profile names should be [base_resource]-[profile_name]  e.g. observation-bmi
                               # default profiles patient-def is added
                               # does no validation of profiles. It is assumed profiles to be addd are pre-validated
        dir_name = os.path.dirname(__file__) + '\Templates'
        shutil.move(filepath, dir_name)