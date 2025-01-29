pipeline {
    agent any

    parameters {
        string(name: 'EXECUTOR_ADDRESS', defaultValue: 'http://localhost:4444/wd/hub', description: 'Address of the Selenoid executor')
        string(name: 'APPLICATION_URL', defaultValue: 'http://192.168.1.196:8081', description: 'Address of the OpenCart application')
        string(name: 'BROWSER', defaultValue: 'chrome', description: 'Browser to use')
        string(name: 'THREADS', defaultValue: '1', description: 'Number of threads')
        string(name: 'BROWSER_VERSION', defaultValue: 'latest', description: 'Browser version')
    }

    stages {
        stage('Clean Workspace') {
            steps {
                deleteDir()
            }
        }
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/rustemsam/otus_selenium'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh '''
                echo "Installing dependencies..."
                pip install -r requirements.txt --break-system-packages
                pip install --no-cache-dir pydantic-core --platform manylinux2014_x86_64 -t . --only-binary=:all: --break-system-packages
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                echo "Starting tests with the following parameters:"
                echo "Executor Address: ${params.EXECUTOR_ADDRESS}"
                echo "Application URL: ${params.APPLICATION_URL}"
                echo "Browser: ${params.BROWSER}"
                echo "Browser Version: ${params.BROWSER_VERSION}"
                echo "Threads: ${params.THREADS}"


                python3 -m pytest --browser=${params.BROWSER} \
                                  --selenium_url=${params.EXECUTOR_ADDRESS} \
                                  --base_url=${params.APPLICATION_URL} \
                                  --junit-xml=junit.xml \
                                  --alluredir=allure-results \
                                  src/tests/pages/login/test_admin_login.py
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'junit.xml', fingerprint: true
            junit 'junit.xml'
        }
        failure {
            echo "Build failed! Check logs for errors."
        }
    }
}
