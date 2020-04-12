$(document).ready(function(){


    var current_bd, current_collection
    var fields = []
    var full_text = ''


    function showError(error){
        $('#success').html('');
        $('#error').html(error);
    }


    function check_height(e) {
        // Если появляется скролл и его ширина больше клиентской → увеличиваем ширину клиента
        if (this.scrollHeight > this.clientHeight) {
            this.style.height = this.scrollHeight + 5 + 'px';
        }
    }
    $('.json_items').map(check_height)

    function send_data(e) {
        data = JSON.parse($(`#${this.dataset.id}`).val())
        data.item_id = data._id
        delete data._id
        data.collection = current_collection
        data.db = current_bd
        $.ajax({
            dataType: 'json',
            url: '/save_item',
            type: 'POST',
            data: JSON.stringify(data),
            success: function(data) {
                console.log(data)
            }
        })
    }

    function save_new_item() {
        data = JSON.parse($(`#new_item_json`).val())
        $.ajax({
            dataType: 'json',
            url: '/beerblog/save_item',
            type: 'POST',
            data: JSON.stringify(data),
            success: function(data){
                draw_items(data.items)
                draw_fields(data.fields)
                draw_pagination(data.pagination)
            }
        })

    }

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
                    <div class="form-group"></div>
                    <hr>
                </form>`);
        }
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

        $('.submit').on('click', send_data)
        $('.json_items').on('input', check_height)
    }

    function get_collection(e) {
        e.preventDefault()
        current_collection = this.dataset.collection
        current_bd = this.dataset.db
        data = {
            'db': current_bd,
            'collection': current_collection
        }
        $.ajax({
            dataType: 'json',
            url: '/get_data',
            type: 'POST',
            data: JSON.stringify(data),
            processData: false,
            contentType: false,
            success: function(data){
                draw_items(data.items)
                draw_fields(data.fields)
                draw_pagination(data.pagination)
                $('#full_text').css('display', 'block')
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
            url: '/get_data',
            type: 'POST',
            data: JSON.stringify(data),
            processData: false,
            contentType: false,
            success: function(data){
                draw_items(data.items)
                draw_pagination(data.pagination)
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
            url: '/get_data',
            type: 'POST',
            data: JSON.stringify(data),
            processData: false,
            contentType: false,
            success: function(data){
                draw_items(data.items)
                draw_fields(data.fields)
                draw_pagination(data.pagination)
            }
        });
    }

    function get_items_by_pagination(e){
        e.preventDefault()
        current_collection = this.attributes.collection.value
        current_bd = this.attributes.db.value
        data = {
            'db': current_bd,
            'collection': current_collection,
            'page': this.attributes.page.value,
            'full_text': full_text,
            'fields': fields,
        }
        $.ajax({
            dataType: 'json',
            url: '/get_data',
            type: 'POST',
            data: JSON.stringify(data),
            processData: false,
            contentType: false,
            success: function(data){
                draw_items(data.items)
                draw_fields(data.fields)
                draw_pagination(data.pagination)
            }
        })
    }

    $('#full_text').on('input', full_text_search)
    $('#save_new_item').on('click', save_new_item)
    $('.collections').on('click', get_collection)
    $('.databases').on('click', show_hide_collection)
    $('.get_beer_btn').on('click', get_items_by_pagination)

})