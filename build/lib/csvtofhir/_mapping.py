import os
import shutil

class _mapping:

    """List all profiles"""
    def get_profiles(self):
        profile_set = set()
        dir_name = os.path.dirname(__file__) + '/profiles'
        for files in os.listdir(dir_name):
            profile_set.add(os.path.splitext(files)[0])
        return profile_set

    def add_profiles(self, filepath):
        print("add profiles")  # Profile names should be [base_resource]-[profile_name]  e.g. observation-bmi
                               # default profiles patient-def is added
                               # does no validation of profiles. It is assumed profiles to be addd are pre-validated
        dir_name = os.path.dirname(__file__) + '/profiles'
        shutil.move(filepath, dir_name)