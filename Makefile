.PHONY: backup
backup:
	rsync -avz ${VPS_DIR} backups/
