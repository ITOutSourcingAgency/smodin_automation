import sys, os

def get_script_path():
	if getattr(sys, 'frozen', False):
		script_path = os.path.dirname(sys.executable)
	else:
		script_path = os.path.dirname(os.path.abspath(__file__))
	return script_path

def modify_file_with_template(content, one_setting, index, one_file):
	splitted_texts = content.split('.')
	total_sentences = len(splitted_texts) - 1
	template_content = ''

	try:
		if '.txt' not in os.path.basename(rf'{one_setting["template_folder"]}'):
			matched_template_file = os.path.join(rf'{one_setting["template_folder"]}', os.path.basename(rf'{one_file}'))
			with open(rf'{matched_template_file}', 'r', encoding='utf-8') as template_file:
				template_content = template_file.read()
		else:
			with open(rf'{one_setting["template_folder"]}', 'r', encoding='utf-8') as template_file:
				print(f'template_file = {template_file}')
				template_content = template_file.read()
	except Exception as e:
		print(f'====================================\nerror = {e}')

	inquote_count = template_content.count('<인용구')


	# 각 chunk의 문장 수 계산
	sentences_per_chunk = total_sentences // inquote_count

	chunks = []
	tmp = ''
	count = 0
	for text in splitted_texts:
		if len(text.strip()) == 0:
			continue
		tmp += f'{text}.'
		count += 1
		if count % sentences_per_chunk == 0:
			chunks.append(tmp.strip())
			tmp = ''

	if tmp:
		chunks.append(tmp.strip())

	first_inquote_idx = template_content.find('<인용구')
	remaining_chunks = chunks.copy()
	search_start_idx = first_inquote_idx + 1
	while remaining_chunks and search_start_idx < len(template_content):
		next_inquote_idx = template_content.find('<인용구', search_start_idx)
		if next_inquote_idx == -1:
			break

		chunk = remaining_chunks.pop(0)
		template_content = template_content[:next_inquote_idx] + chunk + '\n\n' + template_content[next_inquote_idx:]
		search_start_idx = template_content.find('>\n', next_inquote_idx + len(chunk))

	# 남은 chunk를 마지막 <인용구> 또는 <랜덤슬라이드> 태그 밑에 추가
	if remaining_chunks:
		last_placeholder_idx = max(template_content.rfind('<인용구'), template_content.rfind('}>\n<랜덤슬라이드'))
		if last_placeholder_idx != -1:
			last_placeholder_idx += 3
			end_of_last_inquote_idx = template_content.find('>', last_placeholder_idx) + 1
			next_line_start_idx = end_of_last_inquote_idx
			while next_line_start_idx < len(template_content) and template_content[next_line_start_idx] in ['\n', ' ']:
				next_line_start_idx += 1

			insertion_idx = next_line_start_idx
			template_content = template_content[:insertion_idx] + '\n\n' + '\n\n'.join(remaining_chunks).strip() + '\n\n' + template_content[insertion_idx:]
		else:
			template_content += '\n\n' + '\n\n'.join(remaining_chunks).strip()

	tmp_index = ''
	if index == 0:
		tmp_index = '.txt'
	else:
		tmp_index = f'_{index}.txt'        

	output_origin_file_name = os.path.basename(rf'{one_file}').replace('.txt', tmp_index)
	output_origin_directory = os.path.join(get_script_path(), 'srcs', '결과원본파일')
	if not os.path.exists(output_origin_directory):
		os.makedirs(output_origin_directory)
	output_origin_file_path = rf'{os.path.join(output_origin_directory, output_origin_file_name)}'

	with open(output_origin_file_path, 'w', encoding='utf-8') as modified_origin_file:
		modified_origin_file.write(content)

	output_file_name = os.path.basename(rf'{one_file}').replace('.txt', tmp_index)
	output_directory = os.path.join(get_script_path(), 'srcs', '결과파일')
	if not os.path.exists(output_directory):
		os.makedirs(output_directory)
	output_file_path = rf'{os.path.join(output_directory, output_file_name)}'

	with open(output_file_path, 'w', encoding='utf-8') as modified_file:
		modified_file.write(template_content)

