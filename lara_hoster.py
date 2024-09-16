import os
import random
import subprocess
import string
from tabulate import tabulate



def node_newdomain(domain,port):
    os.system('sudo mkdir /var/www/html/'+str(domain))
    os.system('sudo chown -R www-data:www-data /var/www/html/'+str(domain))
    config='''

    server{
    listen 80;
    server_name '''+domain+''';
    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_pass http://127.0.0.1:'''+port+''';
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        # location /overview {
        #     proxy_pass http://127.0.0.1:'''+port+'''$request_uri;
        #     proxy_redirect off;
        # }
    }
    }'''
    f=open('/etc/nginx/sites-available/'+domain+'.conf','w')
    f.write(config)
    f.close()
    os.system('sudo ln -s /etc/nginx/sites-available/'+domain+'.conf /etc/nginx/sites-enabled/'+domain+'.conf')
    os.system('sudo systemctl restart nginx')

    print("\033[32m[!] Everything done, but if you encounter any permission problems, run this command.\033[0m")

    print("\033[38;5;214m\033[1m[!] chown -R www-data:www-data /var/www/html/" + domain + "\033[0m")


def install_nginx():
    os.system('sudo apt-get update')
    os.system('sudo apt-get install nginx -y')
    print("\033[32mnginx installed successfully!\033[0m")

def install_mysql():
    os.system('sudo apt-get update')
    os.system('sudo apt-get install mysql-server -y')
    os.system('sudo systemctl start mysql.service')
    os.system('sudo mysql_secure_installation')
    os.system('sudo systemctl start mysql.service')
    print("\033[32m[!] Mysql installed successfully!\033[0m")

def install_mariadb():
    os.system('sudo apt-get update')
    os.system('sudo apt-get install mariadb-server -y')
    os.system('sudo systemctl start mariadb.service')
    os.system('sudo mysql_secure_installation')
    os.system('sudo systemctl start mariadb.service')
    print("\033[32m[!] mariadb installed successfully!\033[0m")

def install_nvm():

    print("[+] Installing NVM...")


    
    subprocess.run('curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.4/install.sh | bash', shell=True, check=True)

    
    print("=====================================")
    print("\033[31m\033[1mcopy above message and paste it in your terminal\n\033[0m")

    print(f"to install long term release type \033[33m\033[1mnvm install --lts\033[0m")
    print(f"to install a specific version of Node.js type \033[33m\033[1mnvm install (version)\033[0m")

    print("=====================================")

    
    exit()



def install_php_composer():
    version = input('[+] please type php version for example 8.2 >> ')or '8.2'
    os.system('sudo apt-get update')
    os.system('sudo apt-get install software-properties-common -y')
    os.system('sudo add-apt-repository ppa:ondrej/php -y')
    if version =='8.2':
        os.system('sudo apt-get install php8.2 php8.2-mbstring php8.2-gettext php8.2-zip php8.2-fpm php8.2-curl php8.2-mysql php8.2-gd php8.2-cgi php8.2-soap php8.2-sqlite3 php8.2-xml php8.2-redis php8.2-bcmath php8.2-imagick php8.2-intl -y')  
    else:
        os.system('sudo apt-get install php'+version+' php'+version+'-mbstring php'+version+'-gettext php'+version+'-zip php'+version+'-fpm php'+version+'-curl php'+version+'-mysql php'+version+'-gd php'+version+'-cgi php'+version+'-soap php'+version+'-sqlite3 php'+version+'-xml php'+version+'-redis php'+version+'-bcmath php'+version+'-imagick php'+version+'-intl -y')
    os.system('sudo sudo apt-get install git composer -y')
    
    print("\033[32mcomposer and php installed successfully!\033[0m")

def lara_add_new_domain(domain,php_verion):
    os.system('sudo mkdir /var/www/html/'+str(domain))
    os.system('sudo chown -R www-data:www-data /var/www/html/'+str(domain))
    confx ='''

    server {
        listen 80;
        server_name '''+domain+''';
        root /var/www/html/'''+domain+'''/public;

        add_header X-Frame-Options "SAMEORIGIN";
        add_header X-Content-Type-Options "nosniff";

        index index.php;

        charset utf-8;

        location / {
            try_files $uri $uri/ /index.php?$query_string;
        }

        location = /favicon.ico { access_log off; log_not_found off; }
        location = /robots.txt  { access_log off; log_not_found off; }

        error_page 404 /index.php;

        location ~ \.php$ {
            fastcgi_pass unix:/var/run/php/php'''+php_verion+'''-fpm.sock;
            fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
            include fastcgi_params;
        }

        location ~ /\.(?!well-known).* {
            deny all;
        }
    }
    '''


    f=open('/etc/nginx/sites-available/'+domain+'.conf','w')
    f.write(confx)
    f.close()
    os.system('sudo ln -s /etc/nginx/sites-available/'+domain+'.conf /etc/nginx/sites-enabled/'+domain+'.conf')
    os.system('sudo systemctl restart nginx')

    print("\033[32m[!] Everything done, but if you encounter any permission problems, run this command.\033[0m")

    print("\033[38;5;214m\033[1m[!] chown -R www-data:www-data /var/www/html/" + domain + "\033[0m")




def remove_domain(domain):
    
    os.system('sudo rm -r /var/www/html/'+str(domain))
    os.system('sudo rm /etc/nginx/sites-available/'+domain+'.conf')
    os.system('sudo rm /etc/nginx/sites-enabled/'+domain+'.conf')
    os.system('sudo systemctl restart nginx')
    print('[!] now the '+domain+' is deleted !')


