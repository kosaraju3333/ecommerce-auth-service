pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Identify Build') {
            steps {
                script {
                    echo "Branch: ${env.BRANCH_NAME}"
                    echo "PR Number: ${env.CHANGE_ID}"
                    echo "PR Target: ${env.CHANGE_TARGET}"
                }
            }
        }

        stage('PR - Validation') {
            when {
                allOf {
                    changeRequest()
                    expression {
                        return env.CHANGE_TARGET?.startsWith('release/')
                    }
                }
            }

            parallel {
                stage('Gitleaks') {
                    steps {
                        sh '''
                            set -eu

                            gitleaks git . \
                            --redact \
                            --exit-code 1
                        '''
                    }
                }

                stage('Pytest') {
                    steps {
                        sh '''
                            set -eu
                            python3 -m venv .venv
                            .venv/bin/python -m pip install -r requirements.txt
                            .venv/bin/python -m pip install pytest
                            .venv/bin/python -m pytest tests/unit/ -v
                            .venv/bin/python -m pytest tests/api/ -v
                        '''
                    }
                }

                stage('Trivy') {
                    steps {
                        echo 'Trivy configuration pending'
                    }
                }

            }

        }


        stage('Test Coverage') {
            when {
                expression {
                    return env.BRANCH_NAME?.startsWith('release/')
                }
            }

            steps {
                sh '''
                    set -eu

                    python3 -m venv .venv

                    .venv/bin/python -m pip install -r requirements.txt

                    .venv/bin/python -m pip install pytest pytest-cov

                    .venv/bin/python -m pytest tests/unit/ tests/api/ \
                        --cov=app \
                        --cov-report=term-missing \
                        --cov-report=xml:coverage.xml

                    test -s coverage.xml
                '''
            }
        }


        stage('SonarQube Analysis') {
            when {
                expression {
                    return env.BRANCH_NAME?.startsWith('release/')
                }
            }
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'

                    withSonarQubeEnv('SonarQube-Server') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=ecommerce-auth \
                            -Dsonar.sources=app,alembic,.env \
                            -Dsonar.tests=tests \
                            -Dsonar.python.version=3.13 \
                            -Dsonar.python.coverage.reportPaths=coverage.xml
                        """
                    }
                }
            }
        }
        

        stage('SonarQube Quality Gate') {
            when {
                expression {
                    return env.BRANCH_NAME?.startsWith('release/')
                }
            }
            steps {
                timeout(time: 10, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }


    }
}