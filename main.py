import re
import json
import pdfplumber

REQUIRED_FIELDS = {
    "policyNumber",
    "policyholderName",
    "effectiveDates",
    "date",
    "time",
    "location",
    "description",
    "claimant",
    "thirdParties",
    "contactDetails",
    "assetID",
    "estimatedDamage",
    "claimType",
    "attachments",
    "initialEstimate"
}

def extract_from_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    # Simplistic pattern matching
    fields = {
        "policyInformation": {
            "policyNumber": find_field(text, r"POLICY NUMBER[: ]*(.*)"),
            "policyholderName": find_field(text, r"NAME OF INSURED.*\n(.*)"),
            "effectiveDates": ""
        },
        "incidentInformation": {
            "date": find_field(text, r"DATE OF LOSS[: ]*(.*)"),
            "time": find_field(text, r"TIME[: ]*(.*)"),
            "location": find_field(text, r"LOCATION OF LOSS.*\n(.*)"),
            "description": find_field(text, r"DESCRIPTION OF ACCIDENT.*\n(.*)")
        },
        "involvedParties": {
            "claimant": find_field(text, r"DRIVER'S NAME AND ADDRESS.*\n(.*)"),
            "thirdParties": "",
            "contactDetails": ""
        },
        "assetDetails": {
            "assetType": "Automobile",
            "assetID": find_field(text, r"V\.I\.N\.: (.*)"),
            "estimatedDamage": find_field(text, r"ESTIMATE AMOUNT[: ]*(.*)")
        },
        "otherFields": {
            "claimType": "",
            "attachments": "",
            "initialEstimate": ""
        }
    }

    return fields


def find_field(text, pattern):
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()
    return ""


def find_missing_fields(extracted):
    flat = json.loads(json.dumps(extracted).replace(" ", ""))
    missing = []

    def recurse(obj):
        for key, val in obj.items():
            if isinstance(val, dict):
                recurse(val)
            else:
                if (key in REQUIRED_FIELDS) and (val == ""):
                    missing.append(key)

    recurse(extracted)
    return missing


def classify_claim(extracted, missing):
    # Rule: Missing mandatory fields → Manual Review
    if missing:
        return "Manual Review", "Mandatory FNOL fields are missing."

    # Extract damage estimate
    estimate = extracted["assetDetails"]["estimatedDamage"]
    est = int(re.sub(r"[^\d]", "", estimate)) if estimate else 0

    # Rule: <25,000 → Fast-track
    if est < 25000:
        return "Fast-track", "Estimated damage < 25,000."

    return "Standard", "Default routing."


def run(path):
    data = extract_from_pdf(path)
    missing = find_missing_fields(data)
    route, reason = classify_claim(data, missing)

    output = {
        "extractedFields": data,
        "missingFields": missing,
        "recommendedRoute": route,
        "reasoning": reason
    }

    print(json.dumps(output, indent=4))


if __name__ == "__main__":
    run("ACORD-Automobile-Loss-Notice-12.05.16.pdf")
