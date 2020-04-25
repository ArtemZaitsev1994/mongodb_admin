$(document).ready(function(){
    local_token = localStorage.getItem('Authorization')
    cookie_token = $.cookie('Authorization')

    if (cookie_token === undefined && local_token === null){
        // Если у нас нет токена нигде, просим сервер ссылку на авторизацию
        $.ajax({
            dataType: 'json',
            url: '/api/get_auth_link',
            type: 'POST',
            data: JSON.stringify({}),
            processData: false,
            contentType: false,
            success: function(data){
                if (data.success){
                    window.location.replace(data.auth_link);
                } else {
                    draw_error('Ошибка на стороне сервера')
                }
            }
        })
    } else if (cookie_token !== undefined){
        // если токен пришел в куках 
        // приходит, если мы залогинились только что -> валидный по определению
        localStorage.setItem('Authorization', cookie_token)
        $.removeCookie('Authorization')
    } else if (local_token !== null){
        // если токен есть у нас в локал сторедже, проверям валидный ли он до сих пор
        $.ajax({
            dataType: 'json',
            url: '/api/check_token',
            type: 'POST',
            data: JSON.stringify({'token': local_token}),
            processData: false,
            contentType: false,
            beforeSend: function(request) {
                request.setRequestHeader("Authorization", local_token);
            },
            success: function(data){
                if (data.success){

                } else {
                    window.location.replace(data.auth_link);
                }
            }
        })
    }
    token = localStorage.getItem('Authorization')
    console.log(token)

    function checkAuth(data){
        if (!data.success && data.invalid_token){
            console.log(11111111111111111111)
            window.location.replace(data.auth_link);
        }
    }


    var current_bd, current_collection
    var fields = []
    var full_text = ''


    function check_height(e) {
        // Если появляется скролл и его ширина больше клиентской → увеличиваем ширину клиента
        if (this.scrollHeight > this.clientHeight) {
            this.style.height = this.scrollHeight + 5 + 'px';
        }
    }
    $('.json_items').map(check_height)


    function draw_fields(fields){
        $('#fields').empty()
        for (let li of fields){
            $('#fields').append(`<button id=field_${li} class="field btn btn-outline-primary list-group-item" value="${li}">${li}</button>`)
        }
        $('.field').on('click', choose_field)
    }


    function draw_items(items) {
        $('#items_container').empty()
        for (item of items){
            $('#items_container').append(`
                <form role="form" style="width:100%">
                    <div class="form-group row">
                        <textarea id="${item['_id']}" class="json_items" style="width:7000px">${JSON.stringify(item, undefined, 2)}</textarea>
                    </div>

                    <input class="btn btn-primary submit" title="Сохранить" type="button" data-id="${item['_id']}" value="Сохранить">
                    <input class="btn btn-danger delete" title="Удалить" type="button" data-id="${item['_id']}" value="Удалить">
                        <div id="${item['_id']}_error_message" style="color: red"></div>
                        <div id="${item['_id']}_success_messagea" style="color: green"></div>
                    <div class="form-group"></div>
                    <hr>
                </form>`);
        }

        $('.submit').on('click', send_data)
        $('.delete').on('click', remove_item)
    }


    function draw_error(error) {
        $('#items_container').empty()
        $('#error_message').html(`
            <form style="width:100%;color: red">
                <div class="form-group row">
                    ${error}    
                </div>
            </form>`
        )
    }


    function draw_pagination(pag){
        if (pag.page <= 1) {
            $('#prev_link').attr('class', 'disabled')
        } else {
            $('#prev_link').removeAttr('class', 'disabled')
        }
        if (!pag.has_next) {
            $('#next_link').attr('class', 'disabled')
        } else {
            $('#next_link').removeAttr('class', 'disabled')
        }

        $('#prev_link').attr('page', pag.prev)
        $('#next_link').attr('page', pag.next)

        $('.json_items').map(check_height)
        $('.json_items').on('input', check_height)
    }


    function draw_dbs(dbs){
        $('#databases_list').empty()
        for (let db of dbs){    
            $('#databases_list').append(
                `<a href="#" class="nav-link databases" data-database="${db.name}">${db.name}</a>
                  <ul id="${db.name}" style="display: none"> </ul>`
            )
            for (let c of db.collections){
                $(`#${db.name}`).append(
                    `<li class="collections" data-db="${db.name}" data-collection="${c}" class="nav-item">
                        <a class="nav-link" href="">${c}</a>
                    </li>`
                )
            }
        }

        $('.databases').on('click', show_hide_collection)
        $('.collections').on('click', get_collection)
    }


    function send_data(e) {
        _id = this.dataset.id
        try {
            data = JSON.parse($(`#${_id}`).val())
        } catch(e) {
            $(`#${this.dataset.id}_error_message`).text('Ошибка: неверная структура JSON')
            return
        }
        data.item_id = data._id
        delete data._id
        data.collection = current_collection
        data.db = current_bd
        $.ajax({
            dataType: 'json',
            url: '/api/save_item',
            type: 'POST',
            data: JSON.stringify(data),
            processData: false,
            contentType: false,
            beforeSend: function(request) {
                request.setRequestHeader("Authorization", token);
            },
            success: function(data) {
                checkAuth(data)
                answers = {
                    'inserted': 'Был создан новый документ',
                    'updated': 'Документ был обновлен',
                    'failed': 'Документ не был вставлен',
                    'invalid_id': 'Невалидный _id'
                }
                if (data.success){
                    $(`#${_id}_success_messagea`).text(answers[data.message])
                } else {
                    $(`#${_id}_error_message`).text(answers[data.message])
                }
                
            }
        })
    }


    function get_dbs() {
        $.ajax({
            dataType: 'json',
            url: '/api/get_dbs',
            type: 'POST',
            data: JSON.stringify({}),
            processData: false,
            contentType: false,
            beforeSend: function(request) {
                request.setRequestHeader("Authorization", token);
            },
            // headers: {
            //     'Authorization':'Basic xxxxxxxxxxxxx',
            //     'X-CSRF-TOKEN':'xxxxxxxxxxxxxxxxxxxx',
            //     'Content-Type':'application/json'
            // },
            success: function(data){
                checkAuth(data)
                if (data.success){
                    draw_dbs(data.dbs)
                } else {
                    draw_error('Ошибка на стороне сервера')
                    $('#database-items').css('display', 'none')
                }
            }
        })
    }
    get_dbs()


    function get_collection(e) {
        e.preventDefault()
        console.log
        current_collection = this.dataset.collection
        current_bd = this.dataset.db
        data = {
            'db': current_bd,
            'collection': current_collection
        }
        $.ajax({
            dataType: 'json',
            url: '/api/get_data',
            type: 'POST',
            data: JSON.stringify(data),
            processData: false,
            contentType: false,
            beforeSend: function(request) {
                request.setRequestHeader("Authorization", token);
            },
            success: function(data){
                checkAuth(data)
                if (data.success){
                    $('#collection_name').text(current_collection)
                    $('#full_text').css('display', 'block')
                    $('#database-items').css('display', 'block')
                    draw_items(data.items)
                    draw_fields(data.item_fields)
                    draw_pagination(data.pagination)
                } else {
                    draw_error('Ошибка на стороне сервера')
                    $('#database-items').css('display', 'none')
                }
            }
        });
    }


    function choose_field(e) {
        elem = $(`#${this.id}`)
        value = this.value
        if (elem.hasClass('btn-outline-primary')) {
            elem.removeClass('btn-outline-primary')
            elem.addClass('btn-primary')
            elem.css('background-color', '#007bff')
            fields.push(this.value)
        } else {
            elem.removeClass('btn-primary')
            elem.addClass('btn-outline-primary')
            elem.css('background-color', '')
            fields.splice(fields.indexOf(value), 1)
        }
        data = {
            'fields_filter': fields,
            'db': current_bd,
            'collection': current_collection
        }
        $.ajax({
            dataType: 'json',
            url: '/api/get_data',
            type: 'POST',
            data: JSON.stringify(data),
            processData: false,
            contentType: false,
            beforeSend: function(request) {
                request.setRequestHeader("Authorization", token);
            },
            success: function(data){
                checkAuth(data)
                if (data.success){
                    draw_items(data.items)
                    draw_pagination(data.pagination)
                } else {
                    draw_error('Ошибка на стороне сервера')
                    $('#database-items').css('display', 'none')
                }
            }
        });
    }


    function show_hide_collection(e) {
        if ($(`#${this.dataset.database}`).css('display') == 'none') {
            $(`#${this.dataset.database}`).css('display', 'block')
        } else {
            $(`#${this.dataset.database}`).css('display', 'none') 
        }
    }


    function full_text_search(e) {
        full_text = this.value
        data = {
            'text': full_text,
            'db': current_bd,
            'collection': current_collection
        }
        $.ajax({
            dataType: 'json',
            url: '/api/get_data',
            type: 'POST',
            data: JSON.stringify(data),
            processData: false,
            contentType: false,
            beforeSend: function(request) {
                request.setRequestHeader("Authorization", token);
            },
            success: function(data){
                checkAuth(data)
                if (data.success){
                    $('#full_text_error').css('display', 'none')
                    draw_items(data.items)
                    draw_fields(data.item_fields)
                    draw_pagination(data.pagination)
                } else {
                    $('#full_text_error').css('display', 'block')
                }
            }
        });
    }


    function get_items_by_pagination(e){
        e.preventDefault()
        data = {
            'db': current_bd,
            'collection': current_collection,
            'page': this.attributes.page.value,
            'full_text': full_text,
            'fields_filter': fields,
        }
        $.ajax({
            dataType: 'json',
            url: '/api/get_data',
            type: 'POST',
            data: JSON.stringify(data),
            processData: false,
            contentType: false,
            beforeSend: function(request) {
                request.setRequestHeader("Authorization", token);
            },
            success: function(data){
                checkAuth(data)
                if (data.success){
                    draw_items(data.items)
                    draw_fields(data.item_fields)
                    draw_pagination(data.pagination)
                } else {
                    draw_error('Ошибка на стороне сервера')
                    $('#database-items').css('display', 'none')
                }
            }
        })
    }


    function remove_item(e){
        _id = this.dataset.id
        data = {
            '_id': this.dataset.id,
            'db': current_bd,
            'collection': current_collection
        }
        $.ajax({
            dataType: 'json',
            url: '/api/remove_item',
            type: 'POST',
            data: JSON.stringify(data),
            processData: false,
            contentType: false,
            beforeSend: function(request) {
                request.setRequestHeader("Authorization", token);
            },
            success: function(data) {
                checkAuth(data)
                answers = {
                    'removed': 'Документ был удален',
                    'failed': 'Документ не был удален',
                    'invalid_id': 'Невалидный _id'
                }
                if (data.success){
                    $(`#${_id}_success_messagea`).text(answers[data.message])
                } else {
                    $(`#${_id}_error_message`).text(answers[data.message])
                }
                
            }
        })
    }


    $('#full_text').on('input', full_text_search)
    $('#save_new_item').on('click', send_data)
    $('.get_beer_btn').on('click', get_items_by_pagination)

})