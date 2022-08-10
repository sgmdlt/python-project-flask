## Анализ страниц

На этом этапе необходимо добавить небольшой SEO-анализ на этап проверки сайта.

### Ссылки

* [DiDOM](https://github.com/Imangazaliev/DiDOM)
* [Хелпер optional()](https://laravel.com/docs/8.x/helpers#method-optional)

### Задачи

* Проверьте наличие тега `<h1>` на странице. Если он есть то запишите его содержимое в базу.
* Проверьте наличие тега `<title>` на странице. Если он есть то запишите его содержимое в базу.
* Проверьте наличие тега `<meta name="description" content="...">` на странице. Если он есть то запишите содержимое аттрибута `content` в базу.
* Выведите эту информацию в списке проверок конкретного сайта.

### Подсказки

* Парсинг и извлечение данных из HTML делается через библиотеку DiDOM.
* Для обращения к свойствам или методам элементов DOM дерева используйте хелпер [optional()](https://laravel.com/docs/8.x/helpers#method-optional).