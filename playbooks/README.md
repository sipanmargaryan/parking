### Parking ansible

This repository is responsible for provisioning and deployment of parking

* [Install](https://docs.ansible.com/ansible/2.7/installation_guide/intro_installation.html) Ansible
* Copy hosts.ini.dist to hosts.ini
* Replace the placeholder with your server IP (make sure, that you have an ssh access to the server)
* Use appropriate command to edit parameters in vault then deploy the application

### Commands

Run security playbook at the very beginning

```ansible-playbook security.yml -i hosts.ini -l prod```

Edit private file

```ansible-vault edit vars/private.yml```

Deploy

```ansible-playbook playbook.yml -i hosts.ini -l prod -t deploy```

Run all recipes

```ansible-playbook playbook.yml -i hosts.ini -l prod```