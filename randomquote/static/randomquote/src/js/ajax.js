
let get_data_url = '/popular/get_data/' // Переход на ссылку с ajax запросом

function draw_messages(messages) { // То что мы будем делать с нашими данными
  console.log(messages) // Сейчас мы просто хотим вывести их в консоль
}

function like(){
  
}

function ajax_get(){
  return fetch(get_data_url, {
      method: 'GET',
  }).then(response => response.json()) // Преобразуем полученный ответ в JSON
    .then(data => draw_messages(data)) // Обрабатываем данные, полученные в ответе с помощью функции draw_message [3 строка]
    .catch(error => console.error('Ошибка:', error)); // Если возникли ошибки, выводим их в консоль
}