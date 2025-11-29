"""
MediWise AI Bot - Server Script
================================

Purpose: Comprehensive data retrieval and analysis bot for ERPNext Healthcare
Type: Server Script (API)
API Method: mediwise_bot.query
AI Integration: RAG via n8n Webhook

⚠️ DEPLOYMENT INSTRUCTIONS:
1. Go to ERPNext → Server Script → New (or edit existing)
2. Script Name: MediWise AI Bot
3. Script Type: API
4. API Method: mediwise_bot.query
5. Paste this entire script
6. Update N8N_WEBHOOK_URL with your n8n webhook URL
7. Enable and Save

⚠️ CONFIGURATION:
- Update N8N_WEBHOOK_URL in the RAG WEBHOOK CONFIGURATION section
- The webhook should accept: {"sessionId": "...", "chatInput": "..."}
- The webhook should return: {"output": "AI response text"}

Author: MediWise Development Team
Version: 3.0.0 (RAG Integration)
Last Updated: December 2024

NOTE: frappe and json are pre-loaded in Server Scripts, no imports needed
"""

# pylint: disable=all
# type: ignore
# pyright: reportUndefinedVariable=false
# The above comments suppress linter warnings for frappe/json which are pre-loaded in Server Scripts

# =============================================================================
# RAG WEBHOOK CONFIGURATION
# =============================================================================

# ⚠️ REPLACE WITH YOUR ACTUAL N8N WEBHOOK URL
# Get from your n8n workflow webhook node
N8N_WEBHOOK_URL = "https://surgemind.app.n8n.cloud/webhook/82106378-43fd-4766-9117-0465104fcc67"


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

# Get request payload
payload = frappe.form_dict  # noqa: F821
query_type = payload.get("query_type")
parameters = payload.get("parameters", {})
options = payload.get("options", {})

# =============================================================================
# AI-POWERED QUERY (RAG WEBHOOK)
# =============================================================================

