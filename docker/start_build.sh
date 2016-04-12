#!/bin/bash
rm -rf target
./build.sh jenkins_build
cd target/site/cobertura
sed 's#filename="#filename="/var/develenv/jenkins/jobs/metrics-queue-consumer/workspace/workspace/#g' coverage.xml > coverage_new.xml
mv coverage.xml coverage_old.xml
mv coverage_new.xml coverage.xml
cd ../../..
metrics_runner.sh

