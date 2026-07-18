import os
import json
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class DocumentQAChatbot:
    def __init__(self):
        self.faqs = {}
        self.pdf_content = {}
        self.vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')
        self.vectors = None
        self.all_questions = []
        self.load_faqs()
    
    def load_faqs(self):
        """Load FAQs from JSON file"""
        try:
            with open('faqs.json', 'r') as f:
                data = json.load(f)
                self.faqs = {item['question']: item['answer'] for item in data['faqs']}
                self.all_questions = list(self.faqs.keys())
        except FileNotFoundError:
            print("faqs.json not found")
    
    def extract_pdf_text(self, pdf_path):
        """Extract text from PDF"""
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
    
    def add_pdf_knowledge(self, pdf_path):
        """Add PDF content to knowledge base"""
        text = self.extract_pdf_text(pdf_path)
        self.pdf_content[pdf_path] = text
        self._rebuild_vectors()
    
    def _rebuild_vectors(self):
        """Rebuild TF-IDF vectors after adding new content"""
        all_docs = self.all_questions + [text[:500] for text in self.pdf_content.values()]
        if all_docs:
            self.vectors = self.vectorizer.fit_transform(all_docs)
    
    def find_answer(self, user_question, threshold=0.3):
        """Find best matching answer"""
        if not self.all_questions:
            return "No FAQs loaded", 0.0
        
        self._rebuild_vectors()
        user_vector = self.vectorizer.transform([user_question])
        similarities = cosine_similarity(user_vector, self.vectors)[0]
        best_idx = np.argmax(similarities)
        best_score = similarities[best_idx]
        
        if best_score < threshold:
            return "Sorry, I couldn't find a matching answer.", best_score
        
        answer = self.faqs.get(self.all_questions[best_idx], "Answer not found")
        return answer, best_score

