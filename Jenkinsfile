pipeline {
  agent none
  stages {
    stage('Build') {
      agent any
      steps {
        sh 'echo "building the repo"'
      }
    }
    stage('Dependency Check') {
      agent any
      steps {
        sh 'echo "Dependency Check"'
        dependencyCheck additionalArguments: '', odcInstallation: 'default'
        dependencyCheckPublisher pattern: 'dependency-check-report.xml'
      }
    }

    stage('Unit Test and warnings') {
      agent {
        dockerfile {
          filename 'Dockerfile.Jenkins'
        }
      }
      steps {
        sh "pwd"
        dir("web_app") {
          sh "cp .env.example .env"
        }
        sh "pwd"
        sh '''#!/bin/bash
        pytest
        python3 - m pylint--output - format = parseable--fail - under = 3.0. / web_app--msg - template = "{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" | tee pylint.log || echo "pylint exited with $?"
        '''
      }
    }

  }

  post {
    always {
      echo 'The pipeline completed'
      node(null) {
        script {
          echo "linting Success, Generating Report"
          recordIssues enabledForFailure: true, aggregatingResults: true, tool: pyLint(pattern: 'pylint.log')
        }

      }
    }
    success {
      echo "Flask Application Up and running!!"
    }
    failure {
      echo 'Build stage failed'
      error('Stopping early…')
    }
  }
}