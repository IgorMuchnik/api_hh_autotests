api_url = "https://api.hh.ru/"
areas_url = api_url + "areas"
area_url = api_url + "areas/{}"
employers_url = api_url + "employers"
vacancies_url = api_url + "vacancies"

codes_success = [x+200 for x in range(100)]
codes_client_error = [x+400 for x in range(100)]

invalid_area_ids = ['9999999999999999', 'qwerty', '-1',
                    '<script>alert("wtf")</script>', ' ']

country_name = "Россия"
region_name = "Санкт-Петербург"
company_name = "IQ Орtiоn Sоftwаre"
vacancy_name = "QA Engineer"

country_id = 0  # detecting on runtime
region_id = 0   # detecting on runtime
company_id = 0  # detecting on runtime

thread_count = 32
