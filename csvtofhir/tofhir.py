import pandas
from csvtofhir._mapping import _mapping
from csvtofhir import csvtofhir
import os
import csv
import io
import sys
import csv
import logging
from datetime import datetime
from collections import OrderedDict
import jinja2
from flask import Flask, render_template
import requests

class radData:

    # def parse_csv(self,csvfile):
    #
    #     #Read Data from csv file
    #     data = pandas.read_csv(csvfile)
    #     header_list = list(data)
    #
    #     #List available profiles
    #     datamap = _mapping()
    #
    #     #print(datamap.get_profiles())
    #     datamap.default_map(header_list,profile_set=datamap.get_profiles())

    def convert(self, csvfile):

        this = os.getcwd()
        keys = ['pat_id', 'gender', 'birthDate', 'deceasedBoolean', 'stage', 'ecog', 'ecogText', 'smok_stat', 'smok-statText']
        fhirDict = OrderedDict().fromkeys(keys, None)


        def populate_Data(data, fhirDict):
            # Get Patient Information
            fhirDict['pat_id'] = data['study_id']
            if data['gender'] == '1':
                fhirDict['gender'] = 'male'
            elif data['gender'] == '2':
                fhirDict['gender'] = 'female'
            else:
                fhirDict['gender'] = 'Unknown'
            fhirDict['birthDate'] = year = datetime.now().year - int(float(data['age']))
            if data['deadstat'] == '1':
                fhirDict['deceasedBoolean'] = 'true'
            else:
                fhirDict['deceasedBoolean'] = 'false'
            # Get the Condition/ Stage Information
            if data['stage'] == '1':
                fhirDict['stage'] = 'III A'
            elif data['stage'] == '2':
                fhirDict['stage'] = 'III B'
            else:
                fhirDict['stage'] = 'Not Specified'
            # Observation - ECOG Performance Status
            if data['who3g'] == '0':
                fhirDict['ecog'] = 'C105722'
                fhirDict['ecogText'] = 'Ecog Performance Status 0'
            elif data['who3g'] == '1':
                fhirDict['ecog'] = 'C105723'
                fhirDict['ecogText'] = 'Ecog Performance Status 1'
            elif data['who3g'] == '2':
                fhirDict['ecog'] = 'C105725'
                fhirDict['ecogText'] = 'Ecog Performance Status 2'
            elif data['who3g'] == '3':
                fhirDict['ecog'] = 'C105726'
                fhirDict['ecogText'] = 'Ecog Performance Status 3'
            elif data['who3g'] == '4':
                fhirDict['ecog'] = 'C105727'
                fhirDict['ecogText'] = 'Ecog Performance Status 4'
            elif data['who3g'] == '5':
                fhirDict['ecog'] = 'C105728'
                fhirDict['ecogText'] = 'Ecog Performance Status 5'
            else:
                fhirDict['ecog'] = 'Not Specified'
            # Observation - Smoking Status
            if data['dumsmok2'] == '1':
                fhirDict['smok_stat'] = '446172000'
                fhirDict['smok-statText']="Never/ex smoker"
            if data['dumsmok2'] == '2':
                fhirDict['smok_stat'] = '8392000'
                fhirDict['smok-statText'] = "Current Smmoker"
            else:
                fhirDict['smok_stat'] = 'Not Specified'
                fhirDict['smok-statText'] = "Not Specified"
            # Observation - BMI
            fhirDict['bmi'] = data['bmi']
            # FEV1
            fhirDict['fev1'] = data['fev1pc_t0']
            # Histology - observation
            # tstage - observation
            # nstage - observation
            # gtv - observation
            # Countpetallg
            # countpet_mediast6g
            return fhirDict


        def fhir_post_bundle(base_url, bundle):
            try:
                res = requests.post(base_url, headers={'Content-Type': 'application/json+fhir'}, data=bundle)
                res.raise_for_status()
            except Exception as e:
                logging.error("Failed; failing Bundle was:\n{}".format(bundle))
                raise e


        tpl_suffix = '-dstu3'
        tplenv = jinja2.Environment(loader=jinja2.FileSystemLoader('C:/Users/ananya.choudhury/PycharmProjects/FHIR_Radiotherapy/csvtofhir/Templates/'))
        tpl_patient = tplenv.get_template('patientRadiotherapy.json')
        tpl_condition = tplenv.get_template('Condition.json')
        tpl_obsBMI = tplenv.get_template('Observation-bmi.json')
        tpl_obsECOG = tplenv.get_template('Observation-ecog.json')
        tpl_obsFev = tplenv.get_template('Observation-fev.json')
        tpl_obsSmok = tplenv.get_template('Observation-Smok.json')
#        tpl_bundle = tplenv.get_template('bundle{}.json'.format(tpl_suffix))
        with io.open(csvfile, 'r') as CSVFile:
            rawData = csv.DictReader(CSVFile)
            head = None
            resources = []
            bundles = []
            i = 1
            push_to = None  # 'http://localhost:5000/baseDstu3/'
            bundle_per_patient = False

            print("Converting to FHIR.....")

            for row in rawData:
                data = populate_Data(row, fhirDict)

                # Patient Resources
                jsonDataPat = tpl_patient.render(pat_id=data['pat_id'], gender=data['gender'], birthDate=data['birthDate'],
                                                 deceasedBoolean=data['deceasedBoolean'])
                # Observation- BMI
                bmiid = "bmi_" + data["pat_id"]
                jsonDataObsBmi = tpl_obsBMI.render(bmi_id=bmiid, pat_id=data['pat_id'], bmi_val=data['bmi'])

                # Observation - ECOG
                ecogid = "ecog" + data["pat_id"]
                jsonDataObsEcog = tpl_obsECOG.render(obsEcog_id=ecogid, pat_id=data['pat_id'], code=data['ecog'],
                                                     disp_val=data['ecogText'])
                # Observation - FEV
                fevid = "fev" + data["pat_id"]
                jsonDataObsFev = tpl_obsFev.render(obsFev_id=fevid, pat_id=data['pat_id'], fev_val=data['fev1'])

                # Observation - smok
                smokstatid = "smokstat"+data["pat_id"]
                jsonDataObssmok=tpl_obsSmok.render(smok_id=smokstatid, pat_id = data['pat_id'],statCode =data['smok_stat'],disp_text=data['smok-statText'])

                # jsonDataCondition =tpl_condition.render()
                # resources.append(jsonDataPa


                with open("C:/Users/ananya.choudhury/PycharmProjects/FHIR_Radiotherapy/Generated/patient{}.json".format(
                        i), "w") as f:
                    f.write(jsonDataPat)


                with open("C:/Users/ananya.choudhury/PycharmProjects/FHIR_Radiotherapy/Generated/bmi{}.json".format(
                        i), "w") as f:
                    f.write(jsonDataObsBmi)


                with open("C:/Users/ananya.choudhury/PycharmProjects/FHIR_Radiotherapy/Generated/ecog{}.json".format(
                        i), "w") as f:
                    f.write(jsonDataObsEcog)

                # with open("C:/Users/ananya.choudhury/PycharmProjects/FHIR_Radiotherapy/Generated/smokstat{}.json".format(
                #         i), "w") as f:
                #     f.write(jsonDataObssmok)

                    i+=1

            print("Succesfull")



# from csvtofhir._mapping import _mapping
#
# mapper = _mapping()
#
# profile_list = mapper.get_profiles()
# print(profile_list)

