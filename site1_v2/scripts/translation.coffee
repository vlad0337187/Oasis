window.language = 'ru'




translate = (subject) ->
	text
	if window.language == 'ru'
		return eval('ru.' + subject)
	else if window.language == 'en'
		return eval('en.' + subject)
	else
		return 'specified wrong language'


translate_write = (subject) ->
	### Немного не работает. Временно из-за того что сразу получает доступ по id к 'main'###
	if window.language == 'ru'
		text = eval('ru.' + subject)
	else if window.language == 'en'
		text = eval('en.' + subject)
	else
		text = 'specified wrong language'

	document.getElementById('main').innerHTML = text
	return




window.fill_main_menu_according_translation = () ->
	document.getElementById('main').innerHTML =
	eval('window.' + window.language +
	'.main_menu.main')
	document.getElementById('news').innerHTML =
	eval('window.' + window.language +
	'.main_menu.news')
	document.getElementById('development_history').innerHTML =
	eval('window.' + window.language + '.main_menu.development_history')
	document.getElementById('current_state').innerHTML =
	eval('window.' + window.language +
	'.main_menu.current_state')
	document.getElementById('gallery').innerHTML =
	eval('window.' + window.language +
	'.main_menu.gallery')
	document.getElementById('donations').innerHTML =
	eval('window.' + window.language +
	'.main_menu.donations')




window.eng =
	main_menu:
		{main: 'Main', news: 'News', development_history: 'Development history', current_state: 'State of project', gallery: 'Gallery', donations: 'Donations'}
window.ru =
	main_menu:
		{main: 'Главная', news: 'Новости', development_history: 'История разработки', current_state: 'Состояние проекта', gallery: 'Галерея', donations: 'Пожертвования'}








switch document.readyState
	when 'loading'
		document.addEventListener('DOMContentLoaded', window.fill_main_menu_according_translation, false)
	when 'interactive', 'complete'
		window.fill_main_menu_according_translation()