def create_database(db_name,db_user,db_password,root_pw):
    
    try:
        import mysql.connector
    except Exception:
        print('mysql-connector-python library not found. Please install it by: pip3 install mysql-connector-python')
        install = input('Do you want to install this library for you? (Y or N) >> ')
        if install == "Y" or install == 'y':
            os.system("sudo apt update")
            os.system('sudo apt-get install python3-pip -y')
            os.system('pip3 install mysql-connector-python')
            os.system('pip3 install mysql-connector-python --break-system-packages')
            import mysql.connector

        else:
            exit()
    # Connect to MySQL as root without a password
    
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password=root_pw  # passowrd comes to here
    )
    try:

        cursor = connection.cursor()
    except Exception as e:
        print("[!] can not connect to Mysql check your root password")
        exit()
    # SQL queries
    create_database_query = f"CREATE DATABASE IF NOT EXISTS {db_name};"
    create_user_query = f"CREATE USER IF NOT EXISTS {db_user}@'localhost' IDENTIFIED BY '{db_password}';"
    grant_privileges_query = f"GRANT ALL PRIVILEGES ON {db_name}.* TO {db_user}@'localhost';"
    flush_privileges_query = "FLUSH PRIVILEGES;"

    ORANGE = "\033[38;5;214m"  # Orange color
    RESET = "\033[0m"  # Reset color
    BOLD = "\033[1m"
    data = [
        [f"{BOLD}Host:{RESET}", "127.0.0.1"],
        [f"{BOLD}Database Name:{RESET}", db_name],
        [f"{BOLD}Database Username:{RESET}", db_user],
        [f"{BOLD}Database Password:{RESET}", db_password]
    ]
    print(f"{ORANGE}{BOLD}database successfully created{RESET}")
    print(tabulate(data, tablefmt="grid"))
    


    # Execute SQL queries
    cursor.execute(create_database_query)
    cursor.execute(create_user_query)
    cursor.execute(grant_privileges_query)
    cursor.execute(flush_privileges_query)
    # Commit changes
    connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()    

os.system('clear')

def banner():
        
    print('''

    
    ░█─── ─█▀▀█ ░█▀▀█ ─█▀▀█ 　 ░█─░█ █▀▀█ █▀▀ ▀▀█▀▀ █▀▀ █▀▀█ 
    ░█─── ░█▄▄█ ░█▄▄▀ ░█▄▄█ 　 ░█▀▀█ █──█ ▀▀█ ──█── █▀▀ █▄▄▀ 
    ░█▄▄█ ░█─░█ ░█─░█ ░█─░█ 　 ░█─░█ ▀▀▀▀ ▀▀▀ ──▀── ▀▀▀ ▀─▀▀

    V2
    automaicaly host your Project  !

    from FD

    github.com/FDX100

    ====================================
    We are recommending that you .\n\trun this tool as the \033[31mroot\033[0m user.
    ====================================''')

    print('''
    1 => add or remove domains
    2 => install server and requirements    
    other key to exit
        ''')

def guide_msg():


    try:
            
        choice = input('[!] your choice >> ')
        if (str(choice) == '1'):
            
            print(''' 
            1 => add new domain for laravel.
            2 => add new domain for nodeJS.
            3 => remove domain.
            4 => create new mysql user and database
            ''')
            choice = input('[!] your choice >> ')
            if (choice =="1"):
                domain = input('[!] type new domain >> ')
                php_verion = input('[!] type your php version default is 8.2 >> ') or "8.2"
                lara_add_new_domain(domain,php_verion)
            elif(choice =="2"):
                domain = input('[!] type new domain >> ')
                print('[!] do not use duplicated port number. ')
                port = input('[!] your project port >> ')
                node_newdomain(domain,port)
            elif(choice =="3"):
                domain = input('[+] type domain to remove >> ')
                ch = input ('[!] are you sure you want to (y) or (n) delete '+domain+' >> ')
                if (ch =='y' or ch =='Y'):
                    remove_domain(domain)
                else:
                    print('exit !')
            elif(choice =="4"):
                length = 12  # Set the desired password length
                characters = string.ascii_letters + string.digits 
                password = ''.join(random.choice(characters) for i in range(length))
                
                print("\033[32mWelcome to creating Database Section\033[0m")
                print("\033[93m[!] beware you should run this script as root to perform this function\033[0m")

                db_name = input('[!] enter the database name you want to create >> ')
                db_user = input("[!] enter the database username you want to create >> ")

                print('[-] if password empty we will generate a new password for you.')

                db_password = input("[!] enter the database password you want to create >> ") or password

                print("================================================")
                print("\033[31m[!] if root password wrong this function not work !!\033[0m")

                root_pw = input('[!] enter the root password of your mysql >> ') or str("")

                
                create_database (db_name,db_user,db_password,root_pw)


        elif(str(choice) == '2'):
            print(''' 
            1 => install mysql Server.
            2 => install PHP & composer.
            3 => install MariaDB Server.
            4 => install Nodejs.
            5 => install nginx
            ''')
            choice = input('[!] your choice >> ')
            if (choice =="1"):
                install_mysql()
            elif(choice=="2"):
                install_php_composer()
            elif(choice=="3"):
                install_mariadb()
            elif(choice=="5"):
                install_nginx()

            elif(choice=="4"):
               # print('[!] if you want node to be installed on other users run with no root user')


                install_nvm()

                          

        else:
            print('[!] scipt is exited ')
            exit()    
    except KeyboardInterrupt:
        print('[!] Lara Hoster is exited')
root_command=subprocess.check_output(['whoami'])


while True:
        banner()
        guide_msg()