if query_type == "ai_query":
    # AI-powered intelligent query with RAG webhook
    patient_id = parameters.get("patient_id")
    user_query = parameters.get("user_query", "")
    patient_context = parameters.get("patient_context", {})
    is_initial_load = parameters.get("is_initial_load", False)
    session_id = parameters.get("session_id")  # Session ID from frontend (includes timestamp)
    file_url = parameters.get("file_url")  # File URL from Frappe upload
    file_name = parameters.get("file_name")
    file_type = parameters.get("file_type")
    
    if not user_query:
        frappe.response.update({
            "status": "error",
            "message": "user_query is required for AI queries"
        })
    elif not patient_context or not patient_context.get("patient"):
        frappe.response.update({
            "status": "error",
            "message": "patient_context is required for AI queries"
        })
    else:
        try:
            # Send COMPLETE raw patient data JSON to LLM - NO TRANSFORMATION
            # Use simple JSON serialization - data comes from frontend already as clean JSON
            try:
                patient_data_json = json.dumps(patient_context, indent=2, default=str)
            except:
                # Fallback: convert to string if JSON serialization fails
                patient_data_json = str(patient_context)
            
            # Build chat input for RAG webhook with FULL raw JSON
            if is_initial_load:
                chat_input = f"""I've just opened this patient's medical record. Please analyze their complete profile and provide:

COMPLETE PATIENT DATA (RAW JSON):
{patient_data_json}

Please provide:
1. A brief overview of the patient
2. Key alerts or concerns (allergies, chronic conditions)
3. Important points from their medical history
4. Any recommendations for the doctor's attention

Keep it concise and actionable."""
            else:
                chat_input = f"""COMPLETE PATIENT DATA (RAW JSON):
{patient_data_json}

DOCTOR'S QUESTION:
{user_query}

Provide a helpful medical response based on the complete patient data above. Analyze all encounter details, symptoms, diagnosis, medications, lab tests, and procedures."""
            
            # Add file information to chat input if provided
            if file_url:
                # Build full public URL if relative
                if file_url.startswith('/'):
                    frappe_base = frappe.utils.get_url()  # noqa: F821
                    full_file_url = f"{frappe_base}{file_url}"
                else:
                    full_file_url = file_url
                
                # Determine file type for context
                file_type_info = ""
                if file_type:
                    file_type_info = f" (type: {file_type})"
                elif file_name:
                    ext = file_name.split('.')[-1].lower()
                    if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                        file_type_info = " (image)"
                    elif ext == 'pdf':
                        file_type_info = " (PDF document)"
                    elif ext in ['doc', 'docx']:
                        file_type_info = " (Word document)"
                    elif ext == 'txt':
                        file_type_info = " (text file)"
                    elif ext in ['xls', 'xlsx']:
                        file_type_info = " (Excel file)"
                    else:
                        file_type_info = " (file)"
                
                # Add file reference to chat input
                file_context = f"""

IMPORTANT: A file has been uploaded for analysis:
- File Name: {file_name or 'Uploaded file'}{file_type_info}
- File URL: {full_file_url}

Please analyze this file in the context of the patient's medical data."""
                chat_input = f"{chat_input}{file_context}"
            
            # Use session ID from frontend (generated with timestamp when patient is selected)
            # Fallback to patient_id-based session if not provided (for backward compatibility)
            if not session_id:
                session_id = f"patient_{patient_id}"
            
            # Call n8n RAG webhook
            webhook_response = frappe.make_post_request(
                N8N_WEBHOOK_URL,
                headers={
                    "Content-Type": "application/json"
                },
                data=json.dumps({
                    "sessionId": session_id,
                    "chatInput": chat_input
                })
            )
            
            # Parse webhook response
            if isinstance(webhook_response, str):
                webhook_response = json.loads(webhook_response)
            
            # Extract AI response from webhook
            # Expected format: {"output": "AI response text"}
            ai_response = None
            if isinstance(webhook_response, dict):
                if "output" in webhook_response:
                    ai_response = webhook_response["output"]
                elif "message" in webhook_response:
                    # Handle alternative response format
                    ai_response = webhook_response["message"]
                elif "response" in webhook_response:
                    ai_response = webhook_response["response"]
                else:
                    # If response structure is unexpected, try to get any text field
                    for key in ["text", "content", "result", "data"]:
                        if key in webhook_response:
                            value = webhook_response[key]
                            if isinstance(value, str):
                                ai_response = value
                                break
                            elif isinstance(value, dict) and "text" in value:
                                ai_response = value["text"]
                                break
            
            # If still no response, use the whole response as string
            if not ai_response:
                if isinstance(webhook_response, str):
                    ai_response = webhook_response
                else:
                    ai_response = json.dumps(webhook_response)
            
            frappe.response.update({
                "status": "success",
                "query_type": query_type,
                "data": {
                    "ai_response": ai_response,
                    "user_query": user_query,
                    "patient_id": patient_id,
                    "model_used": "RAG (n8n)"
                }
            })
            
        except Exception as e:
            # Log the error for debugging
            frappe.log_error(
                title="MediWise AI Bot - RAG Processing Error",
                message=f"Error: {str(e)}\nPatient ID: {patient_id}\nQuery: {user_query}"
            )
            frappe.response.update({
                "status": "error",
                "message": f"RAG processing failed: {str(e)}",
                "fallback_message": "AI assistant temporarily unavailable. Please try again."
            })

# =============================================================================
# SEARCH PATIENTS
# =============================================================================

elif query_type == "search_patients":
    search_term = parameters.get("search_term", "")
    limit = parameters.get("limit", 5000)  # Default to high limit to load all patients
    
    filters = []
    if search_term:
        filters.append(["patient_name", "like", f"%{search_term}%"])
    
    patients = frappe.get_all(
        "Patient",
        filters=filters,
        fields=["name", "patient_name", "mobile", "email", "sex as gender", "dob", "blood_group"],
        order_by="modified desc",
        limit=limit
    )
    
    frappe.response.update({
        "status": "success",
        "query_type": query_type,
        "data": {
            "results": patients,
            "count": len(patients)
        }
    })

# =============================================================================
# GET PATIENT SUMMARY
# =============================================================================

