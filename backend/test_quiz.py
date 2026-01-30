"""Test script to debug quiz generation."""
import sys
import os
import traceback

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.scraper import scrape_wikipedia
from app.services.llm_service import generate_quiz, generate_related_topics

def test_quiz_generation():
    url = "https://en.wikipedia.org/wiki/Alan_Turing"
    
    print("=== Step 1: Scraping Wikipedia ===")
    try:
        scraped_data = scrape_wikipedia(url)
        print(f"Title: {scraped_data['title']}")
        print(f"Summary length: {len(scraped_data['summary'])}")
        print(f"Content length: {len(scraped_data['content'])}")
        print(f"Sections: {scraped_data['sections'][:5]}")
        print(f"Entities: {scraped_data['key_entities']}")
    except Exception as e:
        print(f"Scraping error: {e}")
        print("\n=== FULL TRACEBACK ===")
        traceback.print_exc()
        print("=== END TRACEBACK ===\n")
        return
    
    print("\n=== Step 2: Generating Quiz ===")
    try:
        quiz = generate_quiz(
            title=scraped_data['title'],
            content=scraped_data['content'],
            num_questions=5
        )
        print(f"Generated {len(quiz)} questions")
        for i, q in enumerate(quiz[:2]):
            print(f"\nQ{i+1}: {q['question'][:80]}...")
            print(f"  Answer: {q['answer']}")
    except Exception as e:
        print(f"Quiz generation error: {e}")
        print("\n=== FULL TRACEBACK ===")
        traceback.print_exc()
        print("=== END TRACEBACK ===\n")
        return
    
    print("\n=== Step 3: Generating Related Topics ===")
    try:
        topics = generate_related_topics(
            title=scraped_data['title'],
            sections=scraped_data['sections'],
            entities=scraped_data['key_entities']
        )
        print(f"Related topics: {topics}")
    except Exception as e:
        print(f"Related topics error: {e}")
        print("\n=== FULL TRACEBACK ===")
        traceback.print_exc()
        print("=== END TRACEBACK ===\n")
    
    print("\n=== All tests passed! ===")

if __name__ == "__main__":
    test_quiz_generation()
