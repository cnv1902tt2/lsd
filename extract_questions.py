#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tự động trích xuất câu hỏi và đáp án từ file HTML
"""

import re
import os
import json
from html import unescape

def clean_text(text):
    """Làm sạch text, loại bỏ khoảng trắng thừa"""
    if not text:
        return ""
    text = unescape(text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_questions_from_html(html_content):
    """Trích xuất câu hỏi và đáp án từ nội dung HTML"""
    questions = []
    
    # Tìm tất cả các block câu hỏi
    question_blocks = re.findall(
        r'<azt-question-standalone-for-preview[^>]*>.*?</azt-question-standalone-for-preview>',
        html_content,
        re.DOTALL
    )
    
    # Đánh số câu hỏi tăng dần từ 1
    question_counter = 1
    
    for block in question_blocks:
        question_data = {}
        
        # Trích xuất ID gốc (để tham khảo)
        label_match = re.search(
            r'<div[^>]*class="question-standalone-label"[^>]*>\s*Câu&nbsp;\s*(\d+)&nbsp;.*?ID:\s*(\d+)',
            block,
            re.DOTALL
        )
        if label_match:
            question_data['original_number'] = label_match.group(1)
            question_data['id'] = label_match.group(2)
        
        # Gán số câu hỏi tăng dần
        question_data['number'] = str(question_counter)
        
        # Trích xuất nội dung câu hỏi
        content_match = re.search(
            r'<azt-question-content-box[^>]*>.*?<span class="ng-star-inserted">(.*?)</span>',
            block,
            re.DOTALL
        )
        if content_match:
            question_data['question'] = clean_text(content_match.group(1))
        
        # Trích xuất các đáp án
        answers = []
        answer_pattern = r'<div[^>]*class="answer ng-star-inserted"[^>]*>.*?<b[^>]*class="answer-label"[^>]*>\s*([A-D])\.\s*</b>.*?<span class="ng-star-inserted">(.*?)</span>'
        answer_matches = re.findall(answer_pattern, block, re.DOTALL)
        
        for label, answer_text in answer_matches:
            answers.append({
                'label': label,
                'text': clean_text(answer_text)
            })
        question_data['answers'] = answers
        
        # Trích xuất đáp án đúng
        correct_answer_match = re.search(
            r'Đáp án:\s*([A-D])',
            block
        )
        if correct_answer_match:
            question_data['correct_answer'] = correct_answer_match.group(1)
        
        if 'question' in question_data:
            questions.append(question_data)
            question_counter += 1  # Tăng số thứ tự câu hỏi
    
    return questions

def save_questions_to_txt(questions, output_file):
    """Lưu câu hỏi vào file txt"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("DANH SÁCH CÂU HỎI VÀ ĐÁP ÁN\n")
        f.write("=" * 80 + "\n\n")
        
        for q in questions:
            f.write(f"Câu {q.get('number', 'N/A')} (ID: {q.get('id', 'N/A')})\n")
            f.write(f"{q.get('question', '')}\n\n")
            
            for answer in q.get('answers', []):
                f.write(f"  {answer['label']}. {answer['text']}\n")
            
            f.write(f"\nĐáp án đúng: {q.get('correct_answer', 'N/A')}\n")
            f.write("\n" + "-" * 80 + "\n\n")
        
        f.write(f"Tổng số câu hỏi: {len(questions)}\n")

def save_questions_to_json(questions, output_file):
    """Lưu câu hỏi vào file JSON"""
    data = {
        "total_questions": len(questions),
        "questions": questions
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def process_html_file(html_file_path):
    """Xử lý file HTML"""
    print(f"Đang đọc file: {html_file_path}")
    
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print("Đang trích xuất câu hỏi...")
    questions = extract_questions_from_html(html_content)
    
    print(f"Đã tìm thấy {len(questions)} câu hỏi")
    
    # Tạo tên file output
    base_name = os.path.splitext(os.path.basename(html_file_path))[0]
    output_txt = os.path.join(os.path.dirname(html_file_path), f"{base_name}_questions.txt")
    output_json = os.path.join(os.path.dirname(html_file_path), f"{base_name}_questions.json")
    
    print(f"Đang lưu vào file TXT: {output_txt}")
    save_questions_to_txt(questions, output_txt)
    
    print(f"Đang lưu vào file JSON: {output_json}")
    save_questions_to_json(questions, output_json)
    
    print("Hoàn thành!")
    return output_txt, output_json

def process_all_files_in_folder(folder_path):
    """Xử lý tất cả các file trong thư mục"""
    print(f"Đang quét thư mục: {folder_path}")
    
    files_processed = []
    
    # Quét tất cả các file trong thư mục
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Bỏ qua thư mục và các file không phải HTML
        if os.path.isdir(file_path):
            continue
        
        # Kiểm tra xem file có phải là de_1, de_2, ... không
        if re.match(r'^de_\d+$', filename):
            print(f"\n{'='*80}")
            output_txt, output_json = process_html_file(file_path)
            files_processed.append(output_txt)
            files_processed.append(output_json)
    
    print(f"\n\n{'='*80}")
    print(f"ĐÃ XỬ LÝ {len(files_processed)} FILE")
    print(f"{'='*80}")
    for f in files_processed:
        print(f"  - {f}")

if __name__ == "__main__":
    # Thư mục chứa các file đề thi
    folder_path = r"d:\De Thi"
    
    # Xử lý tất cả các file trong thư mục
    process_all_files_in_folder(folder_path)
