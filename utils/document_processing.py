def doc_with_lines(document: str):
    document_lines = document.split("\n")
    document_with_line_numbers = ""
    line2text = {}
    for i, line in enumerate(document_lines):
        document_with_line_numbers += f"[{i}] {line}\n"
        line2text[i] = line
    return document_with_line_numbers, line2text
