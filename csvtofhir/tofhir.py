import pandas
from csvtofhir._mapping import _mapping

class radData:

    def parse_csv(self,csvfile):

        #Read Data from csv file
        data = pandas.read_csv(csvfile)
        header_list = list(data)

        #List available profiles
        datamap = _mapping()

        #print(datamap.get_profiles())
        datamap.default_map(header_list,profile_set=datamap.get_profiles())




# from csvtofhir._mapping import _mapping
#
# mapper = _mapping()
#
# profile_list = mapper.get_profiles()
# print(profile_list)

