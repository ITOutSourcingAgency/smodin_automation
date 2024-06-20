import os, sys

def modify_file_with_template(content):
	with open(content, 'r', encoding='utf-8') as output_file:
		output_content = output_file.read()
	splitted_texts = output_content.split('.')
	chunks = []

	count = 0
	tmp = ''
	for text in splitted_texts:
		tmp += f'{text}.'
		count += 1
		if count % 5 == 0:
			chunks.append(tmp)
			tmp = ''

	with open('/Users/yback/projects/smodin_automation/srcs/템플릿파일/template.txt', 'r', encoding='utf-8') as template_file:
		template_content = template_file.read()

	first_inquote_idx = template_content.find('<인용구')
	remaining_chunks = chunks.copy()

	search_start_idx = first_inquote_idx + 1
	while remaining_chunks:
		next_inquote_idx = template_content.find('<인용구', search_start_idx)
		if next_inquote_idx == -1:
			break

		chunk = remaining_chunks.pop(0)

		template_content = template_content[:next_inquote_idx] + chunk.strip() + '\n\n' + template_content[next_inquote_idx:]
		search_start_idx = template_content.find('>\n', next_inquote_idx + len(chunk.strip()))
	
	if remaining_chunks:
		last_placeholder_idx = template_content.rfind('}>')
		if last_placeholder_idx != -1:
			template_content = template_content[:last_placeholder_idx+2] + '\n\n' + '\n\n'.join(remaining_chunks).strip() + template_content[last_placeholder_idx+2:]
		else:
			template_content += '\n\n' + '\n\n'.join(remaining_chunks).strip()
			
	output_file_name = os.path.basename('/Users/yback/projects/smodin_automation/srcs/수정할파일/file.txt').replace('.txt', f'{search_start_idx}.txt')
	with open(f'{get_script_path()}/srcs/결과파일/{output_file_name}', 'w', encoding='utf-8') as modified_file:
		modified_file.write(template_content)
	print("파일 수정 완료")

def get_script_path():
	if getattr(sys, 'frozen', False):
		# PyInstaller로 패키징된 경우
		script_path = os.path.dirname(sys.executable)
	else:
		# 스크립트가 실행되는 경우
		script_path = os.path.dirname(os.path.abspath(__file__))
	return script_path

modify_file_with_template('/Users/yback/projects/smodin_automation/srcs/수정할파일/file.txt')