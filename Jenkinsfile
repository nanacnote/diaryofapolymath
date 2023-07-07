pipeline {
    agent none

    environment {
        REGISTRY_URL = "registry.hiramlabs.com"
        REGISTRY_NAMESPACE = "image/diaryofapolymath"
        DOT_ENV_FILE_TEST = credential('diaryofapolymath-dot-env-file-test')
        DOT_ENV_FILE_PROD = credential('diaryofapolymath-dot-env-file-prod')
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '5'))
        disableConcurrentBuilds()
    }

    stages {
        agent {
            dockerfile {
                filename 'Dockerfile.test'
            }
        }
        stage('Run all tests') {
            agent {
                docker {
                    image 'docker:latest'
                }
            }
            steps {
                script {
                    def image = docker.build('test-image', '-f Dockerfile.test .')
                    def container = image.run()
                    sh "docker logs ${container.id}")
                }
            }
        }
        stage('Deploy to staging') {
            when {
                branch 'staging'
            }
            agent {
                docker {
                    image 'docker:latest'
                    registryCredentials 'registry-auth-credential'
                }
            }
            steps {
                script {
                    def image = docker.build("${env.REGISTRY_URL}/${REGISTRY_NAMESPACE}", '-f Dockerfile.build .')
                    image.push('canary')
                }
            }
        }
        stage('Deploy to production') {
            when {
                branch 'master'
            }
            agent {
                docker {
                    image 'docker:latest'
                    registryCredentials 'registry-auth-credential'
                }
            }
            steps {
                script {
                    def tag = sh(script: "git describe --tags --abbrev=0 --match=master --exact-match", returnStdout: true).trim()
                    def image = docker.build("${env.REGISTRY_URL}/${REGISTRY_NAMESPACE}", '-f Dockerfile.build .')
                    image.push(tag)
                    image.push('latest')
                }
            }
        }
    }
    post {
        always {
            sh('docker system prune -a -f --volumes')
        }
    }
}
