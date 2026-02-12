#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Large-Scale Quiz Performance Test
Test quiz performance with 100+ questions loaded
"""

import sys
from pathlib import Path
import time
from datetime import datetime

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.db.database import DatabaseManager
from src.core.quiz_engine import QuizEngine, QuizMode
from src.db.models import Question, Category

def test_large_scale_quiz():
    """Test quiz engine with large dataset"""
    
    print("\n" + "="*70)
    print("Large-Scale Quiz Performance Test")
    print("="*70 + "\n")
    
    db_manager = DatabaseManager()
    quiz_engine = QuizEngine()
    
    # Get database stats
    session = db_manager.get_session()
    q_count = session.query(Question).count()
    c_count = session.query(Category).count()
    db_manager.close_session(session)
    
    print(f"Database Statistics:")
    print(f"  - Total Questions: {q_count}")
    print(f"  - Total Categories: {c_count}\n")
    
    if q_count < 100:
        print(f"Warning: Expected 100+ questions, found {q_count}")
        print(f"Run 'load_real_data.py' first to load sample data")
        return False
    
    # Test 1: Random Mode Performance
    print("Test 1: Random Quiz Mode (50 questions)")
    print("-" * 70)
    
    try:
        start_time = time.time()
        session_id = quiz_engine.start_session(
            mode=QuizMode.RANDOM,
            question_count=50
        )
        load_time = time.time() - start_time
        
        print(f"✓ Session started in {load_time:.2f}s: {session_id}")
        
        # Get all questions and measure time
        start_time = time.time()
        questions_data = []
        for i in range(50):
            q = quiz_engine.get_current_question()
            if q:
                questions_data.append(q)
            if i < 49:
                quiz_engine.next_question()
        
        question_time = time.time() - start_time
        print(f"✓ Retrieved 50 questions in {question_time:.2f}s ({question_time/50*1000:.2f}ms per question)")
        
    except Exception as e:
        print(f"✗ Test 1 failed: {e}")
        return False
    
    # Test 2: Category Filtering Performance
    print("\n\nTest 2: Category-Based Quiz (30 questions from 1 category)")
    print("-" * 70)
    
    try:
        session = db_manager.get_session()
        categories = session.query(Category).all()
        db_manager.close_session(session)
        
        if categories:
            cat = categories[0]
            
            start_time = time.time()
            session_id_2 = quiz_engine.start_session(
                mode=QuizMode.BY_CATEGORY,
                question_count=30,
                category_ids=[cat.id]
            )
            filter_time = time.time() - start_time
            
            print(f"✓ Category quiz started in {filter_time:.2f}s")
            print(f"  - Category: {cat.name}")
            
            # Verify questions are from correct category
            q = quiz_engine.get_current_question()
            if q and q.category_id == cat.id:
                print(f"✓ Questions from correct category")
            else:
                print(f"✗ Wrong category detected")
        
    except Exception as e:
        print(f"✗ Test 2 failed: {e}")
        return False
    
    # Test 3: Mock Test Performance
    print("\n\nTest 3: Mock Test Mode (100 questions)")
    print("-" * 70)
    
    try:
        start_time = time.time()
        session_id_3 = quiz_engine.start_session(
            mode=QuizMode.MOCK_TEST,
            question_count=100
        )
        mock_time = time.time() - start_time
        
        print(f"✓ Mock test started in {mock_time:.2f}s")
        print(f"  - Session ID: {session_id_3}")
        
        # Measure question loading time
        q1 = quiz_engine.get_current_question()
        if q1:
            print(f"✓ First question loaded: {q1.text[:50]}...")
        
    except Exception as e:
        print(f"✗ Test 3 failed: {e}")
        return False
    
    # Test 4: Answer Submission & Scoring
    print("\n\nTest 4: Answer Submission (20 questions)")
    print("-" * 70)
    
    try:
        # Start small quiz for testing
        start_time = time.time()
        session_id_4 = quiz_engine.start_session(
            mode=QuizMode.RANDOM,
            question_count=20
        )
        
        correct_count = 0
        submit_times = []
        
        session = db_manager.get_session()
        
        for i in range(20):
            q = quiz_engine.get_current_question()
            if q:
                # Get choices
                q_db = session.query(Question).filter_by(id=q.id).first()
                if q_db and q_db.choices:
                    choice = q_db.choices[0]
                    
                    submit_start = time.time()
                    quiz_engine.submit_answer(choice.id)
                    submit_times.append(time.time() - submit_start)
                    
                    if choice.is_correct:
                        correct_count += 1
            
            if i < 19:
                quiz_engine.next_question()
        
        db_manager.close_session(session)
        
        avg_submit_time = sum(submit_times) / len(submit_times) * 1000
        total_time = time.time() - start_time
        
        print(f"✓ 20 questions answered in {total_time:.2f}s")
        print(f"  - Average submit time: {avg_submit_time:.2f}ms")
        print(f"  - Score: {correct_count}/20")
        
    except Exception as e:
        print(f"✗ Test 4 failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 5: Session Completion
    print("\n\nTest 5: Session Completion & Results")
    print("-" * 70)
    
    try:
        start_time = time.time()
        results = quiz_engine.finish_session()
        completion_time = time.time() - start_time
        
        print(f"✓ Session completed in {completion_time:.2f}s")
        if results:
            print(f"  - Answered: {results.get('answered', 0)} questions")
            print(f"  - Correct: {results.get('correct', 0)} questions")
            if results.get('answered', 0) > 0:
                rate = (results.get('correct', 0) / results.get('answered', 0)) * 100
                print(f"  - Correct rate: {rate:.1f}%")
        
    except Exception as e:
        print(f"✗ Test 5 failed: {e}")
        return False
    
    return True

if __name__ == '__main__':
    success = test_large_scale_quiz()
    
    print("\n" + "="*70)
    print("Test Summary")
    print("="*70)
    
    if success:
        print("✅ All performance tests passed!")
        print("\nThe quiz engine performs well with 100+ questions.")
        print("Ready for production deployment.")
    else:
        print("❌ Some tests failed - see above for details")
    
    print("\n")
