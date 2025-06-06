from pathlib import Path
import os
import sys
import tempfile
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from .models import Family, Species
from .forms import FamilyForm, SpeciesForm
from django.contrib import messages
import json
import torch
from ultralytics.nn.tasks import DetectionModel
from ultralytics.nn.modules.conv import Conv, Concat
from ultralytics.nn.modules.block import C2f, SPPF, Bottleneck, DFL
from ultralytics.nn.modules.head import Detect
from torch.nn.modules.container import Sequential, ModuleList
from torch.nn.modules.conv import Conv2d
from torch.nn.modules.batchnorm import BatchNorm2d
from torch.nn.modules.activation import SiLU
from torch.nn.modules.upsampling import Upsample
from torch.nn.modules.pooling import MaxPool2d
from torch.nn.modules.linear import Linear

# Get the base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Update the model paths to use Path objects
custom_model_path = BASE_DIR / "runs" / "detect" / "train4" / "weights" / "best.pt"
default_model_path = BASE_DIR / "models" / "yolov8x.pt"

model = None
model_load_error = None
model_in_use = None

def setup_model_loading():
    """Setup safe globals for model loading based on PyTorch version."""
    try:
        # Get PyTorch version
        torch_version = torch.__version__
        major_version = int(torch_version.split('.')[0])
        minor_version = int(torch_version.split('.')[1])

        # Define all required safe globals
        safe_globals = [
            DetectionModel,
            Conv,
            Concat,
            C2f,
            SPPF,
            Bottleneck,
            DFL,
            Detect,
            Sequential,
            ModuleList,
            Conv2d,
            BatchNorm2d,
            SiLU,
            Upsample,
            MaxPool2d,
            Linear
        ]

        # For PyTorch 2.6 and above
        if major_version >= 2 and minor_version >= 6:
            if hasattr(torch.serialization, 'add_safe_globals'):
                torch.serialization.add_safe_globals(safe_globals)
            else:
                # Fallback for older PyTorch versions
                import warnings
                warnings.warn("PyTorch version doesn't support add_safe_globals. Using alternative loading method.")
                return False
        return True
    except Exception as e:
        print(f"Error setting up model loading: {str(e)}")
        return False

# Check which model file exists and set the path accordingly
if custom_model_path.exists():
    model_path = str(custom_model_path)
    model_in_use = "Custom-trained model (Chinese Egret)"
elif default_model_path.exists():
    model_path = str(default_model_path)
    model_in_use = "Base YOLOv8x model (generic)"
else:
    model_path = None
    model_load_error = (
        f"No model file found. Please provide either a custom-trained model at '{custom_model_path}' "
        f"or a base model at '{default_model_path}'. See the README for instructions."
    )

if model_path and not model_load_error:
    try:
        from ultralytics import YOLO
        
        # Setup model loading with safe globals
        use_safe_globals = setup_model_loading()
        
        # Load model with appropriate settings
        if use_safe_globals:
            model = YOLO(model_path, task='detect')
        else:
            # Fallback method for older PyTorch versions
            model = YOLO(model_path, task='detect', weights_only=False)
            
    except ImportError:
        model_load_error = (
            "The 'ultralytics' package is not installed. If you only want to run inference, make sure you installed only the required packages. "
            "If you want to train or update the model, install training dependencies with: pip install -r requirements-dev.txt"
        )
    except Exception as e:
        model_load_error = f"Error loading YOLO model: {str(e)}"

def dashboard(request):
    """Main dashboard view"""
    return render(request, 'admindashboard/dashboard.html')

def logout_view(request):
    """Logout view"""
    logout(request)
    return redirect('login')

def bird_identification_view(request):
    """Bird identification view (legacy name)"""
    return render(request, 'admindashboard/bird_identification.html')

def identify_bird(request):
    """Bird identification view (new name)"""
    return render(request, 'admindashboard/bird_identification.html')

