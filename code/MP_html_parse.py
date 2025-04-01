import re
import csv
import html

# Input and output file paths
input_file = 'data/raw/MP_html_source_all_child_care_providers_20250401.html'
output_file = 'data/intermediate/MP_child_care_facilities_20250401.csv'

def extract_text_content(html_text):
    """Extract plain text from HTML content"""
    if not html_text:
        return ''
    
    # Decode HTML entities
    decoded_text = html.unescape(html_text)
    
    # Remove HTML tags
    text_without_tags = re.sub(r'<[^>]*>', ' ', decoded_text)
    
    # Normalize whitespace
    normalized_text = re.sub(r'\s+', ' ', text_without_tags)
    
    return normalized_text.strip()

def extract_emails(html_text):
    """Extract email addresses from mailto links"""
    emails = []
    email_pattern = re.compile(r'href="mailto:([^"]+)"')
    
    for match in email_pattern.finditer(html_text):
        emails.append(match.group(1))
    
    return ', '.join(emails)

def main():
    # Read the HTML file
    with open(input_file, 'r', encoding='utf-8') as file:
        file_content = file.read()
    
    # Extract all sections with facility information
    section_pattern = re.compile(r'<section class="elementor-section elementor-inner-section(.*?)</section>', re.DOTALL)
    sections = section_pattern.findall(file_content)
    
    if not sections:
        print("No sections found in the HTML file.")
        return
    
    # Find all text elements with facility information
    facilities = []
    
    # Process each section
    for section in sections:
        # Check if section has orange text (facility name indicator)
        if '<span style="color: #ff6600;">' not in section:
            continue
        
        # Find the text element in the section
        text_element_pattern = re.compile(r'<div class="elementor-element.*?elementor-widget-text-editor.*?<div class="elementor-widget-container">(.*?)</div>.*?</div>', re.DOTALL)
        text_element_match = text_element_pattern.search(section)
        
        if not text_element_match:
            continue
        
        text_element = text_element_match.group(1)
        
        # Extract the paragraph containing facility info
        paragraph_pattern = re.compile(r'<p>(.*?)</p>', re.DOTALL)
        paragraph_match = paragraph_pattern.search(text_element)
        
        if not paragraph_match:
            continue
        
        paragraph = paragraph_match.group(1)
        
        # Make sure it contains orange text
        if '<span style="color: #ff6600;">' not in paragraph:
            continue
        
        # Extract facility name
        name_pattern = re.compile(r'<span style="color: #ff6600;">(.*?)</span>', re.DOTALL)
        name_match = name_pattern.search(paragraph)
        
        if not name_match:
            continue
        
        # Extract the name from different HTML structures
        name_span = name_match.group(1)
        name = ''
        
        if '<em><strong>' in name_span:
            inner_match = re.search(r'<em><strong>(.*?)</strong></em>', name_span)
            name = extract_text_content(inner_match.group(1)) if inner_match else ''
        elif '<strong><em>' in name_span:
            inner_match = re.search(r'<strong><em>(.*?)</em></strong>', name_span)
            name = extract_text_content(inner_match.group(1)) if inner_match else ''
        else:
            # Try to extract name from any structure
            name = extract_text_content(name_span)
        
        if not name:
            continue
        
        # Split the paragraph by <br /> to get the address lines, phone, director, and email
        lines = paragraph.split('<br />')
        
        # Find lines after the facility name
        name_line_index = -1
        for i, line in enumerate(lines):
            if '<span style="color: #ff6600;">' in line:
                name_line_index = i
                break
        
        content_lines = lines[name_line_index + 1:] if name_line_index >= 0 else lines
        
        # Extract address (first two lines after the name)
        address_line1 = extract_text_content(content_lines[0]) if content_lines else ''
        address_line2 = extract_text_content(content_lines[1]) if len(content_lines) > 1 else ''
        address = ', '.join(filter(None, [address_line1, address_line2]))
        
        # Extract phone number
        phone = ''
        for line in content_lines:
            if 'Tel.:' in line:
                phone = extract_text_content(line).replace('Tel.:', '').strip()
                break
        
        # Extract director/principal/program director
        director = ''
        principal = ''
        program_director = ''
        
        for line in content_lines:
            if 'Director:' in line:
                director = extract_text_content(line).replace('Director:', '').strip()
            elif 'Principal:' in line:
                principal = extract_text_content(line).replace('Principal:', '').strip()
            elif 'Program Director:' in line:
                program_director = extract_text_content(line).replace('Program Director:', '').strip()
        
        # Use the first available director field
        final_director = director or principal or program_director
        
        # Extract email
        email = extract_emails(paragraph)
        
        # Add the facility to our list
        facilities.append({
            'name': name,
            'address': address,
            'phone': phone,
            'director': final_director,
            'email': email
        })
    
    # Remove any duplicate facilities based on the name
    unique_facilities = []
    facility_names = set()
    
    for facility in facilities:
        if facility['name'] not in facility_names:
            facility_names.add(facility['name'])
            unique_facilities.append(facility)
    
    print(f"Successfully extracted information for {len(unique_facilities)} unique facilities")
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Facility Name', 'Address', 'Phone Number', 'Director', 'Email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for facility in unique_facilities:
            writer.writerow({
                'Facility Name': facility['name'],
                'Address': facility['address'],
                'Phone Number': facility['phone'],
                'Director': facility['director'],
                'Email': facility['email']
            })
    
    print(f"CSV file has been created at: {output_file}")
    print(f"Total facilities extracted: {len(unique_facilities)}")

if __name__ == "__main__":
    main()