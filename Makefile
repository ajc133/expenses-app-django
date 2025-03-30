.PHONY: backup
backup:
	rsync -avz ${UPLOADS_DIR} ${LOCAL_DIR}/
	rsync -avz ${DB_PATH} ${LOCAL_DIR}/
