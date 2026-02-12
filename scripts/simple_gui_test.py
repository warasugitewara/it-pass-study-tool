#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple GUI Test - Module and Window Initialization
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_pyside6():
    """Test PySide6 imports"""
    try:
        from PySide6.QtWidgets import QApplication, QMainWindow
        from PySide6.QtCore import Qt
        print("OK: PySide6 imports successful")
        return True
    except Exception as e:
        print(f"FAIL: PySide6 import error: {e}")
        return False

def test_modules():
    """Test core module imports"""
    try:
        from src.db.database import DatabaseManager
        from src.utils.data_manager import DataManager
        from src.core.quiz_engine import QuizEngine
        from src.core.statistics import StatisticsEngine
        from src.ui.main_window import MainWindow
        print("OK: All modules loaded successfully")
        return True
    except Exception as e:
        print(f"FAIL: Module import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database():
    """Test database initialization"""
    try:
        from src.db.database import DatabaseManager
        from src.db.models import Question, Category, Year
        
        db_manager = DatabaseManager()
        session = db_manager.get_session()
        
        q_count = session.query(Question).count()
        c_count = session.query(Category).count()
        y_count = session.query(Year).count()
        
        print(f"OK: Database initialized - Q:{q_count} C:{c_count} Y:{y_count}")
        return True
    except Exception as e:
        print(f"FAIL: Database test error: {e}")
        return False

def test_window():
    """Test MainWindow creation"""
    try:
        from PySide6.QtWidgets import QApplication
        from src.ui.main_window import MainWindow
        
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        window = MainWindow()
        print(f"OK: MainWindow created - Title: {window.windowTitle()}, Size: {window.width()}x{window.height()}")
        return True
    except Exception as e:
        print(f"FAIL: Window creation error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=== GUI Test Suite ===\n")
    
    results = []
    results.append(("PySide6", test_pyside6()))
    results.append(("Module Load", test_modules()))
    results.append(("Database", test_database()))
    results.append(("Window", test_window()))
    
    print("\n=== Results ===")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"[{status}] {name}")
    
    print(f"\nTotal: {passed}/{total} passed")
    sys.exit(0 if passed == total else 1)
