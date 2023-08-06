import json

class Information():
    def __init__(self):
        pass
    def load(self):
        pass
    def save(self):
        pass
  

detail = {'user':'',
          'place':'',
          'city': '',
          'country':'',
          'provider':'',
          'email_1':'',
          'email_2':'',
          'first_name':'',
          'last_name':'',
          }
persons= {'user_0':detail}
          
          


    
if __name__ == "__main__":
    print(persons)
    with open('profile.json', 'w') as fp:
        json.dump(persons, fp, sort_keys=True, indent=4)
    
    with open('profile.json', 'r') as infile:
        data = json.load(infile)
    print('from file',data)
              