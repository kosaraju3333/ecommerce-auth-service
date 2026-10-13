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

        stage('PR - Gitleaks Scan') {
            when {
                allOf {
                    changeRequest()
                    expression {
                        return env.CHANGE_TARGET?.startsWith('release/')
                    }
                }
            }

            steps {
                sh '''
                    set -eu

                    gitleaks git . \
                    --redact \
                    --exit-code 1
                '''
            }


        }
    }
}