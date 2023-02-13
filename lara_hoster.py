import os
import random
import subprocess

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
    f.write(confx)
    f.close()
    os.system('sudo ln -s /etc/nginx/sites-available/'+domain+'.conf /etc/nginx/sites-enabled/'+domain+'.conf')
    os.system('sudo systemctl restart nginx')
    print('[!] every thing done but if you got any problem with permsion run this command')
    print('[!] chown -R www-data:www-data /var/www/html/'+domain)


def install_nginx():
    os.system('sudo apt-get update')
    os.system('sudo apt-get install nginx -y')
    print('nginx installed successfully!')
def install_mysql():
    os.system('sudo apt-get update')
    os.system('sudo apt-get install mysql-server -y')
    os.system('sudo systemctl start mysql.service')
    os.system('sudo mysql_secure_installation')
    os.system('sudo systemctl start mysql.service')
    print('[!] Mysql installed successfully!')
def install_mariadb():
    os.system('sudo apt-get update')
    os.system('sudo apt-get install mariadb-server -y')
    os.system('sudo systemctl start mariadb.service')
    os.system('sudo mysql_secure_installation')
    os.system('sudo systemctl start mariadb.service')
    print('[!] mariadb installed successfully!')
def install_nvm(version):
    os.system('sudo apt-get update')
    os.system('sudo apt-get install curl -y')
    
    os.system('sudo  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash')
  

    os.system('''export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
    ''')
    print('[!] nvm installed successfully!')
    nvm_bash = '''
        . ~/.nvm/nvm.sh
        . ~/.profile
        . ~/.bashrc
        nvm install '''+version

    x=open('nvinstall.sh','w')
    x.write(nvm_bash)
    x.close()
    os.system('sudo bash nvinstall.sh')
    os.system('sudo rm nvinstall.sh')


    print('[!] node is installed successfully')

def install_php_composer():
    version = input('[+] please type php version for example 8.1 >> ')
    os.system('sudo apt-get update')
    os.system('sudo apt-get install software-properties-common -y')
    os.system('sudo add-apt-repository ppa:ondrej/php -y')
    if version =='8.1':
        os.system('sudo apt-get install php8.1 php8.1-mbstring php8.1-gettext php8.1-zip php8.1-fpm php8.1-curl php8.1-mysql php8.1-gd php8.1-cgi php8.1-soap php8.1-sqlite3 php8.1-xml php8.1-redis php8.1-bcmath php8.1-imagick php8.1-intl -y')  
    else:
        os.system('sudo apt-get install php'+version+' php'+version+'-mbstring php'+version+'-gettext php'+version+'-zip php'+version+'-fpm php'+version+'-curl php'+version+'-mysql php'+version+'-gd php'+version+'-cgi php'+version+'-soap php'+version+'-sqlite3 php'+version+'-xml php'+version+'-redis php'+version+'-bcmath php'+version+'-imagick php'+version+'-intl -y')
    os.system('sudo sudo apt-get install git composer -y')
    print(' composer and php installed successfully!')
def add_new_domain(domain):
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
            fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
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

    print('[!] every thing done but if you got any problem with permsion run this command')
    print('[!] chown -R www-data:www-data /var/www/html/'+domain)



def remove_domain(domain):
    
    os.system('sudo rm -r /var/www/html/'+str(domain))
    os.system('sudo rm /etc/nginx/sites-available/'+domain+'.conf')
    os.system('sudo rm /etc/nginx/sites-enabled/'+domain+'.conf')
    os.system('sudo systemctl restart nginx')
    print('[!] now the '+domain+' is deleted !')


os.system('clear')

def banner():
        
    print('''

    
    ░█─── ─█▀▀█ ░█▀▀█ ─█▀▀█ 　 ░█─░█ █▀▀█ █▀▀ ▀▀█▀▀ █▀▀ █▀▀█ 
    ░█─── ░█▄▄█ ░█▄▄▀ ░█▄▄█ 　 ░█▀▀█ █──█ ▀▀█ ──█── █▀▀ █▄▄▀ 
    ░█▄▄█ ░█─░█ ░█─░█ ░█─░█ 　 ░█─░█ ▀▀▀▀ ▀▀▀ ──▀── ▀▀▀ ▀─▀▀

    automaicaly host your Project  !

    from FD

    github.com/FDX100

    ====================================
    please run this tool as root user
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
            ''')
            choice = input('[!] your choice >> ')
            if (choice =="1"):
                domain = input('[!] type new domain >> ')
                add_new_domain(domain)
            elif(choice =="2"):
                domain = input('[!] type new domain >> ')
                print('[!] do not use duplicated port number.')
                port = input('[!] your project port >> ')
                add_new_domain(domain)
            elif(choice =="3"):
                domain = input('[+] type domain to remove >> ')
                ch = input ('[!] are you sure you want to (y) or (n) delete '+domain+' >> ')
                if (ch =='y' or ch =='Y'):
                    remove_domain(domain)
                else:
                    print('exit !')

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
                print('[!] if you want node to be installed on other users run with no root user')
                print('[!] node version to install example (14.5) if you do not know just press enter')
                version = input("[+] type version of node >> ")
                if (str(version) ==""):
                    
                    install_nvm("--lts")
                else:
                     install_nvm(version)

                          

        else:
            print('[!] scipt is exited ')
            exit()    
    except KeyboardInterrupt:
        print('[!] Lara Hoster is exited')
root_command=subprocess.check_output(['whoami'])


while True:
        banner()
        guide_msg()

