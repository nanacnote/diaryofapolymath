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
            when {
                expression {
                    return isCommitMsgValidForCI()
                }
            }
            steps {
                script {
                    withCredentials([file(credentialsId: 'diaryofapolymath-dot-env-file-test', variable: 'FILE')]) {
                        sh 'cp "$FILE" .env'
                    }
                    def testImage = docker.build('test-image', '-f Dockerfile.test .')
                    sh "docker run --rm ${testImage.id}"
                }
            }
        }
        stage('Deploy to staging') {
            when {
                branch 'staging'
                expression {
                    return isCommitMsgValidForCI()
                }
            }
            steps {
                script {
                    withCredentials([file(credentialsId: 'diaryofapolymath-dot-env-file-staging-prod', variable: 'FILE')]) {
                        sh 'rm -rf .env && cp "$FILE" .env'
                    }
                    docker.withRegistry("https://${env.REGISTRY_URL}", 'registry-auth-credential') {
                        def stagingImage = docker.build("${env.REGISTRY_URL}/${env.REGISTRY_NAMESPACE}", '-f Dockerfile.build .')
                        stagingImage.push('staging')
                    }
                }
            }
        }
        stage('Deploy to production') {
            when {
                branch 'main'
                expression {
                    return isCommitMsgValidForCI()
                }
            }
            steps {
                script {
                    withCredentials([file(credentialsId: 'diaryofapolymath-dot-env-file-main-prod', variable: 'FILE')]) {
                        sh 'rm -rf .env && cp "$FILE" .env'
                    }
                    docker.withRegistry("https://${env.REGISTRY_URL}", 'registry-auth-credential') {
                        def prodImage = docker.build("${env.REGISTRY_URL}/${env.REGISTRY_NAMESPACE}", '-f Dockerfile.build .')
                        def releaseImage = docker.build("release-image", '-f Dockerfile.release .')
                        sh "docker run --rm -v ${pwd()}:/usr/home/diaryofapolymath ${releaseImage.id}"
                        def tag = sh(returnStdout: true, script: 'cat __version__').trim()
                        prodImage.push(tag)
                        prodImage.push('latest')
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

def isCommitMsgValidForCI() {
    def commitMessage = sh(returnStdout: true, script: 'git log -1 --pretty=%B').trim()
    return !(commitMessage =~ /.*\[skip ci\].*/).find()
}

