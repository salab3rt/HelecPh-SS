import json, os

class UserCoordProfile:
    
    def __init__(self):
        self.profiles = self.load_profiles()
        self.current_profile = next(iter(self.profiles.get('profiles', {}).values()), None)

        #print(self.current_profile)
        
    def load_profiles(self):
        profiles_file = "profiles.json"
        if os.path.exists(profiles_file):
            with open(profiles_file, "r") as file:
                profiles_dict = json.loads(file.read())
                #print(profiles_dict['profile'])
                return profiles_dict
        else:
            init_profiles = {"profiles":{}}
            with open(profiles_file, "w") as file:
                json.dump(init_profiles, file)
                
        return self.load_profiles()

    def save_profile(self, profile_name, profile_data):
        profiles_file = "profiles.json"

        profiles = self.load_profiles()
        profiles['profiles'][profile_name] = profile_data

        with open(profiles_file, "w") as file:
            json.dump(profiles, file)
            

    
        
    