elif query_type == "get_patient_summary":
    patient_id = parameters.get("patient_id")
    
    if not patient_id:
        frappe.throw("patient_id is required")
    
    # Get patient - get ALL fields as raw dict
    patient = frappe.get_doc("Patient", patient_id)
    patient_data = patient.as_dict()
    
    # Get encounter names first
    encounter_names = frappe.get_all(
        "Patient Encounter",
        filters={"patient": patient_id, "docstatus": ["!=", 2]},
        fields=["name"],
        order_by="encounter_date desc",
        limit=5
    )
    
    # Get ALL encounter data as raw dicts (including all child tables)
    encounters = []
    for enc_name in encounter_names:
        try:
            enc_doc = frappe.get_doc("Patient Encounter", enc_name.name)
            # Use as_dict() to get ALL fields including child tables - NO TRANSFORMATION
            enc_data = enc_doc.as_dict()
            encounters.append(enc_data)
        except Exception as e:
            # If we can't get full doc, skip it
            pass
    
    # Get appointment names first
    appointment_names = frappe.get_all(
        "Patient Appointment",
        filters={
            "patient": patient_id,
            "appointment_date": [">=", frappe.utils.nowdate()],
            "status": ["in", ["Open", "Scheduled", "Confirmed"]]
        },
        fields=["name"],
        order_by="appointment_date asc",
        limit=5
    )
    
    # Get ALL appointment data as raw dicts (including all fields) - NO TRANSFORMATION
    appointments = []
    for apt_name in appointment_names:
        try:
            apt_doc = frappe.get_doc("Patient Appointment", apt_name.name)
            # Use as_dict() to get ALL fields
            apt_data = apt_doc.as_dict()
            appointments.append(apt_data)
        except Exception as e:
            # If we can't get full doc, skip it
            pass
    
    # Get lab tests
    lab_tests = frappe.get_all(
        "Lab Test",
        filters={"patient": patient_id},
        fields=["name", "lab_test_name", "status", "result_date", "creation"],
            order_by="creation desc",
            limit=5
        )
    
    # Patient data is already in patient_data from as_dict() above
    # No need to manually extract fields - we have everything
    
    # Build alerts
    alerts = []
    try:
        if patient.allergies:
            alerts.append({
                "type": "allergy",
                "severity": "high",
                "message": f"Allergies: {patient.allergies}"
            })
    except:
        pass
    
    frappe.response.update({
        "status": "success",
        "query_type": query_type,
        "data": {
            "patient": patient_data,
            "recent_encounters": encounters,
            "upcoming_appointments": appointments,
            "pending_lab_tests": lab_tests,
            "alerts": alerts
        }
    })

# =============================================================================
# GET PATIENT DETAILS
# =============================================================================

elif query_type == "get_patient_details":
    patient_id = parameters.get("patient_id")
    
    if not patient_id:
        frappe.throw("patient_id is required")
    
    patient = frappe.get_doc("Patient", patient_id)
    
    # Build patient data safely without hasattr/getattr
    patient_info = {"name": patient.name, "patient_name": patient.patient_name}
    
    try:
        patient_info["mobile"] = patient.mobile
    except:
        patient_info["mobile"] = None
    
    try:
        patient_info["email"] = patient.email
    except:
        patient_info["email"] = None
    
    try:
        patient_info["gender"] = patient.sex
    except:
        patient_info["gender"] = None
    
    try:
        patient_info["blood_group"] = patient.blood_group
    except:
        patient_info["blood_group"] = None
    
    try:
        patient_info["age"] = patient.age_html
    except:
        patient_info["age"] = None
    
    try:
        patient_info["dob"] = str(patient.dob) if patient.dob else None
    except:
        patient_info["dob"] = None
    
    frappe.response.update({
        "status": "success",
        "query_type": query_type,
        "data": patient_info
    })

# =============================================================================
# ANALYZE PATIENT HISTORY
# =============================================================================

elif query_type == "analyze_patient_history":
    patient_id = parameters.get("patient_id")
    
    if not patient_id:
        frappe.throw("patient_id is required")
    
    patient = frappe.get_doc("Patient", patient_id)
    encounters = frappe.get_all(
        "Patient Encounter",
        filters={"patient": patient_id, "docstatus": 1},
        fields=["name", "encounter_date"]
    )
    
    frappe.response.update({
        "status": "success",
        "query_type": query_type,
        "data": {
            "patient_profile": {
                "name": patient.name,
                "patient_name": patient.patient_name,
            },
            "visit_frequency": {
                "total_visits": len(encounters),
                "last_visit": str(encounters[0]["encounter_date"]) if encounters else None
            }
        }
    })

