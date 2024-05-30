#!/bin/bash
run=$1

set -a
source .env
set +a

case $run in
    'sync')
    python3 icloud-sync.py
    ;;
    'token')
    python3 refresh-token.py
    ;;
    'tenant')
    python3 fetch-tenant.py
    ;;
    'test')
    python3 test.py
    ;;
    *)
    echo 'Wrong Mode!'
    ;;
esac