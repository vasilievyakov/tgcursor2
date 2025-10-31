#!/bin/bash

# Backup script for database

set -e

BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/backup_${TIMESTAMP}.sql"

echo "📦 Creating database backup..."

# Create backup directory if it doesn't exist
mkdir -p ${BACKUP_DIR}

# Create backup
docker-compose exec -T postgres pg_dump -U postgres tgcursor2 > ${BACKUP_FILE}

# Compress backup
gzip ${BACKUP_FILE}

echo "✅ Backup created: ${BACKUP_FILE}.gz"

# Keep only last 7 backups
cd ${BACKUP_DIR}
ls -t backup_*.sql.gz | tail -n +8 | xargs rm -f

echo "🧹 Old backups cleaned (keeping last 7)"