# =============================================================================
# GET ACTIVE PRESCRIPTIONS
# =============================================================================

elif query_type == "get_active_prescriptions":
    patient_id = parameters.get("patient_id")
    
    if not patient_id:
        frappe.throw("patient_id is required")
    
    encounters = frappe.get_all(
        "Patient Encounter",
        filters={
            "patient": patient_id,
            "docstatus": 1,
            "encounter_date": [">=", frappe.utils.add_days(frappe.utils.nowdate(), -90)]
        },
        fields=["name", "encounter_date", "practitioner"],
        order_by="encounter_date desc"
    )
    
    prescriptions = []
    for enc in encounters:
        try:
            enc_doc = frappe.get_doc("Patient Encounter", enc.name)
            try:
                drug_prescription = enc_doc.drug_prescription
                if drug_prescription:
                    for drug in drug_prescription:
                        med_info = {"prescribed_date": str(enc.encounter_date)}
                        try:
                            med_info["medication"] = drug.drug_name
                        except:
                            med_info["medication"] = None
                        try:
                            med_info["dosage"] = drug.dosage
                        except:
                            med_info["dosage"] = None
                        prescriptions.append(med_info)
            except:
                pass
        except:
            pass
    
    frappe.response.update({
        "status": "success",
        "query_type": query_type,
        "data": {
        "active_prescriptions": prescriptions,
        "count": len(prescriptions)
    }
    })

# =============================================================================
# GET LAB TESTS
# =============================================================================

elif query_type == "get_lab_tests":
    patient_id = parameters.get("patient_id")
    
    if not patient_id:
        frappe.throw("patient_id is required")
    
    lab_tests = frappe.get_all(
        "Lab Test",
        filters={"patient": patient_id},
        fields=["name", "lab_test_name", "status", "result_date", "creation"],
        order_by="creation desc",
        limit=20
    )
    
    frappe.response.update({
        "status": "success",
        "query_type": query_type,
        "data": {
            "lab_tests": lab_tests,
            "count": len(lab_tests)
        }
    })

# =============================================================================
# GET VITAL SIGNS HISTORY
# =============================================================================

elif query_type == "get_vital_signs_history":
    patient_id = parameters.get("patient_id")
    
    if not patient_id:
        frappe.throw("patient_id is required")
    
    vitals = frappe.get_all(
        "Vital Signs",
        filters={"patient": patient_id, "docstatus": ["!=", 2]},
        fields=[
            "name", "signs_date", "signs_time",
            "temperature", "pulse", "respiratory_rate",
            "bp_systolic", "bp_diastolic", "spo2"
        ],
        order_by="signs_date desc",
            limit=20
        )
    
    frappe.response.update({
        "status": "success",
        "query_type": query_type,
        "data": {
            "vital_signs": vitals,
            "count": len(vitals)
        }
    })

# =============================================================================
# GET PATIENT ENCOUNTERS
# =============================================================================

elif query_type == "get_patient_encounters":
    patient_id = parameters.get("patient_id")
    
    if not patient_id:
        frappe.throw("patient_id is required")
    
    filters = {"patient": patient_id, "docstatus": ["!=", 2]}
    
    # Get encounter names first
    encounter_names = frappe.get_all(
        "Patient Encounter",
        filters=filters,
        fields=["name"],
        order_by="encounter_date desc",
        limit=10
    )
    
    # Get ALL encounter data as raw dicts (including all child tables) - NO TRANSFORMATION
    encounters = []
    for enc_name in encounter_names:
        try:
            enc_doc = frappe.get_doc("Patient Encounter", enc_name.name)
            # Use as_dict() to get ALL fields including child tables
            enc_data = enc_doc.as_dict()
            encounters.append(enc_data)
        except Exception as e:
            # If we can't get full doc, skip it
            pass
    
    frappe.response.update({
            "status": "success",
        "query_type": query_type,
        "data": {
            "encounters": encounters,
            "count": len(encounters)
        }
    })

# =============================================================================
# UNKNOWN QUERY TYPE
# =============================================================================

else:  # noqa
    frappe.response.update({
        "status": "error",
        "message": f"Query type '{query_type}' not implemented"
    })

# =============================================================================
# END OF SCRIPT
# =============================================================================
