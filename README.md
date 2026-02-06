# Synapx_Assignment
This project is an Autonomous Insurance Claims Processing Agent designed to automate the early-stage processing of insurance FNOL (First Notice of Loss) documents. The system extracts key claim information from PDF forms, validates the presence of mandatory fields, detects inconsistencies, and classifies the claim into the correct workflow route based on business rules.
It aims to replicate the initial triage performed by human claim handlers, reducing manual workload and improving processing speed.
This project is capable of automatically extracting essential information from FNOL insurance documents, including policy details, incident information, involved parties, and asset-related data. It intelligently detects missing or incomplete fields to ensure that incomplete claims are flagged for manual review. The system also performs risk assessment by scanning the incident description for fraud-related or suspicious keywords. Using clearly defined business rules, the agent classifies each claim into the appropriate workflow route—such as fast-track, manual review, investigation, or specialist queues. All processed information is finally returned in a structured JSON format, making it easy to integrate with downstream insurance systems or automation pipelines.

->Steps to Run
1. Install Dependencies
2. Make sure Python is installed, then run:
3. pip install pdfplumber
4. Place the FNOL Document
5. Add the target FNOL PDF (e.g., ACORD-Automobile-Loss-Notice.pdf) into the project directory.
6. Run the Program
7. Execute the script using:
8. python main.py

View Output
The terminal will display a JSON object containing:
Extracted fields
Missing mandatory fields
Recommended routing category
Explanation for routing decision

Modify Input File (Optional)
You can change the file processed by editing the path inside the run() function in main.py.
