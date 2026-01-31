"""
Détection et correction automatique des erreurs de traduction
Module intelligent pour Book Writer Pro
Créé par Maman pour PHOBOS - 22/01/2026
"""
import re
from typing import Dict, List, Tuple

class TextCleaner:
    """Détecte et corrige automatiquement les erreurs de traduction"""
    
    def __init__(self):
        """Initialise le nettoyeur de texte"""
        self.max_repetition_threshold = 5  # Nombre max de répétitions acceptables
        
    def detect_errors(self, text: str, lang: str) -> Dict[str, any]:
        """
        Détecte les erreurs dans un texte
        
        Returns:
            Dict avec :
            - has_errors: bool
            - errors: List[Dict] avec type, position, contexte
            - can_auto_fix: bool
        """
        if not text or not text.strip():
            return {
                'has_errors': False,
                'errors': [],
                'can_auto_fix': False
            }
        
        errors = []
        
        # 1. Détecter répétitions excessives
        repetition_errors = self._detect_repetitions(text)
        errors.extend(repetition_errors)
        
        # 2. Détecter caractères problématiques pour CID
        if lang in ['zh', 'ja', 'ko']:
            cid_errors = self._detect_cid_problems(text, lang)
            errors.extend(cid_errors)
        
        # 3. Détecter carrés/caractères manquants
        missing_chars = self._detect_missing_chars(text)
        errors.extend(missing_chars)
        
        # Déterminer si correction auto possible
        can_auto_fix = all(e['auto_fixable'] for e in errors)
        
        return {
            'has_errors': len(errors) > 0,
            'errors': errors,
            'can_auto_fix': can_auto_fix,
            'error_count': len(errors)
        }
    
    def _detect_repetitions(self, text: str) -> List[Dict]:
        """Détecte les répétitions excessives de mots/phrases"""
        errors = []
        
        # Pattern : mot ou groupe de mots répété plus de X fois consécutivement
        # Exemple : "Like Like Like Like Like"
        
        words = text.split()
        
        for i in range(len(words)):
            if i + self.max_repetition_threshold >= len(words):
                break
            
            # Vérifier si le mot actuel est répété
            current_word = words[i]
            repetition_count = 1
            
            for j in range(i + 1, min(i + 50, len(words))):  # Check jusqu'à 50 mots
                if words[j] == current_word:
                    repetition_count += 1
                else:
                    break
            
            if repetition_count > self.max_repetition_threshold:
                # Extraire contexte
                start_idx = max(0, i - 5)
                end_idx = min(len(words), i + repetition_count + 5)
                context = ' '.join(words[start_idx:end_idx])
                
                errors.append({
                    'type': 'excessive_repetition',
                    'word': current_word,
                    'count': repetition_count,
                    'position': i,
                    'context': context,
                    'auto_fixable': True,
                    'severity': 'high',
                    'message': f'Le mot "{current_word}" est répété {repetition_count} fois consécutivement'
                })
                
                # Éviter de détecter la même répétition plusieurs fois
                break
        
        return errors
    
    def _detect_cid_problems(self, text: str, lang: str) -> List[Dict]:
        """Détecte les caractères non-CID qui poseront problème en PDF"""
        errors = []
        
        # Caractères problématiques pour CID
        problematic_chars = {
            '·': 'point médian',
            '•': 'bullet',
            '–': 'tiret cadratin',
            '—': 'tiret long',
            ''': 'guillemet courbe',
            ''': 'guillemet courbe',
            '"': 'guillemet double courbe',
            '"': 'guillemet double courbe',
            '…': 'points de suspension',
            '€': 'symbole euro',
            '£': 'symbole livre',
            '©': 'copyright',
            '®': 'registered',
            '™': 'trademark',
        }
        
        for char, name in problematic_chars.items():
            if char in text:
                count = text.count(char)
                # Trouver première occurrence pour contexte
                idx = text.index(char)
                start = max(0, idx - 20)
                end = min(len(text), idx + 20)
                context = text[start:end]
                
                errors.append({
                    'type': 'cid_incompatible_char',
                    'char': char,
                    'char_name': name,
                    'count': count,
                    'context': context,
                    'auto_fixable': True,
                    'severity': 'medium',
                    'message': f'Caractère "{char}" ({name}) incompatible avec police CID ({lang.upper()})'
                })
        
        return errors
    
    def _detect_missing_chars(self, text: str) -> List[Dict]:
        """Détecte les caractères de remplacement (carrés, ?)"""
        errors = []
        
        # Pattern pour carrés/caractères manquants
        # Note : □ et � sont des indicateurs de caractères manquants
        missing_patterns = ['□', '�', '\ufffd']
        
        for pattern in missing_patterns:
            if pattern in text:
                count = text.count(pattern)
                idx = text.index(pattern)
                start = max(0, idx - 20)
                end = min(len(text), idx + 20)
                context = text[start:end]
                
                errors.append({
                    'type': 'missing_character',
                    'char': pattern,
                    'count': count,
                    'context': context,
                    'auto_fixable': False,  # Difficile de corriger automatiquement
                    'severity': 'high',
                    'message': f'Caractère manquant/non supporté détecté ({count} occurrence(s))'
                })
        
        return errors
    
    def auto_fix(self, text: str, lang: str) -> Tuple[str, List[str]]:
        """
        Applique corrections automatiques
        
        Returns:
            (texte_corrigé, liste_corrections_appliquées)
        """
        if not text or not text.strip():
            return text, []
        
        corrections = []
        fixed_text = text
        
        # 1. Corriger répétitions excessives
        fixed_text, rep_corrections = self._fix_repetitions(fixed_text)
        corrections.extend(rep_corrections)
        
        # 2. Corriger caractères CID
        if lang in ['zh', 'ja', 'ko']:
            fixed_text, cid_corrections = self._fix_cid_chars(fixed_text)
            corrections.extend(cid_corrections)
        
        return fixed_text, corrections
    
    def _fix_repetitions(self, text: str) -> Tuple[str, List[str]]:
        """Corrige les répétitions excessives EN PRÉSERVANT LA MISE EN FORME"""
        corrections = []
        
        # Travailler ligne par ligne pour préserver les sauts de ligne
        lines = text.split('\n')
        fixed_lines = []
        
        for line in lines:
            if not line.strip():
                # Ligne vide : conserver telle quelle
                fixed_lines.append(line)
                continue
            
            # Traiter la ligne
            words = line.split()
            fixed_words = []
            i = 0
            
            while i < len(words):
                current_word = words[i]
                repetition_count = 1
                
                # Compter répétitions consécutives
                while i + repetition_count < len(words) and words[i + repetition_count] == current_word:
                    repetition_count += 1
                
                if repetition_count > self.max_repetition_threshold:
                    # Garder seulement 1 occurrence
                    fixed_words.append(current_word)
                    if len(corrections) == 0 or current_word not in corrections[-1]:  # Éviter doublons
                        corrections.append(
                            f'Répétition excessive "{current_word}" ({repetition_count}x) → réduite à 1x'
                        )
                    i += repetition_count
                else:
                    # Garder toutes les occurrences (répétition normale)
                    for _ in range(repetition_count):
                        fixed_words.append(current_word)
                    i += repetition_count
            
            # Reconstruire la ligne avec les espaces d'origine préservés autant que possible
            fixed_line = ' '.join(fixed_words)
            fixed_lines.append(fixed_line)
        
        # Reconstruire le texte avec les sauts de ligne originaux
        fixed_text = '\n'.join(fixed_lines)
        return fixed_text, corrections
    
    def _fix_cid_chars(self, text: str) -> Tuple[str, List[str]]:
        """Corrige les caractères incompatibles CID (PRÉSERVE MISE EN FORME)"""
        corrections = []
        fixed_text = text
        
        # Remplacements simples qui préservent la structure
        replacements = {
            '·': ' ',
            '•': ' ',
            '–': '-',
            '—': '-',
            ''': "'",
            ''': "'",
            '"': '"',
            '"': '"',
            '…': '...',
            '€': 'EUR',
            '£': 'GBP',
            '§': '',
            '©': '(C)',
            '®': '(R)',
            '™': '(TM)',
        }
        
        # Simple remplacement caractère par caractère
        # Ne touche PAS aux sauts de ligne, tabs, ou espaces multiples
        for old_char, new_char in replacements.items():
            if old_char in fixed_text:
                count = fixed_text.count(old_char)
                fixed_text = fixed_text.replace(old_char, new_char)
                corrections.append(
                    f'Caractère "{old_char}" ({count}x) → remplacé par "{new_char}"'
                )
        
        return fixed_text, corrections
    
    def get_fix_suggestions(self, errors: List[Dict]) -> List[Dict]:
        """
        Génère des suggestions de correction pour erreurs non auto-fixables
        
        Returns:
            List[Dict] avec suggestions de correction manuelle
        """
        suggestions = []
        
        for error in errors:
            if not error['auto_fixable']:
                if error['type'] == 'missing_character':
                    suggestions.append({
                        'error': error,
                        'suggestions': [
                            'Retraduire le texte avec un autre outil (Google Translate)',
                            'Éditer manuellement le texte',
                            'Copier depuis une version qui fonctionne',
                            'Accepter la limitation et expliquer aux lecteurs'
                        ],
                        'recommended': 'Retraduire avec Google Translate'
                    })
        
        return suggestions
