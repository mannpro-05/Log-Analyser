import json
import os
print( os.listdir())
mail_server = input("Enter your SMTP outgoing mail server: ")
portNumber = input("Enter your outgoing port number: ")
username = input("Enter your outgoing username: ")
numbers = [1,2]
ssl_value = ["True", "False"]
while True:
    use_ssl = int(input("Does your mail server use SSL:\n1.Yes\n2.No\n:"))
    password = input('Password: ')
    cpassword = input('Confirm Password: ')

    if password == cpassword and (len(password)!=0) and (use_ssl in numbers):
        with open('modules/config.json') as file:
            config_data = json.load(file)
            config_data["MAIL_SERVER"] = mail_server
            config_data["MAIL_PORT"] = portNumber
            config_data["MAIL_USE_SSL"] = ssl_value[use_ssl-1]
            config_data["MAIL_USERNAME"] = username
            config_data["MAIL_PASSWORD"] = password
            with open('modules/config.json', 'w') as configFile:
                json.dump(config_data, configFile)
                configFile.close()
            file.close()
        break
    else:
        print('Please check the password or the SSL options again!!!')