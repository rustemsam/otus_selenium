pipeline {
    agent any

    parameters {
        string(name: 'EXECUTOR_ADDRESS', defaultValue: 'http://localhost:4444/wd/hub', description: 'Selenoid executor address')
        string(name: 'APPLICATION_URL', defaultValue: 'http://192.168.1.196:8081', description: 'OpenCart application URL')
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
                script {
                    def executor = params.EXECUTOR_ADDRESS
                    def app_url = params.APPLICATION_URL
                    def browser = params.BROWSER
                    def browser_version = params.BROWSER_VERSION
                    def threads = params.THREADS

                    sh """
                    echo "Starting tests with the following parameters:"
                    echo "Executor Address: $executor"
                    echo "Application URL: $app_url"
                    echo "Browser: $browser"
                    echo "Browser Version: $browser_version"
                    echo "Threads: $threads"

                    python3 -m pytest --browser=$browser \
                                      --selenium_url=$executor \
                                      --base_url=$app_url \
                                      --junit-xml=reports/junit.xml \
                                      --alluredir=allure-results \
                                      src/tests/pages/login/test_admin_login.py
                    """
                }
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
            archiveArtifacts artifacts: 'reports/junit.xml', fingerprint: true
            junit 'reports/junit.xml'
        }
        failure {
            echo "Build failed! Check logs for errors."
        }
    }
}
