#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Suppression des warnings inutiles pour interface propre
Cree par Maman Margot pour PHOBOS - 31 Janvier 2026
"""

import warnings
import os
import sys

def suppress_all_warnings():
    """Supprime tous les warnings non-critiques pour interface propre"""
    
    # 1. Warnings Python standards
    warnings.filterwarnings('ignore')
    
    # 2. Warnings FutureWarning (deprecations)
    warnings.filterwarnings('ignore', category=FutureWarning)
    
    # 3. Warnings UserWarning
    warnings.filterwarnings('ignore', category=UserWarning)
    
    # 4. Warnings DeprecationWarning
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    
    # 5. Variables d'environnement pour supprimer warnings specifiques
    
    # TensorFlow/PyTorch
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Supprime logs TensorFlow
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # Utilise GPU 0 uniquement
    
    # Triton (optimisations CUDA) - FORCE LA SUPPRESSION
    os.environ['TRITON_SUPPRESS_WARNINGS'] = '1'
    os.environ['TRITON_TELEMETRY_DISABLE'] = '1'
    os.environ['XFORMERS_FORCE_DISABLE_TRITON'] = '1'  # Force desactivation Triton
    
    # Transformers/Diffusers
    os.environ['TRANSFORMERS_VERBOSITY'] = 'error'  # Seulement erreurs
    os.environ['DIFFUSERS_VERBOSITY'] = 'error'
    os.environ['TOKENIZERS_PARALLELISM'] = 'false'  # Desactive parallelisme tokenizers
    
    # PyTorch
    os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:512'
    
    # Desactiver les logs torch.distributed
    os.environ['TORCH_DISTRIBUTED_DEBUG'] = 'OFF'
    
    # NumPy
    import numpy as np
    np.seterr(all='ignore')  # Ignore warnings numpy
    
    print("[OK] Warnings supprimes pour interface propre")

def configure_clean_output():
    """Configure la sortie console pour etre propre et lisible"""
    
    # Supprimer les warnings AVANT tout autre import
    suppress_all_warnings()
    
    print("[OK] Configuration sortie console terminee")

