#!/bin/sh/

URL_Front="http://app:8000"
URL_Back="http://db:5432"

test_front() {
    echo "Tests du front en cours..."
    http_code=$(curl -s -o /dev/null -w "%{http_code}" $URL_Front)
    if [ $http_code -eq 200 ]; then
        echo "Test du front réussi (HTTP Status Code: $http_code)."
    else
        echo "Test du front échoué (HTTP Status Code: $http_code)."
    fi
}

test_back() {
    echo "Tests du back en cours..."
    http_code=$(curl -s -o /dev/null -w "%{http_code}" $URL_Back)
    if pg_isready -h db -p 5432 -q; then
        echo "Test du back réussi (PostgreSQL est prêt)."
    else
        echo "Test du back échoué (PostgreSQL ne tourne pas)."
    fi
    
}

# Run the tests
test_front
test_back