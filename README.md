# Finato-QA-Agentic-AI
QA agentic AI for the Finato invoice processing application

AH  Project Documentation: Datamatics QA AI Agent

Project Overview
This project aims to develop a QA Agentic AI to automate the deployment and testing processes for Datamatics’ health insurance invoice processing platform, Amplify Health. The primary focus is on streamlining the deployment of SQL stored procedures and conducting comprehensive testing to ensure system integrity and compliance with business requirements.

Current Deployment Process
* **Environment**: The deployment occurs in the UAT environment, which includes four servers: Scheduler, File, Web, and Database (IPM Amplify-Health).
* **Deployment Objects**: Include SQL stored procedures, JS files, cshtml files, Excel files for entity creation, and DLL deployments.
* **Process**:
    1. SQL objects are placed in a designated path for the SQL Executor scheduler.
    2. Before execution, a backup of the existing stored procedure is created.
    3. The backup follows the naming convention: SP_<original_name>_bkp_<date>.
    4. The new stored procedure is executed.
    5. Backup of all deployment files is taken in a folder named with today’s date and the project name.

Testing Requirements
* **Automation Testing**:
    * Conduct backend testing on the database to verify changes in stored procedures.
    * Ensure changes align with Business Related Documents (BRD) provided via email.
    * Perform unit, frontend, and regression testing.
    * Generate and deliver an Excel sheet with test cases, actual test data, expected results, and module details.

Project Goals
* Develop a QA Agentic AI capable of automating the deployment and testing processes.
* Create a comprehensive workflow and flowchart for the AI development.
* Identify the necessary tech stack and system requirements.
* Estimate the time to completion (ETA) for the project.
* Produce detailed documentation for the project.

Feasibility Study
* Assess the possibility of creating a QA Agentic AI for the described tasks.
* Evaluate the technical and logistical requirements for implementation.

Next Steps
* Conduct a detailed analysis of the current deployment and testing processes.
* Research and select appropriate AI technologies and tools for the project.
* Develop a prototype of the QA Agentic AI and test its functionality.
* Refine the prototype based on testing results and feedback.
* Finalise the workflow, flowchart, and documentation for the project.