@csrf_exempt
def process_bird_image(request):
    if model_load_error:
        return JsonResponse({'error': model_load_error}, status=500)
    if request.method == 'POST' and request.FILES.get('image'):
        # Get image file from request
        image_file = request.FILES['image']
        
        # Create a temporary file to store the uploaded image
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            temp_path = temp_file.name
            for chunk in image_file.chunks():
                temp_file.write(chunk)
        try:
            # Run inference with YOLO v8 on the temporary image file.
            results = model(temp_path, conf=0.5, iou=0.8)
        except Exception as e:
            os.remove(temp_path)
            return JsonResponse({'error': f'Error during model inference: {str(e)}'}, status=500)
        # Process results
        detections = []
        for result in results:
            for box in result.boxes:
                detections.append({
                    'class': result.names[int(box.cls[0])],  # Class name (species)
                    'confidence': float(box.conf[0]),  # Confidence score
                    'coordinates': box.xyxy[0].tolist()  # Bounding box coordinates
                })
        # Clean up temporary file
        os.remove(temp_path)
        # Return JSON response with detections
        return JsonResponse({'detections': detections})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def bird_list(request):
    """Main view for displaying bird families and species"""
    families = Family.objects.filter(is_archived=False).order_by('name')
    family_form = FamilyForm()
    species_form = SpeciesForm()
    
    context = {
        'families': families,
        'family_form': family_form,
        'species_form': species_form,
    }
    return render(request, 'admindashboard/bird_list.html', context)

@require_POST
def add_family(request):
    """Add a new bird family"""
    form = FamilyForm(request.POST)
    if form.is_valid():
        family = form.save(commit=False)
        family.is_archived = False
        family.save()
        messages.success(request, 'Family added successfully!')
    else:
        messages.error(request, 'Error adding family. Please check the form.')
    return redirect('admindashboard:bird_list')

@require_POST
def add_species(request, family_id):
    """Add a new species to a family"""
    family = get_object_or_404(Family, id=family_id)
    form = SpeciesForm(request.POST)
    
    if form.is_valid():
        species = form.save(commit=False)
        species.family = family
        species.is_archived = False
        species.save()
        messages.success(request, 'Species added successfully!')
    else:
        messages.error(request, 'Error adding species. Please check the form.')
    
    return redirect('admindashboard:bird_list')

def edit_family(request, family_id):
    """Edit an existing bird family"""
    family = get_object_or_404(Family, id=family_id)
    
    if request.method == 'POST':
        form = FamilyForm(request.POST, instance=family)
        if form.is_valid():
            form.save()
            messages.success(request, 'Family updated successfully!')
            return redirect('admindashboard:bird_list')
    else:
        form = FamilyForm(instance=family)
    
    return render(request, 'admindashboard/edit_family.html', {
        'form': form,
        'family': family
    })

def edit_species(request, species_id):
    """Edit an existing species"""
    species = get_object_or_404(Species, id=species_id)
    
    if request.method == 'POST':
        form = SpeciesForm(request.POST, instance=species)
        if form.is_valid():
            form.save()
            messages.success(request, 'Species updated successfully!')
            return redirect('admindashboard:bird_list')
    else:
        form = SpeciesForm(instance=species)
    
    return render(request, 'admindashboard/edit_species.html', {
        'form': form,
        'species': species
    })

@require_POST
def archive_family(request, family_id):
    """Archive a bird family"""
    family = get_object_or_404(Family, id=family_id)
    family.is_archived = True
    family.save()
    messages.success(request, 'Family archived successfully!')
    return redirect('admindashboard:bird_list')

@require_POST
def archive_species(request, species_id):
    """Archive a species"""
    species = get_object_or_404(Species, id=species_id)
    species.is_archived = True
    species.save()
    messages.success(request, 'Species archived successfully!')
    return redirect('admindashboard:bird_list')

@require_POST
def restore_family(request, family_id):
    """Restore an archived family"""
    family = get_object_or_404(Family, id=family_id)
    family.is_archived = False
    family.save()
    messages.success(request, 'Family restored successfully!')
    return redirect('admindashboard:bird_list')

@require_POST
def restore_species(request, species_id):
    """Restore an archived species"""
    species = get_object_or_404(Species, id=species_id)
    species.is_archived = False
    species.save()
    messages.success(request, 'Species restored successfully!')
    return redirect('admindashboard:bird_list')

def get_species(request, family_id):
    """Get all species for a family (AJAX endpoint)"""
    family = get_object_or_404(Family, id=family_id)
    species = Species.objects.filter(family=family, is_archived=False).order_by('name')
    data = [{
        'id': s.id,
        'name': s.name,
        'scientific_name': s.scientific_name,
        'iucn_status': s.iucn_status
    } for s in species]
    return JsonResponse(data, safe=False)

def help_view(request):
    """Help page view"""
    return render(request, "admindashboard/help.html")