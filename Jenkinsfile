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
                    hasSkipCiKeywordInCommitMsg()
                }
            }
            steps {
                script {
                    withCredentials([file(credentialsId: 'diaryofapolymath-dot-env-file-test', variable: 'FILE')]) {
                        sh 'rm -rf .env && cp $FILE .env'
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
                    hasSkipCiKeywordInCommitMsg()
                }
            }
            steps {
                script {
                    withCredentials([file(credentialsId: 'diaryofapolymath-dot-env-file-prod', variable: 'FILE')]) {
                        sh 'rm -rf .env && cp $FILE .env'
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
                    hasSkipCiKeywordInCommitMsg()
                }
            }
            steps {
                script {
                    withCredentials([file(credentialsId: 'diaryofapolymath-dot-env-file-prod', variable: 'FILE')]) {
                        sh 'rm -rf .env && cp $FILE .env'
                    }
                    def prodImage = docker.build("${env.REGISTRY_URL}/${env.REGISTRY_NAMESPACE}", '-f Dockerfile.build .')
                    def releaseImage = docker.build("release-image", '-f Dockerfile.release .')
                    sh """
                        docker run --name release-container ${releaseImage.id} --dry-run
                        docker cp release-container:/usr/home/diaryofapolymath/__version__ ./__version__
                    """
                    def tag = sh(returnStdout: true, script: "cat __version__").trim()
                    docker.withRegistry("https://${env.REGISTRY_URL}", 'registry-auth-credential') {
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

def hasSkipCiKeywordInCommitMsg() {
    def commitMessage = sh(returnStdout: true, script: 'git log -1 --pretty=%B').trim()
    return !(commitMessage =~ /.*\[skip ci\].*/).find()
}
