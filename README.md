# AzureCourse-Project03: Ensuring Quality Releases

## Introduction

The main focus of this project was to create disposable test environments and run a variety of automated tests with the usage of Azure DevOps Pipelines. It is neccessary to monitor our application's behavior, and also determine root causes by querying the application’s custom log files. This is done by using Azure Log Analytics and Azure Monitor.
A mocked REST API is deployed to Azure App Services. All the automated test execution happens mainly by using the CI/CD pipeline in Azure Pipelines.
Three major types of tests are performed:

1. Postman - Integration tests
2. Selenium - Functional UI tests
3. JMeter - Performance (load) tests

The remainder of this document presents screenshots with relevant headers which cover all the requirements and tools used to complete this project.
## Environment Creation & Deployment

### Terraform

Terraform init
![](https://github.com/Marko-Buda/AzureCourse-Project03/blob/master/screenshots/terraform_init.JPG)


Terraform plan

![](https://github.com/Marko-Buda/AzureCourse-Project03/blob/master/screenshots/terraform_plan.JPG)


Terraform apply
![](https://github.com/Marko-Buda/AzureCourse-Project03/blob/master/screenshots/terraform_apply.JPG)

### Azure Pipelines

Pipeline overview
![](https://github.com/Marko-Buda/AzureCourse-Project03/blob/master/screenshots/pipeline_summary.JPG)

Pipeline build
![](https://github.com/Marko-Buda/AzureCourse-Project03/blob/master/screenshots/pipeline_build.JPG)


## Automated Testing

### Postman - Integration tests

Postman Run Summary
![](https://github.com/Marko-Buda/AzureCourse-Project03/blob/master/screenshots/postman_tests_run_summary.JPG)

Postman Test Results
![](https://github.com/Marko-Buda/AzureCourse-Project03/blob/master/screenshots/postman_tests_results.JPG)

Postman Publish Test Results
![](https://github.com/Marko-Buda/AzureCourse-Project03/blob/master/screenshots/postman_publish_tests.JPG)

**NOTE**: Server for testing is read-only (the data that was written with POST is not stored in webserver - it only returns succesfull response with the body) and the server in general is unstable (it cannot handle multiple requests in sequential order which causes it to return 429 error).
Links on Knowledge which confirm these statements [link_1](https://knowledge.udacity.com/questions/398515) and [link_2](https://knowledge.udacity.com/questions/636454).

In regression tests I handled this by expecting either 200 or 429 responses. In data validation I could not as I'm expecting body data to be returned and its value checked. This is why put the -x option for Data Validation tests in [Azure pipelines yaml file](https://github.com/Marko-Buda/AzureCourse-Project03/blob/master/azure-pipelines.yaml#L78).

### Selenium - Functional UI tests

![](https://github.com/Marko-Buda/AzureCourse-Project03/blob/master/screenshots/selenium_ui_tests.JPG)

### JMeter - Performance (load) tests

JMeter endurance tests
![](https://github.com/Marko-Buda/AzureCourse-Project03/blob/master/screenshots/jmeter_endurance_tests.JPG)

JMeter stress tests
![](https://github.com/Marko-Buda/AzureCourse-Project03/blob/master/screenshots/jmeter_stress_tests.JPG)

**NOTE**: Due to my azure account being hacked by a hacker who set up an automatic deployment of resources groups with active VMs on all avaiable azure server locations I have now close to 500 euros of costs to pay ([link](https://github.com/Marko-Buda/AzureCourse-Project03/blob/master/screenshots/hacker_issue.JPG)). I have raised the ticket with Microsoft and they are currently investigating it. Because of these reasons I am not willing to execute jmeter tests on "30 users for a max duration of 60 seconds" as this will surely increase my costs. I have instead used 2 users on the period of 60 seconds of test execution. With this I was able to trigger the alert via e-mail ([link](https://github.com/Marko-Buda/AzureCourse-Project03/blob/master/screenshots/email_alert.JPG)).

## Monitoring and Observability

### Azure Monitor

E-mail for HTTP 200 status response
![](https://github.com/Marko-Buda/AzureCourse-Project03/blob/master/screenshots/email_alert.JPG)

Alert chart for HTTP 200 status response
![](https://github.com/Marko-Buda/AzureCourse-Project03/blob/master/screenshots/monitor_alert_chart.JPG)

Alerts monitor
![](https://github.com/Marko-Buda/AzureCourse-Project03/blob/master/screenshots/monitor_alert.JPG)

### Azure Log Analytics

Log for user login
![](https://github.com/Marko-Buda/AzureCourse-Project03/blob/master/screenshots/log_analytics_user_login.JPG)

Log for products added
![](https://github.com/Marko-Buda/AzureCourse-Project03/blob/master/screenshots/log_analytics_products_added.JPG)

Log for products removed
![](https://github.com/Marko-Buda/AzureCourse-Project03/blob/master/screenshots/log_analytics_products_removed.JPG)
