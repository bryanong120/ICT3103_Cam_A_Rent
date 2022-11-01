pipeline {
    agent none 
stages {
	//stage('Build') {
	// parallel {
		stage('Build') {
			agent any 
		steps {
			sh 'echo "building the repo"'
			dependencyCheck additionalArguments: '', odcInstallation: 'default'
        dependencyCheckPublisher pattern: 'dependency-check-report.xml'
		}
		}
	// }
	//}

	stage('Test') {
		    agent {
        dockerfile { filename 'Dockerfile.Jenkins' }
    }
	steps {
		sh '''#!/bin/bash
		echo "hello world"
		python3 --version 
		pytest
		'''
		//pip3 install --no-cache-dir -r requirements.txt --user
		//input(id: "Deploy Gate", message: "Deploy ${params.project_name}?", ok: 'Deploy')
	}
	}
	// stage('Deploy')
	// {
	// steps {
	// 	echo "deploying the application"
	// 	sh "sudo nohup python3 app.py > log.txt 2>&1 &"
	// }
	// }
}

post {
		always {
			echo 'The pipeline completed'
			node(null){
				script{
					python3 -m pylint --output-format=parseable --fail-under=3.0 module --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" | tee pylint.log || echo "pylint exited with $?"
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