my_con = '오늘 성형수술을 통해 가장 큰 변화를 준 얼굴 윤곽에 대한 기본적인 정보와 수술 후 얼굴을 어떻게 수술할 것인가에 대해 이야기하려고 합니다. 얼굴의 전체적인 모양과 비율도 얼굴, 눈, 코, 입 등의 모양에 따라 다르지만 수술만으로는 극적인 변화를 가져올 수 없다. 1. 인식 변화수술 후에는 항상 안경을 잘 써야 해요. 물론 이를 닦는 것도 중요하지만 치약이 칫솔질 부위로 들어가지 않도록 절개하지 않아도 되고 입을 깨끗하게 유지하는 것도 어려울 수 있다. 구강 청결을 유지하기 위해 다음 레시피를 제공 : 얼굴 윤곽을 형성한 후 적어도 일주일 동안 안경을 부지런히 착용해야 합니다. 실이 없는 부분에만 이를 닦으세요. 잠자리에 들기 전에, 잠에서 깨어난 후에, 식사 후에 반드시 입을 다물어라. 약을 머리 뒤로 쳐서 입을 움직이지 말고 머리를 움직여라. 2. 당일 과정입을 다물기가 어렵다면 손으로 입을 막으세요. 병원에서 처방한 구강 세정제를 모두 사용한 후에는 재치료를 받거나 약국에서 리스테린을 구입해 물로 희석하면 된다. 입을 헹군 후 아프지 않거나 맞지 않으면 물이나 소금물로 치아를 헹궈낼 수 있다. 일주일 후, 그들은 병원의 지시에 따라 부드럽고 조심스럽게 이를 닦기 시작할 것이다. 얼굴의 윤곽을 보면 입 안쪽에서 절개하여 입 안쪽에 절개선을 형성합니다. 입 안으로 들어가는 음식 통로는 다양한 세균이 살 수 있게 해 감염과 상처 염증을 유발할 수 있다. 3. 전후 비교 과정이를 위해 안면윤곽형 수술을 받은 경우 위에 안경을 써야 감염과 염증을 예방할 수 있다. 수술 부위는 실이 녹을 때까지 계속 감쌀 수 있다. 감염과 염증은 결과에 나쁜 영향을 미칠 수 있고 심각한 부작용을 일으킬 수 있기 때문에 수행되는 모든 수술은 철저히 통제되어야 한다. 안경은 안경 벤딩 수술 후 최소 일주일 동안 착용해야 합니다. 이것은 실이 완전히 녹을 때까지 계속 분쇄할 필요가 있다. 4. 자신감 회복자기 전에, 아침에 일어나면, 식사 후에 태워야 해요. 콘센트 액체를 더 좋게 만들기 위해 입을 움직이지 않고 머리를 움직이세요. 입을 잘 다물지 못하면, 손으로 입술을 막고 봉인을 하세요. 치실 없이 칫솔질만 조심스럽게 할 수 있다. 평일부터 병원 지시에 따라 양치질을 시작하세요. 수술 일주일 후, 머리는 심장보다 더 높을 것이고 붓기를 줄일 것이다. 5. 완성도에 따른 만족감수술 후 한 달 동안은 그들은 엎드리거나 고개를 숙이지 않았다. 수술 후에, 그들은 6시간 동안 부드러운 음식만 먹을 것이다. 수술 후 2주 동안은 자극적이거나 딱딱한 음식을 피하고 2개월 동안은 조심해야 한다. 3개월 동안 작동 부위를 누르거나 자극하지 않도록 주의해야 한다. 수술 후 적절한 수분과 구강 건강을 유지하는 것이 중요하다. 베개는 주의해야 감염과 염증을 예방할 수 있다.'

one_setting = {
	"name":"test",
    "template_folder": "C:/Users/yoyob/바탕 화면/projects/smodin_automation/srcs/템플릿파일"
}
modify_file_with_template(my_con, one_setting, 0, os.path.join("C:", "Users", "yoyob", "바탕 화면", "projects", "smodin_automation", "srcs", "수정할파일", "남자 안면윤곽.txt"))
