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
                    def commitMessage = sh(returnStdout: true, script: 'git log -1 --pretty=%B').trim()
                    return !(commitMessage =~ /.*\[skip ci\].*/).find()
                }
            }
            steps {
                script {
                    withCredentials([file(credentialsId: 'diaryofapolymath-dot-env-file-test', variable: 'FILE')]) {
                        sh 'cp $FILE .env'
                        def testImage = docker.build('test-image', '-f Dockerfile.test .')
                        sh "docker run --rm ${testImage.id}"
                    }
                }
            }
        }
        stage('Deploy to staging') {
            when {
                branch 'staging'
                expression {
                    def commitMessage = sh(returnStdout: true, script: 'git log -1 --pretty=%B').trim()
                    return !(commitMessage =~ /.*\[skip ci\].*/).find()
                }
            }
            steps {
                script {
                    withCredentials([file(credentialsId: 'diaryofapolymath-dot-env-file-prod', variable: 'FILE')]) {
                        docker.withRegistry("https://${env.REGISTRY_URL}", 'registry-auth-credential') {
                            sh 'cp $FILE .env'
                            def stagingImage = docker.build("${env.REGISTRY_URL}/${env.REGISTRY_NAMESPACE}", '-f Dockerfile.build .')
                            stagingImage.push('staging')
                        }
                    }
                }
            }
        }
        stage('Deploy to production') {
            when {
                branch 'main'
                expression {
                    def commitMessage = sh(returnStdout: true, script: 'git log -1 --pretty=%B').trim()
                    return !(commitMessage =~ /.*\[skip ci\].*/).find()
                }
            }
            steps {
                script {
                    withCredentials([file(credentialsId: 'diaryofapolymath-dot-env-file-prod', variable: 'FILE')]) {
                        docker.withRegistry("https://${env.REGISTRY_URL}", 'registry-auth-credential') {
                            sh 'cp $FILE .env'
                            def prodImage = docker.build("${env.REGISTRY_URL}/${env.REGISTRY_NAMESPACE}", '-f Dockerfile.build .')
                            def releaseImage = docker.build("release-image", '-f Dockerfile.release .')
                            sh "docker run --rm ${releaseImage.id}"
                            prodImage.push(tag)
                            prodImage.push('latest')
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
