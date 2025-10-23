from pathlib import Path

from utilities.keyword_config import company_patterns

def filter_pageviews(input_file, output_file):
    """
    Filter pageviews with context-aware company matching.
    """

    input_path = Path(input_file)
    output_path = Path(output_file)
    
    matched_count = 0
    
    with input_path.open('r', encoding='utf-8') as infile, \
         output_path.open('w', encoding='utf-8') as outfile:
        
        for line in infile:
            parts = line.split(' ', 2)
            
            if len(parts) >= 2:
                page_title_lower = parts[1].lower()
                is_match = False
                
                # Company patterns now imported
                for company, patterns in company_patterns.items():
                    has_include = any(kw in page_title_lower for kw in patterns["include"])
                    
                    if has_include:
                        has_exclude = any(excl in page_title_lower for excl in patterns["exclude"])
                        
                        if not has_exclude:
                            is_match = True
                            break
                
                if is_match:
                    outfile.write(line)
                    matched_count += 1

    return matched_count
