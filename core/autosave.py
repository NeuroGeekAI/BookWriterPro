"""
Auto-save - Sauvegarde automatique périodique
"""
import threading
import time
from typing import Callable

class AutoSave:
    """Gère la sauvegarde automatique"""
    
    def __init__(self, save_callback: Callable, interval: int = 30):
        self.save_callback = save_callback
        self.interval = interval  # secondes
        self.running = False
        self.thread = None
        self.last_save_time = 0
    
    def start(self):
        """Démarre la sauvegarde automatique"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._auto_save_loop, daemon=True)
            self.thread.start()
    
    def stop(self):
        """Arrête la sauvegarde automatique"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
    
    def _auto_save_loop(self):
        """Boucle de sauvegarde automatique"""
        while self.running:
            time.sleep(self.interval)
            if self.running:
                try:
                    self.save_callback()
                    self.last_save_time = time.time()
                except Exception as e:
                    print(f"Erreur auto-save: {e}")
    
    def get_last_save_elapsed(self) -> int:
        """Retourne le temps écoulé depuis la dernière sauvegarde (en secondes)"""
        if self.last_save_time == 0:
            return 0
        return int(time.time() - self.last_save_time)

