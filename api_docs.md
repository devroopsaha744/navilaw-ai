
---

# API Documentation for Legal Assistance

## Overview
This API provides legal assistance by allowing users to upload PDF documents and submit queries for various legal services, including legal advisory, report generation, and case outcome prediction. 

## Base URL
```
https://navilaw-ai.onrender.com/legal-assistance/
```

## HTTP Method
`POST`

## Endpoint
`/legal-assistance/`

## Request Parameters

### Form Parameters

| Parameter | Type        | Required | Description |
|-----------|-------------|----------|-------------|
| `query`   | `string`    | Yes      | A string representing the legal query the user wishes to ask. |
| `option`  | `string`    | Yes      | A string indicating the type of legal assistance required. Possible values are "Legal Advisory", "Legal Report Generation", and "Case Outcome Prediction". |
| `files`   | `List[UploadFile]` | Yes      | A list of PDF files containing legal documents to be analyzed. |

### Example Request
```http
POST /legal-assistance/ HTTP/1.1
Host: https://navilaw-ai.onrender.com/
Content-Type: multipart/form-data

--boundary
Content-Disposition: form-data; name="query"

What are the possible outcomes of my case?
--boundary
Content-Disposition: form-data; name="option"

Case Outcome Prediction
--boundary
Content-Disposition: form-data; name="files"; filename="legal_case.pdf"
Content-Type: application/pdf

<PDF file content>
--boundary--
```

## Response Format

### Successful Response
- **Status Code:** `200 OK`
- **Content-Type:** `application/json`

#### Response Body
- **For Legal Advisory:**
```json
{
    "result": "Based on the provided documents and the legal query, here are the considerations to keep in mind regarding your case..."
}
```

- **For Legal Report Generation:**
```json
{
    "report": "Legal Report:\n\n1. Introduction\n2. Case Details\n3. Analysis\n4. Conclusion"
}
```

- **For Case Outcome Prediction:**
```json
{
    "prediction": "Based on the analysis of the legal precedents and the court's decision in a similar case, there is a 70% chance of a favorable outcome for Fast Retail in their lawsuit against Tech Solutions. The court ruled in favor of Fast Retail, ordering Tech Solutions to pay damages of ₹60,00,000. The uncertainty lies in the court's consideration of not all claimed damages were directly attributable to Tech Solutions' breach. It's crucial to consider this when predicting the outcome."
}
```

### Error Response
- **Status Code:** `400 Bad Request`
- **Content-Type:** `application/json`

#### Response Body
```json
{
    "detail": "Please upload at least one PDF file."
}
```

#### Possible Error Messages
- **If no files are uploaded:**
```json
{
    "detail": "Please upload at least one PDF file."
}
```

- **If no query is provided:**
```json
{
    "detail": "Please enter a query."
}
```

- **If an invalid option is selected:**
```json
{
    "detail": "Invalid option selected."
}
```

## Sample Inputs and Outputs

### 1. Legal Advisory
#### Request
```http
POST /legal-assistance/ 
```
With the following form data:
- **query:** "What are the implications of the new law on my case?"
- **option:** "Legal Advisory"
- **files:** (Upload PDF: `law_document.pdf`)

#### Response
```json
{
    "result": "The new law may affect your case in several ways, particularly regarding..."
}
```

### 2. Legal Report Generation
#### Request
```http
POST /legal-assistance/ 
```
With the following form data:
- **query:** "Generate a report on the recent legal changes."
- **option:** "Legal Report Generation"
- **files:** (Upload PDF: `legal_changes.pdf`)

#### Response
```json
{
    "report": "Legal Report:\n\n1. Introduction\n2. Summary of Changes\n3. Implications\n4. Conclusion"
}
```

### 3. Case Outcome Prediction
#### Request
```http
POST /legal-assistance/ 
```
With the following form data:
- **query:** "What is the likelihood of winning my case based on previous rulings?"
- **option:** "Case Outcome Prediction"
- **files:** (Upload PDF: `previous_rulings.pdf`)

#### Response
```json
{
    "prediction": "Based on the analysis of the legal precedents and the court's decision in a similar case, there is a 70% chance of a favorable outcome for Fast Retail in their lawsuit against Tech Solutions..."
}
```

---


