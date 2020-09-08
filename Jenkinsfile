pipeline {
    agent {
        label "master"
    }

    environment {
        // GLobal Vars
        NAME = "lxp-skill-service"
        PROJECT= "labs"

        // Config repo managed by ArgoCD details
        ARGOCD_CONFIG_REPO = "github.com/WHOAcademy/lxp-config.git"
        ARGOCD_CONFIG_REPO_PATH = "lxp-deployment/values-test.yaml"
        ARGOCD_CONFIG_REPO_BRANCH = "who-int"
        SYSTEM_TEST_BRANCH = "master-who-int"

          // Job name contains the branch eg ds-app-feature%2Fjenkins-123
        JOB_NAME = "${JOB_NAME}".replace("%2F", "-").replace("/", "-")

        GIT_SSL_NO_VERIFY = true

        // Credentials bound in OpenShift
        GIT_CREDS = credentials("${OPENSHIFT_BUILD_NAMESPACE}-git-auth")
        NEXUS_CREDS = credentials("${OPENSHIFT_BUILD_NAMESPACE}-nexus-password")
        QUAY_PUSH_SECRET = "who-lxp-imagepusher-secret"

        // Nexus Artifact repo
        NEXUS_REPO_NAME="labs-static"
        NEXUS_REPO_HELM = "helm-charts"
    }

    // The options directive is for configuration that applies to the whole job.
    options {
        buildDiscarder(logRotator(numToKeepStr: '50', artifactNumToKeepStr: '1'))
        timeout(time: 15, unit: 'MINUTES')
        ansiColor('xterm')
    }

    stages {
        stage('Prepare Environment') {
            failFast true
            parallel {
                stage("Release Build") {
                    options {
                        skipDefaultCheckout(true)
                    }
                    agent {
                        node {
                            label "master"
                        }
                    }
                    when {
                        expression { GIT_BRANCH.startsWith("master") }
                    }
                    steps {
                        script {
                            env.APP_ENV = "prod"
                            // External image push registry info
                            env.IMAGE_REPOSITORY = "quay.io"
                            // app name for master is just learning-experience-platform or something
                            env.APP_NAME = "${NAME}".replace("/", "-").toLowerCase()
                            env.TARGET_NAMESPACE = "whoacademy"
                        }
                    }
                }
                stage("Sandbox Build") {
                    options {
                        skipDefaultCheckout(true)
                    }
                    agent {
                        node {
                            label "master"
                        }
                    }
                    when {
                        expression { GIT_BRANCH.startsWith("dev") || GIT_BRANCH.startsWith("feature") || GIT_BRANCH.startsWith("fix") }
                    }
                    steps {
                        script {
                            env.APP_ENV = "dev"
                            // Sandbox registry deets
                            env.IMAGE_REPOSITORY = 'image-registry.openshift-image-registry.svc:5000'
                            // ammend the name to create 'sandbox' deploys based on current branch
                            env.APP_NAME = "${GIT_BRANCH}-${NAME}".replace("/", "-").toLowerCase()
                            env.TARGET_NAMESPACE = "${PROJECT}-" + env.APP_ENV
                        }
                    }
                }
            }
        }

          stage("Build (Compile App)") {
            agent {
                node {
                    label "jenkins-agent-python38"
                }
            }
            steps {
                script {
                    env.VERSION = sh(returnStdout: true, script: "grep -oP \"(?<=version=')[^']*\" setup.py").trim()
                    env.VERSIONED_APP_NAME = "${NAME}-${VERSION}"
                    env.PACKAGE = "${VERSIONED_APP_NAME}.tar.gz"
                    env.SECRET_KEY = 'gs7(p)fk=pf2(kbg*1wz$x+hnmw@y6%ij*x&pq4(^y8xjq$q#f' //TODO: get it from secret vault
                    env.TEST_DATABASE_SERVICE_HOST = "test-postgresql.labs-dev"
                    env.TEST_DATABASE_SERVICE_PORT = "5432"
                }
                sh 'printenv'

                echo '### Install deps ###'
                sh 'pip install -r requirements.txt'

                echo '### Running tests ###'
                sh 'python manage.py migrate --settings=lxp_skill_service.settings.test'
                sh 'python manage.py test --with-coverage --cover-erase --cover-package=skill_app --with-xunit --xunit-file=xunittest.xml --cover-branches --cover-html --settings=lxp_skill_service.settings.test'

                echo '### Packaging App for Nexus ###'
                sh '''
                    python -m pip install --upgrade pip
                    pip install setuptools wheel
                    python setup.py sdist
                    curl -v -f -u ${NEXUS_CREDS} --upload-file dist/${PACKAGE} http://${SONATYPE_NEXUS_SERVICE_SERVICE_HOST}:${SONATYPE_NEXUS_SERVICE_SERVICE_PORT}/repository/${NEXUS_REPO_NAME}/${APP_NAME}/${PACKAGE}
                '''
            }
            // Post can be used both on individual stages and for the entire build.
            post {
                always {
                    // archiveArtifacts "**"
                    junit 'xunittest.xml'
                    // publish html
                    publishHTML target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: false,
                        keepAll: true,
                        reportDir: 'cover',
                        reportFiles: 'index.html',
                        reportName: 'Django Code Coverage'
                    ]
                }
            }
        }

      stage("Bake (OpenShift Build)") {
            options {
                skipDefaultCheckout(true)
            }
            agent {
                node {
                    label "master"
                }
            }
            steps {
                sh 'printenv'

                echo '### Get Binary from Nexus and shove it in a box ###'
                sh  '''
                    rm -rf package-contents*
                    curl -v -f -u ${NEXUS_CREDS} http://${SONATYPE_NEXUS_SERVICE_SERVICE_HOST}:${SONATYPE_NEXUS_SERVICE_SERVICE_PORT}/repository/${NEXUS_REPO_NAME}/${APP_NAME}/${PACKAGE} -o ${PACKAGE}
                    tar -xvf ${PACKAGE}
                    BUILD_ARGS=" --build-arg git_commit=${GIT_COMMIT} --build-arg git_url=${GIT_URL}  --build-arg build_url=${RUN_DISPLAY_URL} --build-arg build_tag=${BUILD_TAG}"
                    echo ${BUILD_ARGS}

                    # oc get bc ${APP_NAME} || rc=$?
                    # dirty hack so i don't have to oc patch the bc for the new version when pushing to quay ...
                    oc delete bc ${APP_NAME} || rc=$?
                    if [[ $TARGET_NAMESPACE == *"dev"* ]]; then
                        echo "🏗 Creating a sandbox build for inside the cluster 🏗"
                        oc new-build --binary --name=${APP_NAME} -l app=${APP_NAME} ${BUILD_ARGS} --strategy=docker
                        oc start-build ${APP_NAME} --from-dir=${VERSIONED_APP_NAME}/. ${BUILD_ARGS} --follow
                        # used for internal sandbox build ....
                        oc tag ${OPENSHIFT_BUILD_NAMESPACE}/${APP_NAME}:latest ${TARGET_NAMESPACE}/${APP_NAME}:${VERSION}
                    else
                        echo "🏗 Creating a potential build that could go all the way so pushing externally 🏗"
                        oc new-build --binary --name=${APP_NAME} -l app=${APP_NAME} ${BUILD_ARGS} --strategy=docker --push-secret=${QUAY_PUSH_SECRET} --to-docker --to="${IMAGE_REPOSITORY}/${TARGET_NAMESPACE}/${APP_NAME}:${VERSION}"
                        oc start-build ${APP_NAME} --from-dir=${VERSIONED_APP_NAME}/. ${BUILD_ARGS} --follow
                    fi
                '''
            }
      }

  stage("Helm Package App (master)") {
            agent {
                node {
                    label "jenkins-agent-helm"
                }
            }
            steps {
                sh 'printenv'
                sh '''
                    helm lint chart
                '''
                sh '''
                    # might be overkill...
                    yq w -i chart/Chart.yaml 'appVersion' ${VERSION}
                    yq w -i chart/Chart.yaml 'version' ${VERSION}
                    yq w -i chart/Chart.yaml 'name' ${APP_NAME}

                    # probs point to the image inside ocp cluster or perhaps an external repo?
                    yq w -i chart/values.yaml 'image_repository' ${IMAGE_REPOSITORY}
                    yq w -i chart/values.yaml 'image_name' ${APP_NAME}
                    yq w -i chart/values.yaml 'image_namespace' ${TARGET_NAMESPACE}
                    yq w -i chart/values.yaml 'image_tag' ${VERSION}

                    # latest built image
                    yq w -i chart/values.yaml 'app_tag' ${VERSION}
                '''
                sh '''
                    # package and release helm chart?
                    helm package chart/ --app-version ${VERSION} --version ${VERSION} --dependency-update
                    curl -v -f -u ${NEXUS_CREDS} http://${SONATYPE_NEXUS_SERVICE_SERVICE_HOST}:${SONATYPE_NEXUS_SERVICE_SERVICE_PORT}/repository/${NEXUS_REPO_HELM}/ --upload-file ${APP_NAME}-${VERSION}.tgz
                '''
            }
        }

        stage("Deploy App") {
            failFast true
            parallel {
                stage("sandbox - helm3 publish and install"){
                    options {
                        skipDefaultCheckout(true)
                    }
                    agent {
                        node {
                            label "jenkins-agent-helm"
                        }
                    }
                    when {
                        expression { GIT_BRANCH.startsWith("dev") || GIT_BRANCH.startsWith("feature") || GIT_BRANCH.startsWith("fix") }
                    }
                    steps {
                        // TODO - if SANDBOX, create release in rando ns
                        sh '''
                            helm uninstall ${APP_NAME} --namespace=${TARGET_NAMESPACE} || rc=$?
                            helm upgrade --install ${APP_NAME} \
                                --namespace=${TARGET_NAMESPACE} \
                                http://${SONATYPE_NEXUS_SERVICE_SERVICE_HOST}:${SONATYPE_NEXUS_SERVICE_SERVICE_PORT}/repository/${NEXUS_REPO_HELM}/${APP_NAME}-${VERSION}.tgz
                        '''
                    }
                }
                stage("test env - ArgoCD sync") {
                    options {
                        skipDefaultCheckout(true)
                    }
                    agent {
                        node {
                            label "jenkins-agent-argocd"
                        }
                    }
                    when {
                        expression { GIT_BRANCH.startsWith("master") }
                    }
                    steps {
                        echo '### Commit new image tag to git ###'
                        sh  '''
                            git clone https://${ARGOCD_CONFIG_REPO} config-repo
                            cd config-repo
                            git checkout ${ARGOCD_CONFIG_REPO_BRANCH}
                            yq w -i ${ARGOCD_CONFIG_REPO_PATH} "applications.name==test-${NAME}.source_ref" ${VERSION}
                            git config --global user.email "jenkins@rht-labs.bot.com"
                            git config --global user.name "Jenkins"
                            git config --global push.default simple
                            git add ${ARGOCD_CONFIG_REPO_PATH}
                            git commit -m "🚀 AUTOMATED COMMIT - Deployment of ${APP_NAME} at version ${VERSION} 🚀" || rc=$?
                            git remote set-url origin  https://${GIT_CREDS_USR}:${GIT_CREDS_PSW}@${ARGOCD_CONFIG_REPO}
                            git push -u origin ${ARGOCD_CONFIG_REPO_BRANCH}
                            # Give ArgoCD a moment to gather it's thoughts and roll out a deployment before Jenkins races on to test things
                            # issue here is an asynchronous pipline (argo) intreacting with a synchronous job ie jenkins
                            sleep 20
                        '''
                    }
                }


            }
        }

        stage("Validate Deployment") {
            failFast true
            parallel {
                stage("sandbox - validate deployment"){
                    options {
                        skipDefaultCheckout(true)
                    }
                    agent {
                        node {
                            label "master"
                        }
                    }
                    when {
                        expression { GIT_BRANCH.startsWith("dev") || GIT_BRANCH.startsWith("feature") || GIT_BRANCH.startsWith("fix") }
                    }
                    steps {
                        sh '''
                           set +x
                           COUNTER=0
                           DELAY=5
                           MAX_COUNTER=60
                           echo "Validating deployment of ${APP_NAME} in project ${TARGET_NAMESPACE}"
                           LATEST_DC_VERSION=\$(oc get dc ${APP_NAME} -n ${TARGET_NAMESPACE} --template='{{ .status.latestVersion }}')
                           RC_NAME=${APP_NAME}-\${LATEST_DC_VERSION}
                           set +e
                           while [ \$COUNTER -lt \$MAX_COUNTER ]
                           do
                             RC_ANNOTATION_RESPONSE=\$(oc get rc -n ${TARGET_NAMESPACE} \$RC_NAME --template="{{.metadata.annotations}}")
                             echo "\$RC_ANNOTATION_RESPONSE" | grep openshift.io/deployment.phase:Complete >/dev/null 2>&1
                             if [ \$? -eq 0 ]; then
                               echo "Deployment Succeeded!"
                               break
                             fi
                             echo "\$RC_ANNOTATION_RESPONSE" | grep -E 'openshift.io/deployment.phase:Failed|openshift.io/deployment.phase:Cancelled' >/dev/null 2>&1
                             if [ \$? -eq 0 ]; then
                               echo "Deployment Failed"
                               exit 1
                             fi
                             if [ \$COUNTER -lt \$MAX_COUNTER ]; then
                               echo -n "."
                               COUNTER=\$(( \$COUNTER + 1 ))
                             fi
                             if [ \$COUNTER -eq \$MAX_COUNTER ]; then
                               echo "Max Validation Attempts Exceeded. Failed Verifying Application Deployment..."
                               exit 1
                             fi
                             sleep \$DELAY
                           done
                           set -e
                        '''
                    }
                }
            }
        }

        stage("Trigger System Tests") {
            options {
                skipDefaultCheckout(true)
            }
            agent {
                node {
                    label "master"
                }
            }
            when {
                expression { GIT_BRANCH.startsWith("master") }
            }
            steps {
                sh  '''
                    echo "TODO - Run tests"
                '''
                build job: "system-tests/${SYSTEM_TEST_BRANCH}", parameters: [[$class: 'StringParameterValue', name: 'APP_NAME', value: "${APP_NAME}" ],[$class: 'StringParameterValue', name: 'VERSION', value: "${VERSION}"]], wait: false
            }
        }
    }
}
