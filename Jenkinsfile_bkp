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

        stage('PR Validation') {
            when {
                changeRequest()
            }
            steps {
                echo 'Running PR validation pipeline'
            }
        }

        stage('Release CI/CD') {
            when {
                expression {
                    return env.BRANCH_NAME ==~ /^release\/.+$/
                }
            }
            steps {
                echo 'Running release CI/CD pipeline'
            }
        }
    }
}