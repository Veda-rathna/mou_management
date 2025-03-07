from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Company, MOU
from .cloud_storage import upload_to_cloudinary
from datetime import datetime
from rest_framework.decorators import api_view
from django.core.files.storage import default_storage
from django.conf import settings
import os
import time
import json

class UploadMOUView(APIView):
    def post(self, request):
        company_id = request.data.get("company_id")
        pdf = request.FILES.get("pdf")
        signature = request.FILES.get("signature")
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")

        if not company_id or not pdf or not signature or not start_date or not end_date:
            return Response({"error": "Missing required fields (company_id, pdf, signature, start_date, end_date)."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response({"error": "Company not found. Please provide a valid company ID."},
                            status=status.HTTP_404_NOT_FOUND)

        try:
            # Convert dates from string to actual date objects
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."},
                            status=status.HTTP_400_BAD_REQUEST)

        pdf_url = upload_to_cloudinary(pdf)
        signature_url = upload_to_cloudinary(signature)

        mou = MOU.objects.create(
            company=company,
            pdf_url=pdf_url,
            signature_url=signature_url,
            start_date=start_date,
            end_date=end_date
        )

        return Response({"mou_id": mou.id, "message": "Upload successful"},
                        status=status.HTTP_201_CREATED)

@api_view(['POST'])
def upload_mou(request):
    try:
        # Get form data
        company_name = request.POST.get('company_name')
        company_id = request.POST.get('company_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        pdf = request.FILES.get('pdf')
        signature = request.FILES.get('signature')

        # Validate data
        if not all([company_name, company_id, start_date, end_date, pdf, signature]):
            return Response({'error': 'All fields are required'}, status=400)

        # Create directories
        mou_dir = os.path.join(settings.MEDIA_ROOT, 'mous')
        sig_dir = os.path.join(settings.MEDIA_ROOT, 'signatures')
        os.makedirs(mou_dir, exist_ok=True)
        os.makedirs(sig_dir, exist_ok=True)

        # Save files with company_id prefix
        pdf_name = f"{company_id}_{pdf.name}"
        sig_name = f"{company_id}_{signature.name}"

        pdf_path = os.path.join(mou_dir, pdf_name)
        sig_path = os.path.join(sig_dir, sig_name)

        with open(pdf_path, 'wb+') as f:
            for chunk in pdf.chunks():
                f.write(chunk)

        with open(sig_path, 'wb+') as f:
            for chunk in signature.chunks():
                f.write(chunk)

        # Save record data
        records_file = os.path.join(settings.MEDIA_ROOT, 'records.json')
        records = []
        if os.path.exists(records_file):
            with open(records_file, 'r') as f:
                records = json.load(f)

        records.append({
            'company_name': company_name,
            'company_id': company_id,
            'start_date': start_date,
            'end_date': end_date,
            'pdf_file': pdf_name,
            'signature_file': sig_name
        })

        with open(records_file, 'w') as f:
            json.dump(records, f)

        return Response({'message': 'Upload successful'})

    except Exception as e:
        print("Upload error:", str(e))
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def list_mous(request):
    try:
        records_file = os.path.join(settings.MEDIA_ROOT, 'records.json')
        if os.path.exists(records_file):
            with open(records_file, 'r') as f:
                records = json.load(f)
        else:
            records = []

        return Response({'records': records})
    except Exception as e:
        return Response({'error': str(e)}, status=500)
