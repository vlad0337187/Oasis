window.load_according_address = () ->
	#alert "function load_according_link() started"
	main_frame = document.getElementsByName('main_frame')[0]

	###Хэши (текст в адресе после #) не должны совпадать с id элементов
	чтобы браузер автоматически не прокручивал страницу до них###
	switch location.hash
		when '', '#/main'
			main_frame.src = './pages/main_' + window.language + '.html'
			#alert 'hash is empty or main page'
			#alert location.hash
		when '#/news'
			#alert 'hash is not empty'
			#alert location.hash
			main_frame.src = './pages/news_' + window.language + '.html'
		when '#/development_history'
			main_frame.src = './pages/development_history_' + window.language + '.html'
		when '#/current_state'
			main_frame.src = './pages/current_state_' + window.language + '.html'
		when '#/gallery'
			main_frame.src = './pages/gallery_' + window.language + '.html'
		when '#/donations'
			main_frame.src = './pages/donations_' + window.language + '.html'




window.change_address = (address) ->
	location.hash = address








switch document.readyState
	when 'loading'
		document.addEventListener('DOMContentLoaded', window.load_according_address, false)
		window.addEventListener('hashchange', window.load_according_address, false)
	when 'interactive', 'complete'
		window.load_according_address()
		window.addEventListener('hashchange', window.load_according_address, false)
