pipeline {
    agent any

    environment {
        REGISTRY_URL = "registry.hiramlabs.com"
        REGISTRY_NAMESPACE = "image/diaryofapolymath"
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '3'))
        disableConcurrentBuilds()
    }

    stages {
        stage('Run all tests') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'diaryofapolymath-dot-env-file-test', variable: 'FILE')]) {
                        sh 'cp $FILE .env'
                        def image = docker.build('test-image', '-f Dockerfile.test .')
                        sh "docker run --rm ${image.id}"
                    }
                }
            }
        }
        stage('Deploy to staging') {
            when {
                branch 'staging'
            }
            steps {
                script {
                    withCredentials([file(credentialsId: 'diaryofapolymath-dot-env-file-prod', variable: 'FILE')]) {
                        sh 'cp $FILE .env'
                        docker.withRegistry("https://${env.REGISTRY_URL}", 'registry-auth-credential') {
                            def image = docker.build("${env.REGISTRY_URL}/${env.REGISTRY_NAMESPACE}", '-f Dockerfile.build .')
                            image.push('canary')
                        }
                    }
                }
            }
        }
        stage('Deploy to production') {
            when {
                branch 'main'
            }
            steps {
                script {
                    withCredentials([file(credentialsId: 'diaryofapolymath-dot-env-file-prod', variable: 'FILE')]) {
                        sh 'cp $FILE .env'
                        docker.withRegistry("https://${env.REGISTRY_URL}", 'registry-auth-credential') {
                            def tag = sh(script: "git describe --tags --abbrev=0 --match=main --exact-match", returnStdout: true).trim()
                            def image = docker.build("${env.REGISTRY_URL}/${env.REGISTRY_NAMESPACE}", '-f Dockerfile.build .')
                            image.push(tag)
                            image.push('latest')
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            sh 'docker system prune -a -f --volumes'
        }
    }
}
