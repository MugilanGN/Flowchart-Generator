Define structure Patient
    Declare string variables name, icnumber, birthday, contactDetails, medicalHistory, insuranceInfo, patientID

Define structure Diagnosis
    Declare string variables diagnosis, treatment, billingCode

Declare constant integer MAX_PATIENTS = 100
Declare integer patientCount = 0
Declare array patients[MAX_PATIENTS] of Patient
Declare diagnosis of type Diagnosis

While true
    Display menu options:
        "1. Add New Patient"
        "2. Generate Patient Chart"
        "3. Generate Billing Statement"
        "4. Exit"
        "Enter your choice: "
    Read choice from user

    If choice is 1
        If patientCount is greater than or equal to MAX_PATIENTS
            Display "Maximum number of patients reached."
            Continue to next iteration of the loop

        Declare newPatient of type Patient
        Display "Enter patient name: "
        Read newPatient.name from user
        Display "Enter patient's birthday: "
        Read newPatient.birthday from user
        Display "Enter patient's ic number: "
        Read newPatient.icnumber from user
        Display "Enter contact details: "
        Read newPatient.contactDetails from user
        Display "Enter medical history: "
        Read newPatient.medicalHistory from user

        Display insurance types
        Display "1. Hospitalization and surgery insurance"
        Display "2. Critical illness insurance"
        Display "3. Disability income insurance"
        Display "4. Long-term care insurance"
        Display "5. Hospital income insurance"
        Display "6. Comprehensive health insurance"
        Display "Enter insurance information (1-6): "
        Read insuranceChoice from user

        Switch insuranceChoice
            Case 1:
                Set newPatient.insuranceInfo to "HOSPITALIZATION AND SURGERY INSURANCE"
            Case 2:
                Set newPatient.insuranceInfo to "CRITICAL ILLNESS INSURANCE"
            Case 3:
                Set newPatient.insuranceInfo to "DISABILITY INCOME INSURANCE"
            Case 4:
                Set newPatient.insuranceInfo to "LONG-TERM CARE INSURANCE"
            Case 5:
                Set newPatient.insuranceInfo to "HOSPITAL INCOME INSURANCE"
            Case 6:
                Set newPatient.insuranceInfo to "COMPREHENSIVE HEALTH INSURANCE"
            Default:
                Set newPatient.insuranceInfo to "UNKNOWN"

        Increment patientCount
        Generate patientID by concatenating "P" and the value of patientCount
        Set newPatient.patientID to patientID

        Set patients[patientCount - 1] to newPatient

        Display "Patient added successfully. Patient ID: " + newPatient.patientID

    If choice is 2
        If patientCount is 0
            Display "No patient available."
            Continue to next iteration of the loop

        Display "Enter patient index (1-" + patientCount + "): "
        Read patientIndex from user

        If patientIndex is less than 1 or greater than patientCount
            Display "Invalid patient index."
            Continue to next iteration of the loop

        Set patient to patients[patientIndex - 1]

        Display "Enter diagnosis: "
        Read diagnosis.diagnosis from user
        Display "Enter treatment: "
        Read diagnosis.treatment from user

        Call generatePatientChart(patient, diagnosis)

    If choice is 3
        If patientCount is 0
            Display "No patient available."
            Continue to next iteration of the loop

        Display "Enter patient index (1-" + patientCount + "): "
        Read patientIndex from user

        If patientIndex is less than 1 or greater than patientCount
            Display "Invalid patient index."
            Continue to next iteration of the loop

        Set patient to patients[patientIndex - 1]

        Display "Enter billing code: "
        Read diagnosis.billingCode from user

        Call generateBillingStatement(patient, diagnosis)

    If choice is 4
        Break the loop
        If choice is not 1, 2, 3, or 4
        Display "Invalid choice. Please try again."
End While

End program