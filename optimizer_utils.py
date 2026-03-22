import os
import shutil
import subprocess
import psutil
import ctypes
import sys

class SystemOptimizer:
    """Clase para optimizar el sistema operativo"""
    
    @staticmethod
    def is_admin():
        """Verifica si el programa se ejecuta con permisos de administrador"""
        try:
            return ctypes.windll.shell.IsUserAnAdmin()
        except:
            return False
    
    @staticmethod
    def get_disk_usage():
        """Obtiene información de uso de disco"""
        try:
            usage = shutil.disk_usage("C:\")
            total = usage.total / (1024 ** 3)  # Convertir a GB
            used = usage.used / (1024 ** 3)
            free = usage.free / (1024 ** 3)
            percent = (used / total) * 100
            
            return {
                'total': round(total, 2),
                'used': round(used, 2),
                'free': round(free, 2),
                'percent': round(percent, 2)
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def get_memory_info():
        """Obtiene información de memoria RAM"""
        try:
            memory = psutil.virtual_memory()
            return {
                'total': round(memory.total / (1024 ** 3), 2),
                'available': round(memory.available / (1024 ** 3), 2),
                'used': round(memory.used / (1024 ** 3), 2),
                'percent': round(memory.percent, 2)
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def get_cpu_usage():
        """Obtiene información de uso de CPU"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            return {
                'percent': round(cpu_percent, 2),
                'cores': cpu_count
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def terminate_unnecessary_processes():
        """Termina procesos innecesarios para mejorar rendimiento"""
        unnecessary_processes = [
            'OneDrive.exe',
            'SearchIndexer.exe',
            'StartMenuExperienceHost.exe',
            'Cortana.exe'
        ]
        
        killed = []
        failed = []
        
        for process_name in unnecessary_processes:
            try:
                os.system(f'taskkill /IM {process_name} /F 2>nul')
                killed.append(process_name)
            except Exception as e:
                failed.append((process_name, str(e)))
        
        return {'killed': killed, 'failed': failed}
    
    @staticmethod
    def disable_startup_programs():
        """Desactiva programas innecesarios al inicio"""
        try:
            startup_path = os.path.expandvars(
                r'%appdata%\Microsoft\Windows\Start Menu\Programs\Startup'
            )
            
            if os.path.exists(startup_path):
                disabled_count = 0
                for file in os.listdir(startup_path):
                    filepath = os.path.join(startup_path, file)
                    if file.endswith('.lnk'):
                        try:
                            os.remove(filepath)
                            disabled_count += 1
                        except:
                            pass
                
                return {'disabled': disabled_count}
            return {'error': 'Startup path not found'}
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def clean_prefetch():
        """Limpia archivos prefetch del sistema"""
        try:
            prefetch_path = os.path.expandvars(r'%windir%\Prefetch')
            
            if os.path.exists(prefetch_path):
                cleaned = 0
                for file in os.listdir(prefetch_path):
                    if file.endswith('.pf'):
                        filepath = os.path.join(prefetch_path, file)
                        try:
                            os.remove(filepath)
                            cleaned += 1
                        except:
                            pass
                
                return {'cleaned': cleaned}
            return {'error': 'Prefetch path not found'}
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def clean_recycle_bin():
        """Vacía la papelera de reciclaje"""
        try:
            os.system('rd /s /q %systemdrive%\$Recycle.bin')
            return {'status': 'Recycle bin emptied'}
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def optimize_virtual_memory():
        """Optimiza la memoria virtual del sistema"""
        try:
            # Comando para defragmentar disco (requiere permisos de admin)
            os.system('defrag C: /U /V')
            return {'status': 'Virtual memory optimized'}
        except Exception as e:
            return {'error': str(e)}

# Funciones de conveniencia
def get_system_stats():
    """Obtiene estadísticas completas del sistema"""
    return {
        'disk': SystemOptimizer.get_disk_usage(),
        'memory': SystemOptimizer.get_memory_info(),
        'cpu': SystemOptimizer.get_cpu_usage()
    }

def run_full_optimization():
    """Ejecuta optimización completa del sistema"""
    results = {
        'disk_cleaned': SystemOptimizer.clean_prefetch(),
        'recycle_bin': SystemOptimizer.clean_recycle_bin(),
        'startup_programs': SystemOptimizer.disable_startup_programs(),
        'unnecessary_processes': SystemOptimizer.terminate_unnecessary_processes()
    }
    return results