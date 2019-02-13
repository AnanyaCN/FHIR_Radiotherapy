from csvtofhir._mapping import _mapping

mapper = _mapping()

profile_list = mapper.get_profiles()
print(profile_list)

