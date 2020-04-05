edit-vault:
	ansible-vault edit vars/private.yml

deploy:
	ansible-playbook --ask-vault-pass playbook.yml -i hosts.ini -l staging

deploy-prod:
	ansible-playbook --ask-vault-pass playbook.yml -i hosts.ini -l prod